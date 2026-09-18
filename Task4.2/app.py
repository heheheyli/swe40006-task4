from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>SWE40006 Task 4.2</h1><p>Dockerised Flask App! By Hayley~</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    