import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailSender:
    def __init__(self, sender_address, sender_name, smtp_server='your_smtop_server', smtp_port=25, use_tls=False):
        self.sender_address = sender_address
        self.sender_name = sender_name
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_tls = use_tls  # Whether to use STARTTLS

    def send_email(self, to, cc, subject, content, file_paths=None, is_html=False):
        message = MIMEMultipart()
        message['From'] = f"{self.sender_name} <{self.sender_address}>"
        message['To'] = ', '.join(to)
        message['Cc'] = ', '.join(cc)
        message['Subject'] = subject

        # Determine the content type (HTML or plain text)
        message.attach(MIMEText(content, 'html' if is_html else 'plain'))

        # Attach files if provided
        if file_paths:
            for file_path in file_paths: 
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
                    message.attach(part)

        # Create SMTP session for sending the mail
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as session:
            session.ehlo()  # Identify ourselves to the smtp server
            if self.use_tls:
                session.starttls()  # Secure the SMTP connection
                session.ehlo()  # Re-identify ourselves as an encrypted connection
            # Note: If your SMTP server requires authentication, add it here
            session.sendmail(self.sender_address, to + cc, message.as_string())

        print("Mail Sent")
