import os.path
import shutil
from abc import ABC, abstractmethod

from coolname import generate_slug
from jinja2 import Template
from matplotlib.figure import Figure

from report.template import TABLE_TEMPLATE


class AbstractBlock(ABC):

    @abstractmethod
    def __str__(self) -> str:
        return ""


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
    def __init__(self, fig: Figure, dest_dir: str):
        # TODO(yobibyte): we should somehow get the directory automatically.
        # the user should not think about it.
        os.makedirs(dest_dir, exist_ok=True)

        self._id = f"{generate_slug()}.png"
        self._fname = os.path.join(dest_dir, self._id)
        fig.savefig(self._fname)

    def __str__(self) -> str:
        if not self._fname:
            raise ValueError("You have to save the blocks before compiling a report.")
        return f"<p><img src='{self._id}'></p>"


class File(AbstractBlock):
    def __init__(self, file_path: str, dest_dir: str, caption=""):
        # TODO(yobibyte): we should somehow get the directory automatically.
        # the user should not think about it.
        self._caption = caption

        os.makedirs(dest_dir, exist_ok=True)

        self._id = os.path.basename(file_path)
        self._fname = os.path.join(dest_dir, self._id)
        shutil.copyfile(file_path, self._fname)

    def __str__(self) -> str:
        if not self._fname:
            raise ValueError("You have to save the blocks before compiling a report.")
        link_name = self._caption if self._caption else self._id
        return f"<p><a href='{self._id}'>{link_name}</a></p>"


class Table(AbstractBlock):
    def __init__(self, rows, header, caption=""):
        self._rows = rows
        self._header = header
        self._caption = caption

    def __str__(self) -> str:
        template = Template(TABLE_TEMPLATE)
        return template.render(
            caption=self._caption, rows=self._rows, header=self._header
        )
