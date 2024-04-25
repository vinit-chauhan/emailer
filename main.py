import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('.env')
    return config['DEFAULT']['SENDER_EMAIL'], config['DEFAULT']['SENDER_PASSWORD']


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


subject = "Application for a Part-time Job"


def send_scheduled_email_to(server: smtplib.SMTP, sender_email, receivers, body_text_file, attachment_file, reference=None):

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
        print(f"Email sent to {receiver_email} successfully.")


if __name__ == '__main__':
    sender_email, password = read_config()

    list = [
        {'receiver_email': [""], 'body_file': 'some.txt',
            'attachment_file': 'some.pdf', 'reference': 'Some ref or remove it'},
    ]

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)

            for item in list:
                send_scheduled_email_to(server, sender_email, item['receiver_email'], f"res/body/{item['body_file']}",
                                        f"res/resumes/{item['attachment_file']}", item.get('reference', None))
            server.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
