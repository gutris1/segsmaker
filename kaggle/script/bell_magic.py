from pathlib import Path
from typing import Optional
from IPython import get_ipython
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Audio, display
import requests


class _InvisibleAudio(Audio):
    """
    An invisible (`display: none`) `Audio` element which removes itself when finished playing.
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
    Adds a magic to IPython which will play a given sound when a cell finishes running.
    """

    SOUND_DIR = Path(__file__).parent.resolve()
    FILE_MAP = {
        "1": SOUND_DIR / "1.wav",
        "2": SOUND_DIR / "2.wav",
        "3": SOUND_DIR / "3.wav",
    }
    DEFAULT_URL = "https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav"

    def __init__(self, shell):
        super().__init__(shell)
        self._ensure_audio_files()

    def _ensure_audio_files(self):
        """Download the sound files if they are not present."""
        for num, file_path in self.FILE_MAP.items():
            if not file_path.exists():
                url = f"https://huggingface.co/pantat88/ui/resolve/main/{num}.wav"
                response = requests.get(url)
                file_path.write_bytes(response.content)

    @magic_arguments()
    @argument(
        "-u", "--url", default="1", help="Specify sound by number (1, 2, or 3).",
    )
    @argument(
        "line_code",
        nargs="*",
        help="Other code on the line will be executed unless called as a cell magic.",
    )
    @line_cell_magic
    def notify(self, line: str, cell: Optional[str] = None):
        args = parse_argstring(self.notify, line)

        code = cell if cell else " ".join(args.line_code)
        ret = None
        if code:
            ret = self.shell.ex(code)

        sound_file = self.FILE_MAP.get(args.url, None)
        if sound_file and sound_file.exists():
            audio = _InvisibleAudio(filename=str(sound_file), autoplay=True)
        else:
            audio = _InvisibleAudio(url=self.DEFAULT_URL, autoplay=True)
        
        display(audio)
        return ret

get_ipython().register_magics(NotificationMagics)
