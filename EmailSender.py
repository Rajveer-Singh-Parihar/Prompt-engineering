import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import getpass

# EmailSender Class
class EmailSender:
    def __init__(self, smtp_server: str, port: int, email: str, password: str):
        """
        Initialize the EmailSender class.

        Args:
            smtp_server (str): SMTP server address (e.g., smtp.gmail.com)
            port (int): SMTP server port (e.g., 587 for TLS)
            email (str): Sender's email address
            password (str): Sender's email password or app password
        """
        self.smtp_server = smtp_server
        self.port = port
        self.email = email
        self.password = password

    def send_email(self, recipient: str, subject: str, body: str, attachment: str = None):
        """
        Send an email with optional attachment.

        Args:
            recipient (str): Recipient's email address
            subject (str): Email subject
            body (str): Email body content
            attachment (str): Path to the file attachment (default: None)
        """
        try:
            # Initialize the Email Message
            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = recipient
            message["Subject"] = subject

            # Attach the body as plain text
            message.attach(MIMEText(body, "plain"))

            # Handle File Attachment
            if attachment:
                if os.path.isfile(attachment):
                    part = MIMEBase("application", "octet-stream")
                    with open(attachment, "rb") as file:
                        part.set_payload(file.read())

                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                    message.attach(part)
                else:
                    print(f"Warning: Attachment '{attachment}' not found. Skipping attachment.")

            # Connect to SMTP Server and Send Email
            print("\nConnecting to the SMTP server...")
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient, message.as_string())
                print("✅ Email successfully sent to", recipient)

        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication Error: Unable to login. Check your email or password.")
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

# Main Function
def main():
    print("📧 Python Email Sender Application 📧")
    print("------------------------------------")

    # Input SMTP Server Information
    smtp_server = input("Enter SMTP Server (e.g., smtp.gmail.com): ").strip()
    port = int(input("Enter SMTP Port (e.g., 587 for TLS): ").strip())

    # Secure Input for Email and Password
    sender_email = input("Enter Your Email Address: ").strip()
    sender_password = getpass.getpass("Enter Your Email Password (App Password if using Gmail): ")

    # Initialize EmailSender
    email_sender = EmailSender(smtp_server, port, sender_email, sender_password)

    # Email Details
    recipient = input("\nEnter Recipient's Email: ").strip()
    subject = input("Enter Email Subject: ").strip()
    body = input("Enter Email Body: ").strip()
    attachment = input("Enter File Path for Attachment (Press Enter to skip): ").strip()

    # Send Email
    email_sender.send_email(recipient, subject, body, attachment)

if __name__ == "__main__":
    main()
