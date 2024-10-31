from pathlib import Path
from typing import Optional
from IPython import get_ipython
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Audio, display


class _InvisibleAudio(Audio):
    """
    An invisible (`display: none`) `Audio` element with a volume control,
    which removes itself when finished playing.
    """
    
    def __init__(self, *args, volume=1.0, **kwargs):
        self.volume = volume
        super().__init__(*args, **kwargs)

    def _repr_html_(self) -> str:
        audio = super()._repr_html_()
        audio = audio.replace(
            "<audio",
            f'<audio volume="{self.volume}" onended="this.parentNode.removeChild(this)"'
        )
        return f'<div style="display:none">{audio}</div>'

@magics_class
class NotificationMagics(Magics):
    SOUND_FILE = str(Path(__file__).parent.resolve() / "bell.wav")
    DEFAULT_URL = "https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav"

    @magic_arguments()
    @argument("-u", "--url", default=SOUND_FILE, help="URL of audio file to play.")
    @argument("-m", "--mute", action="store_true", help="Play audio muted (for caching).")
    @argument("line_code", nargs="*", help="Code to execute on the same line.")
    @line_cell_magic
    def notify(self, line: str, cell: Optional[str] = None):
        args = parse_argstring(self.notify, line)
        code = cell if cell else " ".join(args.line_code)

        try:
            ret = self.shell.ex(code)
        finally:
            maybe_url = args.url
            is_muted = args.mute
            volume = 0 if is_muted else 1.0

            if maybe_url == self.SOUND_FILE and Path(self.SOUND_FILE).is_file():
                audio = _InvisibleAudio(filename=maybe_url, autoplay=True, volume=volume)
            else:
                audio = _InvisibleAudio(url=maybe_url, autoplay=True, volume=volume)
            display(audio)

        return ret

get_ipython().register_magics(NotificationMagics)
