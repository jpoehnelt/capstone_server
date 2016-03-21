from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import BadRequest
import csv
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'not-a-secret')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if file is None or f.filename.split('.')[-1].lower() != 'csv':
            raise BadRequest(description="CSV File Required")

        reader = csv.reader(f, delimiter=',')
        n = 0
        for i, row in enumerate(reader):
            print(",".join(row))
            n = i

        return jsonify({"rows": n})
    else:
        return render_template('form.html')


@app.errorhandler(BadRequest)
def bad_request(error):
    return jsonify(error.__dict__, status=400)