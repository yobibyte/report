from abc import ABC, abstractmethod
from pathlib import Path

from coolname import generate, generate_slug
from matplotlib.figure import Figure


class AbstractBlock(ABC):

    @abstractmethod
    def __str__(self) -> str:
        return ""

    def save(self, dest_dir):
        Path(dest_dir).mkdir(parents=True, exist_ok=True)


class Paragraph(AbstractBlock):
    def __init__(self, text):
        self._text = text

    def __str__(self) -> str:
        return f"<p>{self._text}</p>"


class Header(AbstractBlock):
    def __init__(self, text):
        self._text = text


class H1(Header):
    def __str__(self) -> str:
        return f"<h1>{self._text}</h1>"


class H2(Header):
    def __str__(self) -> str:
        return f"<h2>{self._text}</h2>"


class H3(Header):
    def __str__(self) -> str:
        return f"<h3>{self._text}</h3>"


class Fig(AbstractBlock):
    def __init__(self, fig: Figure, dest_dir: str | Path):
        # TODO(yobibyte): we should somehow get the directory automatically.
        # the user should not think about it.
        self._fig = fig
        self._id = generate_slug()
        self._fname = None
        self.save(dest_dir)

    def __str__(self) -> str:
        if not self._fname:
            raise ValueError("You have to save the blocks before compiling a report.")
        return f"<img src='{self._id}.png'>"

    def save(self, dest_dir):
        super().save(dest_dir)
        self._fname = Path(dest_dir).joinpath(f"{self._id}.png")
        self._fig.savefig(self._fname)
