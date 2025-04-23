import atexit
import os
import platform
import re
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

import requests

VERSION = "0.2"
CURRENT_TUNNELS: List["Tunnel"] = []

machine = platform.machine()
if machine == "x86_64":
    machine = "amd64"

BINARY_REMOTE_NAME = f"frpc_{platform.system().lower()}_{machine.lower()}"
EXTENSION = ".exe" if os.name == "nt" else ""
BINARY_URL = f"https://cdn-media.huggingface.co/frpc-gradio-{VERSION}/{BINARY_REMOTE_NAME}{EXTENSION}"

BINARY_FILENAME = f"{BINARY_REMOTE_NAME}_v{VERSION}"
BINARY_FOLDER = Path(__file__).parent.absolute()
BINARY_PATH = f"{BINARY_FOLDER / BINARY_FILENAME}"

TUNNEL_TIMEOUT_SECONDS = 30
TUNNEL_ERROR_MESSAGE = (
    "Could not create share URL. "
    "Please check the appended log from frpc for more information:"
)

GRADIO_API_SERVER = "https://api.gradio.app/v2/tunnel-request"
GRADIO_SHARE_SERVER_ADDRESS = None


class Tunnel:
    def __init__(self, remote_host, remote_port, local_host, local_port, share_token):
        self.proc = None
        self.url = None
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_host = local_host
        self.local_port = local_port
        self.share_token = share_token

    @staticmethod
    def download_binary():
        if not Path(BINARY_PATH).exists():
            resp = requests.get(BINARY_URL)

            if resp.status_code == 403:
                raise OSError(
                    f"Cannot set up a share link as this platform is incompatible. Please "
                    f"create a GitHub issue with information about your platform: {platform.uname()}"
                )

            resp.raise_for_status()

            # Save file data to local copy
            with open(BINARY_PATH, "wb") as file:
                file.write(resp.content)
            st = os.stat(BINARY_PATH)
            os.chmod(BINARY_PATH, st.st_mode | stat.S_IEXEC)

    def start_tunnel(self) -> str:
        self.download_binary()
        self.url = self._start_tunnel(BINARY_PATH)
        return self.url

    def kill(self):
        if self.proc is not None:
            print(f"Killing tunnel {self.local_host}:{self.local_port} <> {self.url}")
            self.proc.terminate()
            self.proc = None

    def _start_tunnel(self, binary: str) -> str:
        CURRENT_TUNNELS.append(self)
        command = [
            binary,
            "http",
            "-n",
            self.share_token,
            "-l",
            str(self.local_port),
            "-i",
            self.local_host,
            "--uc",
            "--sd",
            "random",
            "--ue",
            "--server_addr",
            f"{self.remote_host}:{self.remote_port}",
            "--disable_log_color",
        ]
        self.proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        atexit.register(self.kill)
        return self._read_url_from_tunnel_stream()

    def _read_url_from_tunnel_stream(self) -> str:
        start_timestamp = time.time()

        log = []
        url = ""

        def _raise_tunnel_error():
            log_text = "\n".join(log)
            print(log_text, file=sys.stderr)
            raise ValueError(f"{TUNNEL_ERROR_MESSAGE}\n{log_text}")

        while url == "":
            # check for timeout and log
            if time.time() - start_timestamp >= TUNNEL_TIMEOUT_SECONDS:
                _raise_tunnel_error()

            assert self.proc is not None
            if self.proc.stdout is None:
                continue

            line = self.proc.stdout.readline()
            line = line.decode("utf-8")

            if line == "":
                continue

            log.append(line.strip())

            if "start proxy success" in line:
                result = re.search("start proxy success: (.+)\n", line)
                if result is None:
                    _raise_tunnel_error()
                else:
                    url = result.group(1)
            elif "login to server failed" in line:
                _raise_tunnel_error()

        return url


def setup_tunnel(
    local_host: str,
    local_port: int,
    share_token: str,
    share_server_address: Optional[str],
) -> str:
    share_server_address = (
        GRADIO_SHARE_SERVER_ADDRESS
        if share_server_address is None
        else share_server_address
    )
    if share_server_address is None:
        response = requests.get(GRADIO_API_SERVER)
        if not (response and response.status_code == 200):
            raise RuntimeError("Could not get share link from Gradio API Server.")
        payload = response.json()[0]
        remote_host, remote_port = payload["host"], int(payload["port"])
    else:
        remote_host, remote_port = share_server_address.split(":")
        remote_port = int(remote_port)
    try:
        tunnel = Tunnel(remote_host, remote_port, local_host, local_port, share_token)
        address = tunnel.start_tunnel()
        return address
    except Exception as e:
        raise RuntimeError(str(e)) from e


def main():
    import argparse
    import secrets
    import time

    parser = argparse.ArgumentParser(description="Set up a tunnel.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="the port number to use for the tunnel.",
    )
    parser.add_argument(
        "port_positional",
        type=int,
        nargs="?",
        help="the port number to use for the tunnel.",
    )
    parser.add_argument(
        "--sd", "--subdomain", type=str, help="the subdomain to use for the tunnel."
    )
    args = parser.parse_args()

    if args.port_positional is not None:
        args.port = args.port_positional

    address = setup_tunnel(
        "127.0.0.1",
        args.port,
        secrets.token_urlsafe(32) if args.sd is None else args.sd,
        None,
    )

    print(address, flush=True)
    time.sleep(3600 * 24 * 3)

if __name__ == "__main__":
    main()
