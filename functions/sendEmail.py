import smtplib
import configparser

class Mailer:

  def __init__(self):      
    # Parse cfg.ini file
    self.config = configparser.ConfigParser()
    self.config.read('./cfg/cfg.ini')

  # Function to email me with anything worth being notified
  def sendMail(self, subject, body):

    recipient = self.config['email']['email_to']
    sender = self.config['email']['email_from']
    password = self.config['email']['email_password']
    message = f"Subject: {subject}\n\n{body}"
    host = self.config['email']['email_host']
    port = self.config['email']['email_port']

    try:
      server = smtplib.SMTP_SSL(host, port)
      server.login(sender, password)
      server.sendmail(sender, recipient, message)
      server.close()
      return True
    
    except Exception as e:
      return e

