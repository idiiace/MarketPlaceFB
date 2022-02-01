import smtplib, ssl
import hashlib as hs

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = ''


# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = ''

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)


me = 'lfbnotifierbot@gmail.com'


def send_email(message):
    sender_email = 'lfbnotifierbot@gmail.com'
    password = ''


    to = []


    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    #sender_email = "my@gmail.com"
    #password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.connect('smtp.gmail.com', '587')
        #server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        
        #server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to, message)

        
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

def trigger(subject,message):
    ms = hs.md5(str(message).encode()).hexdigest()
    send = True
    try:
        df=open('hashes.txt').read()
        for i in df.splitlines():
            if ms in i:
                send=False
    except:
        pass
    
    message = 'Subject: {}\n\n{}'.format('New AD Found : '+str(subject), message)
    send_email(message)
    open('hashes.txt','a').write(ms)
    open('hashes.txt','a').write('\n')
    return True
