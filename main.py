import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail account details
sender_email = ''
password = ''
message: MIMEMultipart
server: smtplib.SMTP


def read_creds():
    global sender_email, password
    creds = []

    with open('.env', 'r') as env:
        for line in env:
            creds.append(line.split('=')[1][:-1])
    return creds

def init():
    global message, server
    # Create a message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = "Applying for a part-time job"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        creds = read_creds()
        server.login(creds[0], creds[1])
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def send_scheduled_email_to(receiver_email, body_text_file, attachment_file):
    global message
    print('Attempting to send mail to', receiver_email)

    message["To"] = receiver_email
    body = ''
    with open(body_text_file, "r") as file:
        body = file.read()
    message.attach(MIMEText(body, "plain"))

    with open(attachment_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=resume.pdf")

        message.attach(part)

    # Send the email
    try:
        global server
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def done():
    global server
    server.quit()


# Schedule the email to be sent every day at a specific time (24-hour format)
# schedule.every().day.at("08:00").do(send_scheduled_email)

if __name__ == '__main__':
    init()

    send_scheduled_email_to("ADD RECEIVERS HERE", "res/body/company-1.txt", "res/resumes/resume1.pdf")

    done()

# while True:
#     schedule.run_pending()
#     time.sleep(1)
