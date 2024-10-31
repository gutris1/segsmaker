from pathlib import Path
from typing import Optional
from IPython import get_ipython
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Audio, display
import requests


class _InvisibleAudio(Audio):
    def _repr_html_(self) -> str:
        audio = super()._repr_html_()
        audio = audio.replace(
            "<audio", '<audio onended="this.parentNode.removeChild(this)"'
        )
        return f'<div style="display:none">{audio}</div>'


@magics_class
class NotificationMagics(Magics):
    SOUND_DIR = Path(__file__).parent.resolve() / "SOUND"
    SOUND_FILES = {
        "1": "https://huggingface.co/pantat88/ui/resolve/main/1.wav",
        "2": "https://huggingface.co/pantat88/ui/resolve/main/2.wav",
        "3": "https://huggingface.co/pantat88/ui/resolve/main/3.wav"
    }
    
    SOUND_FILE = str(SOUND_DIR / "bell.wav")
    DEFAULT_URL = "https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav"

    def __init__(self, shell):
        super().__init__(shell)
        self._download_sounds()

    def _download_sounds(self):
        for key, url in self.SOUND_FILES.items():
            file_path = self.SOUND_DIR / f"{key}.wav"
            if not file_path.is_file():
                response = requests.get(url)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

    @magic_arguments()
    @argument(
        "-u", "--url", default=SOUND_FILE, help="URL of audio file to play.",
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
            if args.line_code and args.line_code[0] in self.SOUND_FILES:
                sound_key = args.line_code[0]
                audio_file = self.SOUND_DIR / f"{sound_key}.wav"
                audio = _InvisibleAudio(filename=str(audio_file), autoplay=True)
            else:
                maybe_url = args.url
                if maybe_url == self.SOUND_FILE:
                    if Path(self.SOUND_FILE).is_file():
                        audio = _InvisibleAudio(filename=maybe_url, autoplay=True)
                    else:
                        audio = _InvisibleAudio(url=self.DEFAULT_URL, autoplay=True)
                else:
                    audio = _InvisibleAudio(url=maybe_url, autoplay=True)
            display(audio)

        return ret


get_ipython().register_magics(NotificationMagics)
