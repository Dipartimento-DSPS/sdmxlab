from flask import Flask, jsonify, Response, request
from sdmx_connector import Sdmx_connector
from db import engine
from plot_line import Plot
from plot_map import Choroplete
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


@app.route('/<agency_id>/<dataset_id>/filter/line', methods=['POST'])
def return_line_plot_json(agency_id, dataset_id):

    payload = request.json
    print(payload)
    print(type(payload))
    try:
        sdmx = Sdmx_connector(agency_id, dataset_id)
        dataset = sdmx.get_filtered_data(key=payload)
        sdmx.save_filtered_data()
        return jsonify(Plot(dataset).line_time_index_base_100().generate_json_plot())

    except Exception as e:
        return str("line error:") + str(e) +  str(payload)

@app.route('/<agency_id>/<dataset_id>/filter/bar', methods=['POST'])
def return_bar_plot_json(agency_id, dataset_id):
    payload = request.json
    print(payload)
    print(type(payload))
    try:
        sdmx = Sdmx_connector(agency_id, dataset_id)
        dataset = sdmx.get_filtered_data(key=payload)
        sdmx.save_filtered_data()
        return jsonify(Plot(dataset).bar().generate_json_plot())

    except Exception as e:
        return str("bar error:") + str(e) +  str(payload)

@app.route('/<agency_id>/<dataset_id>/filter/map', methods=['POST'])
def return_map_plot_json(agency_id, dataset_id):
    payload = request.json
    print(payload)
    print(type(payload))
    try:
        sdmx = Sdmx_connector(agency_id, dataset_id)
        dataset = sdmx.get_filtered_data(key=payload)
        sdmx.save_filtered_data()
        return jsonify(Choroplete(dataset).load_shape().apply_eurostat().generate_fig().generate_html_map().generate_json_plot())

    except Exception as e:
        return str("map error:") + str(e) +  str(payload)


app.run(debug=True)