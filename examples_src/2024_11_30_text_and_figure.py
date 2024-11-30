import numpy as np
from matplotlib import pyplot as plt

from report import block
from report.base import AbstractReport


class Report(AbstractReport):

    def load_data(self):
        self._data = np.sin(np.linspace(0, 44 / 7, 100))

    def prepare(self):
        self.add_block(block.H1("We can do figures!"))
        self.add_block(block.Paragraph("Let's plot a sin wave."))
        fig = plt.figure()
        plt.plot(self._data)
        self.add_block(block.Fig(fig, self._report_dir))
        plt.close(fig)


if __name__ == "__main__":
    report = Report(title="text_and_figure")
    report.generate()
