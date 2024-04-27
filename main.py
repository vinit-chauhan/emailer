import os
import smtplib
import configparser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException

from send_list import send_list, test_list

app = FastAPI()

is_test = False if os.environ.get('TEST') == '0' else True


def read_config():
    config = configparser.ConfigParser()
    config.read('.env')
    return config['DEFAULT']['SENDER_EMAIL'], config['DEFAULT']['SENDER_PASSWORD']


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


subject = "Application for a Part-time Job"


def send_scheduled_email_to(server: smtplib.SMTP, sender_email: str, receivers: list[str], body_text_file: str, attachment_file: str, reference=None):

    for receiver_email in receivers:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["Subject"] = subject if reference is None else subject + \
            " | Reference: " + reference
        message["To"] = receiver_email
        body = read_file(body_text_file)
        message.attach(MIMEText(body, "plain"))

        with open(attachment_file, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            "attachment; filename=resume.pdf")
            message.attach(part)

        server.sendmail(sender_email, receiver_email, message.as_string())

    return receivers


sender_email, password = read_config()
send_list = send_list if not is_test else test_list

server: smtplib.SMTP = None

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

except Exception as e:
    raise (f"An error occurred: {str(e)}")


@app.get('/send')
def send():
    sent_to = []
    try:
        for item in send_list:
            sent_to.extend(send_scheduled_email_to(server, sender_email, item['receiver_email'], f"res/body/{item['body_file']}",
                                                   f"res/resumes/{item['attachment_file']}", item.get('reference', None)))

        return {"Status": "Success", "sent_to": sent_to}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/test')
def test():
    sent_to = []
    try:
        for item in test_list:
            sent_to.extend(send_scheduled_email_to(server, sender_email, item['receiver_email'], f"res/body/{item['body_file']}",
                                                   f"res/resumes/{item['attachment_file']}", item.get('reference', None)))

        return {"Status": "Success", "sent_to": sent_to}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
@app.get('/show-list')
def show_list():
    return send_list
