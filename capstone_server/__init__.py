from flask import Flask, request, jsonify, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
import csv
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'not-a-secret')


# initiate sqlalchemy
db = SQLAlchemy(app)


class Record(db.Model):
    __tablename__ = 'record'
    __table_args__ = ()

    # meta
    id = db.Column(db.BigInteger, primary_key=True)
    mac_id = db.Column(db.String, index=True, nullable=False)
    date_captured = db.Column(db.DateTime, index=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    # data
    gyro_x = db.Column(db.SmallInteger)
    gyro_y = db.Column(db.SmallInteger)
    gyro_z = db.Column(db.SmallInteger)

    accel_x = db.Column(db.SmallInteger)
    accel_y = db.Column(db.SmallInteger)
    accel_z = db.Column(db.SmallInteger)

    force_1 = db.Column(db.SmallInteger)
    force_2 = db.Column(db.SmallInteger)
    force_3 = db.Column(db.SmallInteger)
    force_4 = db.Column(db.SmallInteger)

    @staticmethod
    def from_csv(mac_id, date_captured, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z,
                 force_1, force_2, force_3, force_4):
        return Record(**locals())


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if file is None or f.filename.split('.')[-1].lower() != 'csv':
            raise BadRequest(description="CSV File Required")

        reader = csv.reader(f, delimiter=',')

        n = 0
        for i, row in enumerate(reader):
            print("row: %s" % (",".join(row),))

            # create record from row
            try:
                r = Record.from_csv(*row)
            except TypeError as e:
                print("CSV Bad Row %s" % "row: %s" % (",".join(row),))
                raise BadRequest(description="CSV Bad Row %s" % "row: %s" % (",".join(row),))
            else:
                db.session.add(r)

            # keep count
            n = i

        db.session.commit()

        return jsonify({"rows": n + 1})
    else:
        return render_template('form.html')


@app.errorhandler(BadRequest)
def bad_request(error):
    return jsonify(error.__dict__, status=400)
