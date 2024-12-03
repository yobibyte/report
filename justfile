lint:
  black {{justfile_directory()}}
  isort {{justfile_directory()}}

serve:
  FLASK_APP={{justfile_directory()}}/report/app.py flask run  --port=4242 --host=0.0.0.0

