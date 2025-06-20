import argparse
import inspect
import os
import re
import shutil
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from jinja2 import Template

from report.block import AbstractBlock, File
from report.template import HTML_TEMPLATE, REPORT_TEMPLATE
from report.util import get_src_out_dirs

REPORTS_SRC_DIR, REPORTS_OUT_DIR = get_src_out_dirs()
DEBUG_MODE = os.environ.get("DEBUG", False)


class AbstractReport(ABC):
    def __init__(
        self,
        title: str,
        attach_source: bool = True,
        locked: bool = False,
    ):
        """Abstract report that every reports inherits/implements.

        Args:
            title: Report title.
            attach_source: If True (default), the report code will be attached at the end.
            locked: If locked, you cannot override the report. Used for safety.
            debug: If debug, generate the report, but do not clean up the output folder,
                   and do not save the generated report.
                   Use this for interactive pdb-driven development and printing out stuff.

        Raises:
            ValueError: If report it locked, regenerating it fails.
        """
        if locked:
            raise ValueError(
                "Cannot regenerate a locked report. Set locked=True if you want to overwrite."
            )
        self._attach_source = attach_source
        self._locked = locked
        if DEBUG_MODE:
            # Add random stuff to the directory name no to destroy the existing, non-debug
            # version of the report.
            title = f"{title}_{uuid.uuid4().hex}"
        self._title = title
        self._report_dir = os.path.join(REPORTS_OUT_DIR, self._title)

        # I keep this check in case the title is not unique.
        # This way we will crash at 'makedirs' call below.
        if os.path.exists(self._report_dir) and not DEBUG_MODE:
            # We are here -> it's not locked and we are not in the debug mode.
            # Clean everything to generate a new version of the report.
            shutil.rmtree(self._report_dir)
        os.makedirs(self._report_dir)

        self._blocks = []
        self._html = None

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    def add_block(self, block: AbstractBlock):
        """Add a block to the report.

        Args:
            block: Block to add.
        """
        self._blocks.append(block)

    def compile(self):
        template = Template(HTML_TEMPLATE)
        self._html = template.render(title=self._title, blocks=self._blocks)

    def save(self):
        if not self._html:
            raise ValueError("Cannot save a report that has not been compiled.")
        with open(os.path.join(self._report_dir, "report.html"), "w") as f:
            f.write(self._html)

    def generate(self):
        """Generate a report."""
        try:
            self.load_data()
            self.prepare()
            if self._attach_source:
                class_fname = inspect.getfile(self.__class__)
                self.add_block(
                    File(
                        class_fname,
                        self._report_dir,
                        caption="This report was generated with this code.",
                    )
                )
            self.compile()
            self.save()
        finally:
            # Cleanup the temporary directory.
            if DEBUG_MODE:
                shutil.rmtree(self._report_dir)


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
    out_fpath = os.path.join(REPORTS_SRC_DIR, f"{date}_{title}.py")
    if os.path.exists(out_fpath):
        if args.overwrite:
            shutil.rmtree(out_fpath)
        else:
            raise ValueError(
                f"{out_fpath} already exists. Use --overwrite flag to overwrite."
            )
    with open(out_fpath, "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    make_report_template()
