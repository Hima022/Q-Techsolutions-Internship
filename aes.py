import pandas as pd
from datetime import datetime
import smtplib
import os

# Use environment variables for email credentials
myEmail = "srihima9199@gmail.com"
myPassword = "wrsg grbb ioij dfyo"


# Get today's date
#today = datetime.now()
today = (6,21 )

# Read the CSV file
data = pd.read_csv(r"C:\Users\user\Downloads\dates.csv")

# Create a dictionary with (month, day) as keys
datesDict = {(row["month"], row["day"]): row for _, row in data.iterrows()}

# Check if today matches any date in the CSV
if today in datesDict:
    emailPerson = datesDict[today]
    templatePath = r"C:\Users\user\Downloads\email1.txt"

    # Read the email template
    try:
        with open(templatePath) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", emailPerson["name"])

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=myEmail, password=myPassword)
            connection.sendmail(
                from_addr=myEmail,
                to_addrs=emailPerson["email"],
                msg=f"Subject:Happy Birthday!\n\n{contents}"
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No birthdays today.")
