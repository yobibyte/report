import unittest

import matplotlib.pyplot as plt

from report import block
from report.base import AbstractReport


class TestBlocks(unittest.TestCase):
    def test_caller_path(self):
        class Report(AbstractReport):
            def load_data(self):
                pass

            def prepare(self):
                plt.plot([1, 2, 3])
                self.add_block(block.Fig(plt.gcf()))

        report = Report("test")
        report.prepare()

        raise NotImplementedError("remove test dir")


if __name__ == "__main__":
    unittest.main()
