from pathlib import Path
from typing import Optional
from IPython import get_ipython
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Audio, display


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
    If a bell.wav file exists in the same directory as this file, that will be used as
    the default sound. Otherwise, the default is the wav file at `DEFAULT_URL`.
    Providing a URL or file path to the magic overrides either of these defaults.
    """

    SOUND_FILE = str(Path(__file__).parent.resolve() / "bell.wav")
    DEFAULT_URL = "https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav"

    @magic_arguments()
    @argument(
        "-u", "--url", default=SOUND_FILE, help="URL or file path of audio file to play.",
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
            if Path(maybe_url).is_file():
                audio = _InvisibleAudio(filename=maybe_url, autoplay=True)
            elif maybe_url == self.SOUND_FILE and Path(self.SOUND_FILE).is_file():
                audio = _InvisibleAudio(filename=self.SOUND_FILE, autoplay=True)
            else:
                audio = _InvisibleAudio(url=maybe_url, autoplay=True)
            display(audio)

        return ret


get_ipython().register_magics(NotificationMagics)
