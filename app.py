from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,request,redirect

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "Toddy.db")}'
db = SQLAlchemy(app)

class Toddy(db.Model):
    Sr = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Handle = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.Sr} - {self.Address}"


def add_toddy_to_db(Address,Password,Handle):
    toddy = Toddy(Address=Address, Password=Password, Handle=Handle)
    db.session.add(toddy)
    db.session.commit()



@app.route('/delete/<int:Sr>')
def delete(Sr):
    toddy = Toddy.query.filter_by(Sr=Sr).first()
    db.session.delete(toddy)
    db.session.commit()
    return redirect('/home')

@app.route('/',methods=['GET','POST'])
def login_page():
    if request.method == "POST":
        render_template('index.html')
    return render_template('login.html')


@app.route('/home',methods = ['GET','POST'])
def home_page():
    if request.method == 'POST':
        if request.form.get("Address"):  # Check if the Address field is present in the form data
            Address = request.form['Address']
            Password = request.form['Password']
            Handle = request.form['Handle']
            add_toddy_to_db(Address,Password,Handle)
            return redirect('/home')
        elif request.form.get("username") and request.form.get("password"):  # Check if the username and password fields are present in the form data
            return redirect('/home') # This line should be replaced with the actual logic for user authentication
    allTodda = Toddy.query.all()
    return render_template('index.html',allTodda = allTodda)

@app.route('/register')
def register_page():
    return render_template('register.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000,debug = True)