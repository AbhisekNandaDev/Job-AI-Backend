import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection

        # Log in to the server
        server.login(login, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        # Close the server connection
        server.quit()





#umay vqlf qxfm xspp
