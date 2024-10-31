from pathlib import Path
from typing import Optional, Union
from IPython import get_ipython
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Audio, display
import requests

class _InvisibleAudio(Audio):
    """
    An invisible (`display: none`) `Audio` element which removes itself when finished playing.
    Taken from https://stackoverflow.com/a/50648266.
    """
    def _repr_html_(self) -> str:
        audio = super()._repr_html_()
        audio = audio.replace(
            "<audio", '<audio onended="this.parentNode.removeChild(this)"'
        )
        return f'<div style="display:none">{audio}</div>'

@magics_class
class NotificationMagics(Magics):
    """
    Magic class to notify via sounds. If a sound file (1.wav, 2.wav, or 3.wav) exists in the same 
    directory as this file, it will be used as a default sound. Otherwise, the default is a URL.
    """

    SOUND_DIR = Path(__file__).parent.resolve()
    SOUND_FILES = {
        1: SOUND_DIR / "1.wav",
        2: SOUND_DIR / "2.wav",
        3: SOUND_DIR / "3.wav",
    }
    SOUND_URLS = {
        1: "https://huggingface.co/pantat88/ui/resolve/main/1.wav",
        2: "https://huggingface.co/pantat88/ui/resolve/main/2.wav",
        3: "https://huggingface.co/pantat88/ui/resolve/main/3.wav",
    }

    def __init__(self, shell):
        super().__init__(shell)
        self._download_sounds()

    def _download_sounds(self):
        for num, path in self.SOUND_FILES.items():
            if not path.is_file():
                url = self.SOUND_URLS[num]
                print(f"Downloading {url} to {path}")
                response = requests.get(url)
                path.write_bytes(response.content)

    @magic_arguments()
    @argument(
        "-u", "--url", default=None, help="URL or integer to play local audio file (1, 2, or 3).",
    )
    @argument(
        "line_code",
        nargs="*",
        help="Other code on the line will be executed, unless this is called as a cell magic.",
    )
    @line_cell_magic
    def notify(self, line: str, cell: Optional[str] = None):
        args = parse_argstring(self.notify, line)
        code = cell if cell else " ".join(args.line_code)

        try:
            ret = self.shell.ex(code)
        finally:
            maybe_url = args.url
            if maybe_url and maybe_url.isdigit() and int(maybe_url) in self.SOUND_FILES:
                file_path = self.SOUND_FILES[int(maybe_url)]
                audio = _InvisibleAudio(filename=file_path, autoplay=True)
            elif maybe_url:
                audio = _InvisibleAudio(url=maybe_url, autoplay=True)
            else:
                audio = _InvisibleAudio(url=self.SOUND_URLS[1], autoplay=True)
            display(audio)

        return ret
