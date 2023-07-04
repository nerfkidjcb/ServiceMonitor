import smtplib
import configparser

# Parse cfg.ini file
config = configparser.ConfigParser()
config.read('./cfg/cfg.ini')

# Function to email me with anything worth being notified
def sendMail(subject, body):

  recipient = config['email']['email_to']
  sender = config['email']['email_from']
  password = config['email']['email_password']
  message = f"Subject: {subject}\n\n{body}"
  host= config['email']['email_host']

  server = smtplib.SMTP(host, 587)
  server.starttls()
  server.login(sender, password)
  res = server.sendmail(sender, recipient, message)
  
  if res != {}:
    print(f"Email failed to send. Error: {res}")

  server.quit()

