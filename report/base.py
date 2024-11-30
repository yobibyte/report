import argparse
import re
import shutil
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from jinja2 import Template

from report.block import AbstractBlock
from report.template import HTML_TEMPLATE, REPORT_TEMPLATE
from report.util import get_src_out_dirs

REPORTS_SRC_DIR, REPORTS_OUT_DIR = get_src_out_dirs()


class AbstractReport(ABC):
    def __init__(self, title, locked=False):
        if locked:
            raise ValueError(
                "Cannot regenerate a locked report. Set locked=True if you want to overwrite."
            )
        self._locked = locked
        self._title = title
        self._report_dir = REPORTS_OUT_DIR.joinpath(self._title)
        if self._report_dir.exists():
            # we are here -> it's not locked. Remove the directory.
            shutil.rmtree(self._report_dir)
        self._report_dir.mkdir()
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
        with open(self._report_dir.joinpath("report.html"), "w") as f:
            f.write(self._html)

    def generate(self):
        self.load_data()
        self.prepare()
        self.compile()
        self.save()


def make_report_template():
    parser = argparse.ArgumentParser(description="Generate a report template.")
    parser.add_argument(
        "title",
        type=str,
        help="Report title",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite report template if exists.",
    )
    args = parser.parse_args()
    title = re.sub(r"[./ ]", "_", args.title)
    template = Template(REPORT_TEMPLATE)
    report_code = template.render(title=title)
    date = datetime.now().strftime("%Y_%m_%d")
    out_fpath = Path.joinpath(Path(REPORTS_SRC_DIR), f"{date}_{title}.py")
    if out_fpath.exists():
        if args.overwrite:
            Path.unlink(out_fpath)
        else:
            raise ValueError(
                f"{out_fpath} already exists. Use --overwrite flag to overwrite."
            )
    with open(out_fpath, "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    make_report_template()
