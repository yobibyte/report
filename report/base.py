import argparse
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from jinja2 import Template

from report.block import AbstractBlock
from report.template import HTML_TEMPLATE, REPORT_TEMPLATE
from report.util import get_src_out_dirs

REPORTS_SRC_DIR, REPORTS_OUT_DIR = get_src_out_dirs()


class AbstractReport(ABC):
    def __init__(self, title):
        self._title = title
        self._blocks = []
        self._html = None

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    def add_block(self, block: AbstractBlock):
        self._blocks.append(block)

    def compile(self):
        template = Template(HTML_TEMPLATE)
        self._html = template.render(title=self._title, blocks=self._blocks)

    def save(self):
        if not self._html:
            raise ValueError("Cannot save a report that has not been compiled.")
        report_dir = REPORTS_OUT_DIR.joinpath(self._title)
        report_dir.mkdir()
        with open(report_dir.joinpath("report.html"), "w") as f:
            f.write(self._html)

    def generate(self):
        self.load_data()
        self.prepare()
        self.compile()
        self.save()


def main():
    parser = argparse.ArgumentParser(description="Generate a report template.")
    parser.add_argument(
        "title",
        type=str,
        help="Report title",
    )
    args = parser.parse_args()
    title = re.sub(r"[./ ]", "_", args.title)
    template = Template(REPORT_TEMPLATE)
    report_code = template.render(title=title)
    date = datetime.now().strftime("%Y_%m_%d")
    out_fpath = Path.joinpath(Path(REPORTS_SRC_DIR), f"{date}_{title}.py")
    with open(out_fpath, "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    main()
