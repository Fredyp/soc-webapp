from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import pdfkit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soc.db'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)
db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    reports = db.relationship('Report', backref='client', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@app.route('/create_client', methods=['POST'])
def create_client():
    name = request.form['name']
    email = request.form['email']
    client = Client(name=name, email=email)
    db.session.add(client)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_report/<int:client_id>', methods=['GET', 'POST'])
def create_report(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        report = Report(title=title, content=content, client=client)
        db.session.add(report)
        db.session.commit()

        rendered = render_template('report_template.html', title=title, content=content)
        pdf_path = f'tmp/report_{report.id}.pdf'
        os.makedirs('tmp', exist_ok=True)
        pdfkit.from_string(rendered, pdf_path)

        msg = Message(subject=f"SOC Report: {title}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[client.email])
        msg.body = f"Please find attached the report: {title}"
        with app.open_resource(pdf_path) as fp:
            msg.attach(f"report_{report.id}.pdf", "application/pdf", fp.read())
        mail.send(msg)
        os.remove(pdf_path)
        return redirect(url_for('index'))
    return render_template('create_report.html', client=client)

@app.route('/report_log/<int:client_id>')
def report_log(client_id):
    client = Client.query.get_or_404(client_id)
    reports = Report.query.filter_by(client_id=client_id).all()
    return render_template('report_log.html', client=client, reports=reports)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)