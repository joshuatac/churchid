import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

import os
import re
from typing import Literal
import random




def generate_otp(length=6):
    """Generates a random OTP of the given length (default is 6)."""
    otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

        

class MessagingService:
    def __init__(self, email=None, number=None):
        self.email = email
        self.number = number

    def is_valid_email(self):
        """Checks if the provided email is valid."""
        if not self.email:
            raise ValidationError({"email":"Email address is required!"})

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, self.email):
            raise ValidationError({"email": "Invalid email!"})

        return True

    def send_email(self, context, template: Literal["otp","registration", "activation",'verification', 'reset_password'], subject):
        """General method to send an email."""

        if not self.email:
            raise ValidationError({"email":"Email address is required!"})

        try:

            # Render plain text content.
            text_content = render_to_string(f"text/{template}.txt", context)
            
            # Render HTML content.
            html_content = render_to_string(f"html/{template}.html", context)

            # Create a multipart email instance.
            msg = EmailMultiAlternatives(subject, text_content, os.getenv("EMAIL_HOST"), [self.email])

            # Attach HTML content to the email instance and send.
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return {"success": True, "message": "Email sent successfully"}

        except Exception as e:
            raise ValidationError(f"Network Error")

    def send_sms(self, ):
        pass

    def send_otp_email(self):
        """Send an OTP to the user's email."""
        otp = generate_otp()
        context = {"otp": otp}
        self.send_email(context, "otp", "Email Verification")
        return otp


    