from abc import ABC, abstractmethod
from jinja2 import Template
import argparse
from datetime import datetime
import re
import configparser
from pathlib import Path

CONFIG_FNAME = ".report"
REPORTS_SRC_DIR = "reports_code"
REPORTS_OUT_DIR = "reports"

project_config = Path.joinpath(Path(__file__).resolve().parent.parent, CONFIG_FNAME)
home_config = Path.joinpath(Path.home(), CONFIG_FNAME)
config = configparser.ConfigParser()
if Path.exists(project_config):
    config.read(project_config)
    REPORTS_SRC_DIR = config["DEFAULT"].get("REPORTS_SRC_DIR", REPORTS_SRC_DIR)
    REPORTS_OUT_DIR = config["DEFAULT"].get("REPORTS_OUT_DIR", REPORTS_OUT_DIR)
elif Path.exists(home_config):
    config.read(project_config)
    REPORTS_SRC_DIR = config["DEFAULT"].get("REPORTS_SRC_DIR", REPORTS_SRC_DIR)
    REPORTS_OUT_DIR = config["DEFAULT"].get("REPORTS_OUT_DIR", REPORTS_OUT_DIR)
Path(REPORTS_SRC_DIR).mkdir(parents=True, exist_ok=True)
Path(REPORTS_OUT_DIR).mkdir(parents=True, exist_ok=True)


class AbstractReport(ABC):
    def __init__(self, title):
        self._title = title

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    def save(self):
        # TODO(yobibyte)
        pass

    def generate(self):
        self.load_data()
        self.prepare()
        self.save()


REPORT_TEMPLATE = """from report.base import AbstractReport


class Report(AbstractReport):
    
    def load_data(self):
        raise NotImplementedError

    def prepare(self):
        raise NotImplementedError

if __name__ == "__main__":
    report = Report(title="{{title}}")
    report.generate()
"""


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
    report_code = template.render(title=args.title)
    date = datetime.now().strftime("%Y_%m_%d")
    out_fpath = Path.joinpath(Path(REPORTS_SRC_DIR), f"{date}_{title}.py")
    with open(out_fpath, "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    main()
