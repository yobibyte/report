# Report

## What is this all about?

I think [notebooks are harmful](https://yobibyte.github.io/notebooks.html).
They make us lazy and encourage bad practices.
But we still need to do our plotting and data analysis, how can we do it differently?
Meet `report` library.

## Mental model

I want my data reports to leave at the same level as the rest of the code: they should be plain code.
I want my colleagues review them, and double check everything.
I also want to easily share the results of my analysis. 

This results in two main decisions:
- Every data report is a python file that follows a particular flow.
- The output of a data report is a static html page (potentially with other artifacts linked on the page, e.g. images).

## Usage 

```bash
pip install git+https://github.com/yobibyte/report.git
```

You've got a `report` command now, use it to generate a new report:

```bash
report megareport
```

This will generate a python file with the following name: `YYYY_MM_DD_megareport.py` in the `reports_code` folder.
After you've created your report, you can run it to generate a `reports/YYYY_MM_DD_megareport/report.html` folder that you can open in your browser.

You can configure the code and html output folders by creating a `.report` file with the following content:
```bash
[DEFAULT]
REPORTS_SRC_DIR=examples_src
REPORTS_OUT_DIR=examples_reports
```
If you run the `report` command from the folder that has `.report` file, this config will be used. 
Otherwise, if you are in a git repo and you have `.report` in the repo root, this config will be used.
Finally, if none of the above worked, it will check in the home folder for the `.report` file and will use that.
If none of the above worked, the default `reports_code` and `reports` will be used.

You can also add a matplotlib style file that all reports will respect:
```
[DEFAULT]
REPORTS_SRC_DIR=examples_src
REPORTS_OUT_DIR=examples_reports
MATPLOTLIB_STYLE_FPATH=examples_src/plots.mplstyle
```

Here is an example of my style file:
```
figure.titlesize:20
figure.figsize:7.0,4.0
figure.dpi:200
xtick.labelsize:12
ytick.labelsize:12
lines.linewidth:3.0
axes.labelsize:15
legend.fontsize:15
axes.grid:False
image.cmap:Accent
```

## Report's anatomy

Report command generates a file with the following class:
```python
class Report(AbstractReport):
    
    def load_data(self):
        raise NotImplementedError

    def prepare(self):
        raise NotImplementedError

if __name__ == "__main__":
    report = Report(title="test")
    report.generate()
```

You will need to fill that in.
I usually load all the data in the `load_data` function and use it in the `prepare` function.
The mental model is that a report consists of blocks, you add them one by one, and when you run the script, it spits out an html with the blocks
coming in the same order as you added those.

So far, we have header blocks (H1, H2, H3), figure and tables.
I will add more blocks in the future, check out `report/block.py` for more details.

Let's finally generate a report.

```python
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

```

**Beware!** If you run the report file, it will overwrite the output directory and can remove your previous report version. Set locked=True in the constructor to throw an exception when attempting to overwrite.
For day-to-day interactive development, run report file with `DEBUG=true` env variable. This will not overwrite you previous version, and this will remove all the report files at the end. You can test your report this way, check out the standard output, and pdb in it. If you pdb post `report.generate()`, you can inspect the report directory too!

Check out [this link](https://yobibyte.github.io/report/report.html) to see how it looks.

I understand that this is not for everyone, but I find this way of doing data analysis more superior and don't think I lost anything after I stopped using notebooks.
