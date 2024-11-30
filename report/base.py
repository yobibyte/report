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
    REPORTS_SRC_DIR = Path(config["DEFAULT"].get("REPORTS_SRC_DIR", REPORTS_SRC_DIR))
    if not REPORTS_SRC_DIR.is_absolute():
        REPORTS_SRC_DIR = Path.joinpath(Path(__file__).resolve().parent.parent, REPORTS_SRC_DIR)
    REPORTS_OUT_DIR = Path(config["DEFAULT"].get("REPORTS_OUT_DIR", REPORTS_OUT_DIR))
    if not REPORTS_OUT_DIR.is_absolute():
        REPORTS_OUT_DIR = Path.joinpath(Path(__file__).resolve().parent.parent, REPORTS_OUT_DIR)
elif Path.exists(home_config):
    config.read(project_config)
    REPORTS_SRC_DIR = config["DEFAULT"].get("REPORTS_SRC_DIR", REPORTS_SRC_DIR)
    REPORTS_OUT_DIR = config["DEFAULT"].get("REPORTS_OUT_DIR", REPORTS_OUT_DIR)
    #todo
else:
    REPORTS_SRC_DIR = Path(REPORTS_SRC_DIR)
    REPORTS_OUT_DIR = Path(REPORTS_OUT_DIR)
REPORTS_SRC_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_OUT_DIR.mkdir(parents=True, exist_ok=True)
print(REPORTS_OUT_DIR)

class AbstractReport(ABC):
    def __init__(self, title):
        self._title = title
        self._blocks = ["<h1>HEADER!!!</h1>"]
        self._html = None

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

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

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    {% for block in blocks %}
        {{ block }}
    {% endfor %}
</body>
</html>
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
    report_code = template.render(title=title)
    date = datetime.now().strftime("%Y_%m_%d")
    out_fpath = Path.joinpath(Path(REPORTS_SRC_DIR), f"{date}_{title}.py")
    with open(out_fpath, "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    main()
