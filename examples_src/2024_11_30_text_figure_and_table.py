import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris

from report import block
from report.base import AbstractReport


class Report(AbstractReport):

    def load_data(self):
        self._fig_data = np.sin(np.linspace(0, 44 / 7, 100))
        self._iris = load_iris()

    def prepare(self):
        self.add_block(block.H1("We can do figures!"))

        self.add_block(block.Paragraph("Let's plot a sin wave."))
        fig = plt.figure()
        plt.plot(self._fig_data)
        self.add_block(block.Fig(fig, self._report_dir))
        plt.close(fig)

        # let's take first 20 rows
        self.add_block(
            block.Table(
                rows=self._iris.data[:20],
                header=self._iris["feature_names"],
                caption="First 20 rows of Iris Dataset",
            )
        )


if __name__ == "__main__":
    report = Report(title="text_figure_and_table")
    report.generate()
