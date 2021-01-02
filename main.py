from flask import Flask, request
from string import Template
from flask import render_template
from nic_parser.parser import Parser

app = Flask(__name__)


class User:

    def __init__(self, name, nic):
        self.nic = nic
        self.name = name
        self.dob = Parser(f"{nic}").birth_date
        self.gender = Parser(f"{nic}").gender


user_list = []


@app.route("/insert_user", methods=["get", "post"])
def insert_user_data():
    print("insert_user_data_method")
    name = ""
    print(request.method)
    if request.method == "POST":
        print("inside the post filter")
        name = request.form.get("user_name")
        nic = request.form.get("nic")
        user_list.append(User(name=name, nic=nic))

    return render_template("user_data.html", user_list=user_list)


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
