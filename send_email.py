import argparse
import getpass
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time


from UserInfo import UserInfo

default_recipient = "DEIAtruth@opm.gov"


def set_app_info():
    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    smtp_server = input("Please enter the SMTP server: ")
    smtp_port = input("Please enter the SMTP port: ")
    email = input("Please enter the email address: ")
    password = getpass.getpass("Please enter your app password: ")
    uinf = UserInfo(first, last, email, password, smtp_server, smtp_port)
    uinf.save()

def clear_app_info():
    os.remove("./files/userInfo.txt")

def send_email(subject, body):
    uInfo = UserInfo.load()
    msg = MIMEMultipart()
    msg['From'] = uInfo.email
    msg['To'] = default_recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(uInfo.smtp_server, uInfo.smtp_port)
        server.starttls()
        server.login(uInfo.email, uInfo.app_password)
        text = msg.as_string()
        server.sendmail(uInfo.email, default_recipient, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

def send_email_wrapper(offenders : list[str]):
    
    uInfo = UserInfo.load()
    subject = ""
    # get random subject from _headerOptions.txt
    with open("./files/_headerOptions.txt", "r") as file:
        subjects = file.readlines()
        subject = subjects[random.randint(0, len(subjects) - 1)]

    body = ""
    # get body text from ./files/_boilerplate.txt
    with open("./files/_boilerplate.txt", "r") as file:
        body = file.read()
    
    #replace [offenders] in body with offenders(new line for each)
    offender_txt = ""
    for offender in offenders:
        offender_txt += offender + "\n"

    body = body.replace("[offenders]", offender_txt + "\n")

    my_name = uInfo.first_name + " " + uInfo.last_name

    body = body.replace("[my_name]", my_name)

    body= body.replace("[my_email]", uInfo.email)

    #send email
    send_email(subject, body)
    

def get_random_first_last_name() -> tuple[str, str]:
    first = ""
    last = ""
    with open("./files/first_names.txt", "r") as file:
        first_names = file.readlines()
        first = first_names[random.randint(0, len(first_names) - 1)].strip()
    with open("./files/last_names.txt", "r") as file:
        last_names = file.readlines()
        last = last_names[random.randint(0, len(last_names) - 1)].strip()

    first = first.lower()
    last = last.lower()
    first = first[0].upper() + first[1:]
    last = last[0].upper() + last[1:]
    return first, last

# TESTING, do not use in production
def test_multiple_emails(num_emails, frequency):
    email_count = 0
    while(email_count < num_emails):
        # send_email(f"test email {email_count}", "blah blah blah", recipient)
        first_last = get_random_first_last_name()
        send_email_wrapper ([first_last[0] + " " + first_last[1]])
        time.sleep(frequency)
        email_count += 1

def send_offenders_to_email():
    offenders = []
    with open("./files/offenders.txt", "r") as file:
        offenders = file.readlines()
    send_email_wrapper(offenders)

def getCmdArgs():
    """
    Parses the command-line arguments and returns the parsed arguments.

    Returns:
        args (argparse.Namespace): The parsed command-line arguments.
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Automates the process of reporting employees who removed DEI roles from their job description.')

    
    # THIS IS FOR TESTING ONLY, FAMILIARIZE YOURSELF WITH THE CAN-SPAM-ACT BEFORE USING THIS
    parser.add_argument('-t', '--testingFlag', type=bool, default=False, help='Switches from reading from the offenders file to reading from first and last name files. DONT EVEN THINK ABOUT SETTING THIS TO TRUE.')
    parser.add_argument('-c', '--count', type=int, default=20, help='TESTING ONLY: The number of emails to send to the recipient')
    parser.add_argument('-f', '--frequency', type=int, default=20, help='TESTING ONLY: The frequency of emails sent to the recipient (in seconds)')

    parser.add_argument('-s', '--set', type=bool, default=False, help='Set the app information')
    # Parse the command-line arguments
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = getCmdArgs()
    uInfo = UserInfo.load()
    if(uInfo == None or args.set):
        set_app_info()
    if(args.testingFlag):
        if(args.count == None or args.frequency == None):
            print("You must specify the count and frequency when using the testing flag")
            exit(1)
        confirm = input(f"YOU ARE IN A TESTING STATE, Are you sure you want to send emails to the recipient? It will send {args.count} emails, at a rate of 1 email every {args.frequency} seconds (y/n): ")
        if(confirm == "y"):
            test_multiple_emails(args.count, args.frequency)
        else:
            print("Aborting")
            exit(1)
    send_offenders_to_email()
