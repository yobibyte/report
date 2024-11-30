REPORT_TEMPLATE = """from report import block
from report.base import AbstractReport


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
