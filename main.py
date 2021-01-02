from flask import Flask
from string import Template
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", name="AAA")


@app.route("/_index_file_from_file_read")
def using_file_read():
    index_file = open("templates/index.html", "r")
    index_string = index_file.readlines()
    temp_string = Template(''.join(index_string))
    index_string = temp_string.substitute(name="ABCCC")
    return f"{index_string}"


if __name__ == '__main__':
    app.run(port=3232)
