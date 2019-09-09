# Dash
Repository of DASH data viz apps

## Structure

The directory `viz` contains the source code.

- `app.py`: Global configuration
- `models/*.py`: Each file represents the model as python module. For example, the economic.py is the models.economic and it represents the economic model.
- `index.py`: Imports the module and expose it as a path on the webserver. For example, the module models.economic is exposed as /economic.
- `assets/`: The assets director for static files.
