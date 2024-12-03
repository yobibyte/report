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
    <style>
        body {
            font-family: monospace;
            background-color: #f4f4f9;
            padding: 20px;
        }
        table {
            border-collapse: collapse;
            border-spacing: 0;
        }
        th, td {
            border: 1px solid #000;
            padding: 2px 5px;
            text-align: left;
        }
        th {
            font-weight: bold;
        }
        caption {
            margin-bottom: 10px;
            text-align: left;
            font-weight: bold;
        }
    </style>
</head>
<body>
    {% for block in blocks %}
        {{ block }}
    {% endfor %}
</body>
</html>
"""

TABLE_TEMPLATE = """
<p>
<table>
    <caption>{{ caption }}</caption>
    <thead>
        <tr>
            {% for h in header %}
                <th>{{ h }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for r in rows %}
            <tr>
            {% for c in r %}
                <td>{{ c }}</td>
            {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>
</p>
"""

FILE_DIR_TEMPLATE = """
<h1>File explorer</h1>
<ul>
{% for file in files %}
<li>
    <a href="{{ (request.path + '/' if request.path != '/' else '') + file }}">
        {{ (request.path + '/' if request.path != '/' else '') + file }}
    </a>
</li>
{% endfor %}
</ul>
"""
