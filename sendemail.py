import smtplib
import socks
#socks.setdefaultproxy(TYPE, ADDR, PORT)
socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, 'http://proxy.cse.cuhk.edu.hk', 8000)
socks.wrapmodule(smtplib)

gmail_user = 'lipenghui315@gmail.com'
gmail_password = 'lipenghui0225'

sent_from = gmail_user
to = ['phli@cse.cuhk.edu.hk', 'phli@link.cuhk.edu.hk', 'lipenghui315@gmail.com', 'pl2689@icloud.com']
subject = 'you received an email for ticket service'
body = 'you might have bought (unpaid) tickets!!'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")
#send_email(gmail_user, gmail_password, to, subject, body)
