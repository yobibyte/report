import os

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
            block.Paragraph(
                "We can show tables (and use html tags to make some cells bold)."
            )
        )
        rows = self._iris.data[:20].tolist()
        rows[0] = [
            f"{el}" if el_idx != 2 else f"<b>{el}</b>"
            for el_idx, el in enumerate(rows[0])
        ]
        self.add_block(
            block.Table(
                rows=rows,
                header=self._iris["feature_names"],
                caption="First 20 rows of Iris Dataset",
            )
        )

        self.add_block(block.H3("We can attach images."))
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "code_example.png"
        )
        self.add_block(
            block.Image(
                image_uri=image_path,
                dest_dir=self._report_dir,
                caption="Your ad could be here!",
            )
        )

        self.add_block(
            block.Image(
                image_uri="https://yobibyte.github.io/pics/socrat.png",
                dest_dir=self._report_dir,
                caption="You can also attach images from URLs!",
            )
        )

        # Add a link to the current file to the report.
        self.add_block(block.H3("We can link files."))
        self.add_block(block.File(__file__, self._report_dir))
        self.add_block(
            block.Paragraph(
                "However, you don't have to link the source code, it is <b>automatically</b> added to the report!"
            )
        )


if __name__ == "__main__":
    report = Report(title="megareport")
    report.generate()
