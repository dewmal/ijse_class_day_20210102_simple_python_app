from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    index_file = open("templates/index.html", "r")
    index_string = index_file.readlines()
    return f"{''.join(index_string)}"


if __name__ == '__main__':
    app.run(port=3232)
