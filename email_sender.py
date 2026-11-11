import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

env_path = BASE_DIR / ".env"

load_dotenv(env_path, override=True)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Check environment variables
if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
    raise ValueError("Email credentials are missing. Check your .env file.")

# Images folder
image_folder = Path("images")


def send_email(image_path):
    image_path = Path(image_path)

    # Create email
    email_message = EmailMessage()

    email_message["Subject"] = "New customer showed up!"
    email_message["From"] = SENDER_EMAIL
    email_message["To"] = RECEIVER_EMAIL

    email_message.set_content(
        "Hey, we just saw a new customer!"
    )

    # Read image
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    # Attach image
    email_message.add_attachment(
        content,
        maintype="image",
        subtype="png",
        filename=image_path.name
    )

    # Connect to Gmail and send email
    try:
        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as gmail:

            gmail.ehlo()
            gmail.starttls()
            gmail.ehlo()

            gmail.login(SENDER_EMAIL, SENDER_PASSWORD)

            gmail.send_message(email_message)


    except smtplib.SMTPException as error:
        print(f"SMTP error: {error}")

    except OSError as error:
        print(f"Connection error: {error}")


# Main program
if __name__ == "__main__":

    images = list(image_folder.glob("*.png"))

    if not images:
        print("No PNG images found in the images folder.")

    else:
        for image in images:
            send_email(image)
