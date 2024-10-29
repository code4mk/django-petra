from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from drf_friend.mailer.inline_css import inline_css

class SendMail:
    """
    A utility class for sending emails using Django's EmailMessage.

    Usage:
    mail = SendMail()
    mail.from_email("sender@example.com").to(["recipient@example.com"]).subject("Subject").html_body("<p>HTML Content</p>").send()
    """

    def __init__(self):
        """
        Initialize the SendMail object with an EmailMessage instance.
        """
        self.email = EmailMultiAlternatives()

    def from_email(self, sender):
        """
        Set the sender email address.

        Args:
            sender (str): The email address of the sender.

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.from_email = sender
        return self

    def to(self, recipients):
        """
        Set the recipient email addresses.

        Args:
            recipients (str or list): The email address or list of email addresses of the recipients.

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.to = recipients if isinstance(recipients, list) else [recipients]
        return self

    def cc(self, cc_recipients):
        """
        Set the carbon copy (cc) recipient email addresses.

        Args:
            cc_recipients (str or list): The email address or list of email addresses of the cc recipients.

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.cc = cc_recipients if isinstance(cc_recipients, list) else [cc_recipients]
        return self

    def bcc(self, bcc_recipients):
        """
        Set the blind carbon copy (bcc) recipient email addresses.

        Args:
            bcc_recipients (str or list): The email address or list of email addresses of the bcc recipients.

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.bcc = bcc_recipients if isinstance(bcc_recipients, list) else [bcc_recipients]
        return self

    def subject(self, subject):
        """
        Set the email subject.

        Args:
            subject (str): The subject of the email.

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.subject = subject
        return self

    def body(self, body, content_type='text/plain'):
        """
        Set the email body.

        Args:
            body (str): The body content of the email.
            content_type (str): The content type of the email body (default is 'text/plain').

        Returns:
            SendMail: The current SendMail instance.
        """
        self.email.attach_alternative(body, content_type)
        return self

    def html_body(self, html_body):
        """
        Set the email body as HTML content.

        Args:
            html_body (str): The HTML content of the email body.

        Returns:
            SendMail: The current SendMail instance.
        """
        return self.body(html_body, content_type='text/html')

    def template(self, template_name, context):
        """
        Set the email body using a Django template.

        Args:
            template_name (str): The name of the template file (without extension).
            context (dict): The context data to render the template.

        Returns:
            SendMail: The current SendMail instance.
        """
        html_body = inline_css(render_to_string(f"mail/{template_name}.html", context))
        return self.html_body(html_body)

    def attach(self, file_paths):
        """
        Attach files to the email.

        Args:
            file_paths (list): List of file paths to be attached.

        Returns:
            SendMail: The current SendMail instance.
        """
        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                self.email.attach(file.name, file.read())
        return self

    def attach_image(self, image_path):
        """
        Attach an image to the email as an inline image.

        Args:
            image_path (str): The path to the image file.

        Returns:
            SendMail: The current SendMail instance.
        """
        with open(image_path, 'rb') as image:
            img = MIMEImage(image.read())
            img.add_header('Content-ID', '<{}>'.format(image.name))
            self.email.attach(img)
        return self

    def send(self):
        """
        Send the email using the configured EmailMessage instance.

        Returns:
            None
        """
        
        self.email.send()
