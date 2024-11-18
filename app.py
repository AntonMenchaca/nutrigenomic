from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "pinging api for nutrigenomic!"})

@app.route('/api/v1/resource')
def resource():
    return jsonify({"data": "This is an example resource."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
