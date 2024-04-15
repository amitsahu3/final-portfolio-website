import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired  # pip install email-validator
import smtplib
from dotenv import load_dotenv, dotenv_values

# setting up enviroment variables for email to use in smtplib
load_dotenv()
my_email = os.environ.get('MY_EMAIL')
my_password = os.environ.get('MY_PASSWORD')
# creating a flask contact form
class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField(label="SEND MESSAGE")

app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)

@app.route('/', methods=['get', 'post'])
def home_page():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        msg = form.message.data

        send_email(name, email, msg)
        return render_template('sent.html')
    form = ContactForm(formdata=None)
    return render_template("index.html", form=form)
def send_email(name, email, msg):

    email_message = f"Subject:New Message\n\nName:{name}\nEmail:{email}\nMessage:{msg}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=email_message)


@app.route('/download')
def download_resume():
    return send_from_directory("../final-portfolio-website/static", 'resume/cheat_sheet.pdf')

@app.route('/download_ml_certificate')
def download_ml_certificate():
    return send_from_directory("../final-portfolio-website/static", 'certificates/machine_learning_certificate.pdf')

@app.route('/download_python_certificate')
def download_python_certificate():
    return send_from_directory("../final-portfolio-website/static", 'certificates/python_bootcamp_certificate.pdf')

if __name__=="__main__":
    app.run(debug=False)







