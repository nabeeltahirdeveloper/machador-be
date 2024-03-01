from application import app
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_swagger import swagger


app=app
start_time = datetime.now()


@app.route("/")
def main():
    elapsed_time = datetime.now() - start_time
    return render_template('index.html', version="1.0", time=elapsed_time)


@app.route("/swagger.json")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Your API Title"
    return jsonify(swag)



if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")