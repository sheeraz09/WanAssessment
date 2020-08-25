import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'guess-it'
app.config['FILE_UPLOADS'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)

        if file.filename != "":

            extension = os.path.splitext(filename)[1]
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                abort(400)

            file.save(os.path.join(app.config['FILE_UPLOADS'], filename))

            print('File saved')
        return redirect(url_for('upload'))

    return render_template('upload.html')


with open("static/uploads/mock.txt", "r") as f:
    text_of_file = f.read()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

db.create_all()

def add_name(full_name):
    names_as_list = full_name.split(',')
    for i in names_as_list:
        j = User(username = i)
        db.session.add(j)
        db.session.commit()
    return j

add_name(text_of_file)

if __name__ == '__main__':
    app.run(debug=True)
