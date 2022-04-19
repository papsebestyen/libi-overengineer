from flask import Flask, jsonify, request

from .process_data import get_query_data, get_raw_data, get_simplicity_data

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "I love overengineering!"


@app.route("/query_data", methods=["GET"])
def get_query():
    args = request.args
    year = args.get("year", default=None, type=int)
    month = args.get("month", default=None, type=int)
    day = args.get("day", default=None, type=int)
    day_delta = args.get("day_delta", default=365, type=int)
    group_hours = args.get("group_hours", default=1, type=int)

    df = get_raw_data(year=year, month=month, day=day)
    return jsonify(
        get_query_data(
            df, day_delta=day_delta, group_hours=group_hours
        ).to_dict(orient="records")
    )


@app.route("/simplicity_data", methods=["GET"])
def get_simplicity():
    args = request.args
    year = args.get("year", default=None, type=int)
    month = args.get("month", default=None, type=int)
    day = args.get("day", default=None, type=int)
    day_delta = args.get("day_delta", default=365, type=int)
    group_hours = args.get("group_hours", default=1, type=int)
    with_prediction = args.get("with_prediction", default=False, type=bool)

    df = get_raw_data(year=year, month=month, day=day)
    return jsonify(
        get_simplicity_data(
            df,
            day_delta=day_delta,
            group_hours=group_hours,
            with_prediction=with_prediction,
        ).to_dict(orient="records")
    )


if __name__ == "__main__":
    app.run(debug=True)
