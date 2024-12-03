"""Use this to serve your report directory."""

import os

from flask import Flask, abort, render_template_string, send_file

from report.template import FILE_DIR_TEMPLATE
from report.util import get_src_out_dirs

app = Flask(__name__)

_, BASE_DIR = get_src_out_dirs()


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def show_directory(req_path):

    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        print("here")
        return send_file(abs_path)

    files = os.listdir(abs_path)
    return render_template_string(FILE_DIR_TEMPLATE, files=files)


if __name__ == "__main__":
    app.run()
