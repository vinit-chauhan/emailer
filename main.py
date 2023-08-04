import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail account details
sender_email = ""
password = ""

# Create a message
message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = "Applying for a part-time job"

global server
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
except Exception as e:
    print(f"An error occurred: {str(e)}")


def send_scheduled_email_to(receiver_email, body_text_file, attachment_file):
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
        part.add_header("Content-Disposition", f"attachment; filename=resume.pdf")

        message.attach(part)

    # Send the email
    try:
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Schedule the email to be sent every day at a specific time (24-hour format)
# schedule.every().day.at("08:00").do(send_scheduled_email)

if __name__ == '__main__':
    receiver = ""
    send_scheduled_email_to(receiver, "res/body/company-1.txt", "res/resumes/resume1.pdf")
    server.quit()

# while True:
#     schedule.run_pending()
#     time.sleep(1)
