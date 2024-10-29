from drf_friend.project.tasks import drf_mail

class SendMailQueue:
    def __init__(self):
        self.email = {
            "delay": 10
        }

    def from_email(self, sender):
        self.email["from"] = sender
        return self

    def to(self, recipients):
        self.email["to"] = recipients if isinstance(recipients, list) else [recipients]
        return self

    def cc(self, cc_recipients):
        self.email["cc"] = cc_recipients if isinstance(cc_recipients, list) else [cc_recipients]
        return self

    def bcc(self, bcc_recipients):
        self.email["bcc"] = bcc_recipients if isinstance(bcc_recipients, list) else [bcc_recipients]
        return self

    def subject(self, subject):
        self.email["subject"] = subject
        return self

    def template(self, template_name, context):
        self.email["template_name"] = template_name
        self.email["context"] = context
        return self

    def attach(self, file_paths):
        self.email.attach_files = file_paths
        return self
    
    def delay(self, the_delay = 2):
        self.email["delay"] = the_delay
        return self

    def send(self):
        """
        Send the email using the configured EmailMessage instance.

        Returns:
            None
        """
        drf_mail.apply_async(args=[self.email], countdown=self.email["delay"])
