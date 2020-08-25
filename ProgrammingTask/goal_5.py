from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return self.text


db.create_all()


@app.route('/')
def todolist():
    incomplete = Todolist.query.filter_by(complete=False).all()
    complete = Todolist.query.filter_by(complete=True).all()

    return render_template('todolist.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todolist(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todolist'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todolist.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todolist'))


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    todo = Todolist.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('todolist'))


if __name__ == '__main__':
    app.run(debug=True)
