from report.base import AbstractReport
from report import block


class Report(AbstractReport):

    def load_data(self):
        # No data for this report.
        pass

    def prepare(self):
        self.add_block(block.H1("This is a report example"))
        self.add_block(
            block.Paragraph("Why use Jupyter notebooks when you can use this?!?!?!")
        )


if __name__ == "__main__":
    report = Report(title="text")
    report.generate()
