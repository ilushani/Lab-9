from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/Lab_9'
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(256), nullable=False)
    def __init__(self, company, term):
        self.company_name = company.strip()
        self.term = [
            Term(duration=int(t)) for t in term.split(',')
        ]

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('term'))

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('main.html', companies=Company.query.all())


@app.route("/main", methods=['GET'])
def main():

    return render_template('main.html', companies=Company.query.all())


@app.route('/add_experience', methods=['POST'])
def add_experience():
    company = request.form['company']
    term = request.form['term']

    db.session.add(Company(company, term))
    db.session.commit()

    return redirect(url_for('main'))
@app.route('/clear_db', methods=['POST'])
def clear_db():
    db.session.query(Term).delete()
    db.session.query(Company).delete()
    db.session.commit()
    return redirect(url_for('main'))