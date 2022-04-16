from flask import Flask, request, jsonify

from .process_data import process_data

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'I love overengineering!'

@app.route("/data", methods=["GET"])
def get_data():
    args = request.args
    args = {k: int(v) for k, v in args.items() if v is not None}

    return jsonify(process_data(**args).to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
