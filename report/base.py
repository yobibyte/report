from abc import ABC, abstractmethod
from jinja2 import Template
import argparse
from datetime import datetime
import re


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
    with open(f"{date}_{title}.py", "w") as f:
        f.write(report_code)


if __name__ == "__main__":
    main()
