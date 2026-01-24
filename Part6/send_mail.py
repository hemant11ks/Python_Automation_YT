# Import smtplib module to connect and send emails using SMTP protocol
import smtplib

# Import pandas to read and process Excel files
import pandas as pd

# Import os module to read environment variables
import os

# EmailMessage helps to create email (subject, body, attachments, etc.)
from email.message import EmailMessage

# Path is used to safely handle file paths
from pathlib import Path

# load_dotenv loads environment variables from .env file
from dotenv import load_dotenv


# ---------------------------------------------------------
# 1️⃣ LOAD EMAIL CREDENTIALS SECURELY
# ---------------------------------------------------------

# Load variables from .env file into environment
load_dotenv()

# Read sender email from environment variable
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# Read sender email app password from environment variable
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Stop execution if email credentials are missing
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Email credentials missing in .env file")


# ---------------------------------------------------------
# 2️⃣ SMTP CONFIGURATION (GMAIL)
# ---------------------------------------------------------

# Gmail SMTP server address
SMTP_SERVER = "smtp.gmail.com"

# Port 587 is used for secure TLS encrypted connection
SMTP_PORT = 587


# ---------------------------------------------------------
# 3️⃣ EXCEL CONFIGURATION
# ---------------------------------------------------------

# Excel file containing attendance data
EXCEL_FILE = "data.xlsx"

# Sheet name inside the Excel file
SHEET_NAME = "Attendance"

# Minimum required working hours
MIN_WORK_HOURS = 8


# ---------------------------------------------------------
# 4️⃣ READ & FILTER EXCEL DATA
# ---------------------------------------------------------
def read_excel_data():
    """
    Reads Excel file and returns employees
    who worked less than minimum hours
    """

    # Read Excel data into pandas DataFrame
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Filter employees with total hours less than required
    short_hours_df = df[df["Total Hours"] < MIN_WORK_HOURS]

    # Return filtered data
    return short_hours_df


# ---------------------------------------------------------
# 5️⃣ CONVERT DATAFRAME TO HTML TABLE
# ---------------------------------------------------------
def dataframe_to_html(df):
    """
    Converts pandas DataFrame into
    styled HTML table for email body
    """

    # Function to highlight low working hours in red color
    def highlight_hours(value):
        if value < MIN_WORK_HOURS:
            return "color:red;font-weight:bold;"
        return ""

    # Apply styling only on "Total Hours" column
    styled_df = df.style.map(highlight_hours, subset=["Total Hours"])

    # Convert styled DataFrame to HTML format
    return styled_df.to_html(index=False)


# ---------------------------------------------------------
# 6️⃣ SEND EMAIL WITH ATTACHMENT
# ---------------------------------------------------------
def send_email(to, cc, subject, html_body, attachment):
    """
    Sends HTML email with Excel attachment
    """

    # Create EmailMessage object
    msg = EmailMessage()

    # Set sender email address
    msg["From"] = SENDER_EMAIL

    # Set primary recipients (visible in email)
    msg["To"] = ", ".join(to)

    # Set CC recipients (visible in email)
    msg["Cc"] = ", ".join(cc)

    # Set email subject
    msg["Subject"] = subject

    # Plain text fallback if email client does not support HTML
    msg.set_content("Please view this email in HTML format.")

    # Add HTML version of email body
    msg.add_alternative(html_body, subtype="html")

    # -----------------------------------------------------
    # ATTACH EXCEL FILE
    # -----------------------------------------------------

    # Open Excel file in binary mode
    with open(attachment, "rb") as file:
        msg.add_attachment(
            file.read(),                     # Read attachment data
            maintype="application",          # File type
            subtype="octet-stream",          # Generic binary subtype
            filename=Path(attachment).name  # Attachment file name
        )

    # -----------------------------------------------------
    # IMPORTANT SMTP DELIVERY LOGIC
    # -----------------------------------------------------

    # TO and CC headers are only for display in email clients.
    # SMTP does NOT automatically read them to deliver emails.
    #
    # Therefore, we must explicitly combine both TO and CC
    # recipients into a single list so SMTP knows exactly
    # where the email should be delivered.
    #
    # Example:
    # to = ["user@gmail.com"]
    # cc = ["manager@gmail.com"]
    # recipients = ["user@gmail.com", "manager@gmail.com"]

    recipients = to + cc

    # -----------------------------------------------------
    # SMTP CONNECTION & EMAIL SEND
    # -----------------------------------------------------

    # Connect to Gmail SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

        # Start TLS encryption
        server.starttls()

        # Login using Gmail App Password
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email to all combined recipients
        server.send_message(msg, to_addrs=recipients)


# ---------------------------------------------------------
# 7️⃣ MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":

    # Step 1: Read and filter attendance data
    short_hours_df = read_excel_data()

    # Exit if no employee has short hours
    if short_hours_df.empty:
        exit()

    # Step 2: Convert data to HTML table
    html_table = dataframe_to_html(short_hours_df)

    # Step 3: Create HTML email body
    html_body = f"""
    <html>
    <body>
        <h2 style="color:red;">Attendance Alert</h2>
        <p>Employees who worked less than {MIN_WORK_HOURS} hours:</p>
        {html_table}
    </body>
    </html>
    """

    # Step 4: Send email with attachment
    send_email(
        to=["ksingh1617@gmail.com"],
        cc=["ksingh1617@gmail.com"],
        subject="Attendance Report",
        html_body=html_body,
        attachment=EXCEL_FILE
    )
    print("Email sent successfully.")
