from flask import Flask, request
from flask import render_template
from werkzeug.utils import secure_filename
from ml_model import train, test, predict

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/train")
def train_page():
    train()


@app.route("/test")
def test_page():
    test()


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    label = "No input"

    if request.method == "POST":
        if "number" in request.files:
            file = request.files["number"]
            file_name = secure_filename(file.filename)
            file.save(file_name)
            predicted_label = predict(image=file_name)
            label = predicted_label

    return render_template("predict.html", label=label)


@app.route("/")
def index():
    return render_template("index.html", name="AAA")


if __name__ == '__main__':
    app.run(port=3232)
