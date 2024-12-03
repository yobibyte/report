"""Use this to serve your report directory."""

import argparse
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


def serve_app():
    parser = argparse.ArgumentParser(description="Run the Flask app")
    parser.add_argument(
        "--port", type=int, default=4242, help="Port to start the Flask app on"
    )
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port, debug=True)


if __name__ == "__main__":
    serve_app()
