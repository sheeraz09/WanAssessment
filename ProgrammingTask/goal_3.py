import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = 'guess-it'
app.config['FILE_UPLOADS'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


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

def counter(last_name):
    name_as_list = last_name.split(',')
    occurrence = 0

    for name in name_as_list:
        name = name.lower()
        split_name = name.split()

        if split_name[-1] == 'siddique':
            occurrence += 1
            
    return occurrence

print(counter(text_of_file))

if __name__ == '__main__':
    app.run(debug=True)
