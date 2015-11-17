from flask import Flask, render_template
from pymongo import MongoClient
import json
from bson import json_util
import settings as s
import storage
import sqlite3
import uptime
import minmax
import farmer_summary


app = Flask(__name__)


@app.route("/")
def network_data():
    conn = sqlite3.connect('network.db')
    cursor = conn.cursor()

    connection = MongoClient(s.MONGODB_HOST, s.MONGODB_PORT)
    storage_collection = connection[s.DBS_NAME][s.STORAGE_COLLECTION]
    farmers_collection = connection[s.DBS_NAME][s.FARMERS_COLLECTION]

    tb_chart = storage.total_storage_graph(storage_collection)

    farmers_chart = storage.total_farmers_graph(storage_collection)

    avg_gb_farmer = storage.avg_gb_farmer(storage_collection)

    uptime_histogram = uptime.uptime_histogram(cursor, farmers_collection)

    minmax_chart = minmax.minmax_chart(storage_collection)

    avg_uptime = uptime.active_average_uptime(cursor, farmers_collection)

    title = 'Storj Group B Data'
    return render_template('index.html', title=title, line_chart=tb_chart,
                           avg_GB=avg_gb_farmer, farmers_chart=farmers_chart,
                           minmax_chart=minmax_chart,
                           uptime_histogram=uptime_histogram,
                           uptime=avg_uptime)


@app.route("/json")
def daily_data():
    connection = MongoClient(s.MONGODB_HOST, s.MONGODB_PORT)
    storage_collection = connection[s.DBS_NAME][s.STORAGE_COLLECTION]

    totals = storage_collection.find({}, {'_id': False, 'total_TB': True,
                                          'time': True, 'total_farmers': True})
    json_totals = []
    for total in totals:
        if storage.is_noon_time(total['time']):
            json_totals.append(total)
    json_totals = json.dumps(json_totals, default=json_util.default)
    return json_totals


@app.route("/api/summary/<btc_addr>")
def api_summary(btc_addr):
    conn = sqlite3.connect('summary.db')
    cursor = conn.cursor()
    json_summary = farmer_summary.json_month_summary(conn, cursor, btc_addr)
    return json_summary


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
