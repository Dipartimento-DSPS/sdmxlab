from flask import Flask, jsonify, Response
from sdmx_connector import Sdmx_connector
from db import engine
from plot_line import Plot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/<agency_id>/<dataset_id>')
def select_filter(agency_id, dataset_id):
    try:
        sdmx = Sdmx_connector(agency_id, dataset_id)
        return jsonify(sdmx.get_variable_code_label())
    except Exception as e:
        return str(e)


@app.route('/<agency_id>/<dataset_id>/<filter>')
def return_plot_div(agency_id, dataset_id, filter):
    try:
        sdmx = Sdmx_connector(agency_id, dataset_id)
        dataset = sdmx.get_filtered_data(key=sdmx.get_variable_code_test())
        sdmx.save_filtered_data()
        return Plot(dataset).line_time_index_base_100().generate_div_plot()

    except Exception as e:
        return str(e)

app.run(debug=True)