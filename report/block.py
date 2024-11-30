from abc import ABC, abstractmethod


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
