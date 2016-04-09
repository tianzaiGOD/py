from config import DevelopmentConfig
from flask.ext.mail import Message
from flask import render_template
from . import mail


def send_email(to, subject, template, **kwargs):
    msg = Message(DevelopmentConfig.FLASKY_MAIL_SUBJECT_PREFIX .append(subject),
                  sender=DevelopmentConfig.FLASKY_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)





