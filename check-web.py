#!/usr/local/bin/python3
import smtplib
import socks

def send_email(user, pwd, recipient, subject, body):

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.yeah.net", 25)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
        return True
    except Exception as e:
        print ("failed to send mail", e)
        return False

from urllib.parse import quote
from urllib.request import urlopen, Request
from os.path import join, exists
from difflib import SequenceMatcher, unified_diff
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def check_web(url, data_dir):
    try:
        req = Request(url=url, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        req.add_header('Referer', url)
        with urlopen(req) as fp:
            new_content = fp.read().decode('utf-8')
            filePath = join(data_dir, quote(url, safe=''))
            diff = False
            similar_score = 1.0

            if not exists(filePath):
                old_content = ""
                # check a new website, we do not append the diff
            else:
                with open(filePath, 'r') as data_fp:
                    old_content = data_fp.read()
                    similar_score = similarity(new_content, old_content)
                    if similar_score < 0.97:
                        diff = "\n".join(list(unified_diff(old_content.split('\n'), new_content.split('\n'))))
            with open(filePath, 'w') as data_fp:
                # write latest version
                data_fp.write(new_content)
            return diff, similar_score
    except Exception as e:
        print(e)
        pass

    return False, -1


from datetime import datetime, date
import pathlib


if __name__ == "__main__":
    fileDir = pathlib.Path(__file__).parent.resolve()
    data_dir = join(fileDir, "web-cache")
    with open(join(fileDir, 'urls.txt'), 'r') as fp:
        urls = [i.strip() for i in fp.readlines() if not i.startswith('#')]
    diffs = []
    updatedUrls = []
    similar_scores = []
    summary = ""
    for url in urls:
        diff, score = check_web(url, data_dir)
        summary += url + ": " + str(score) + "\n"
        similar_scores.append(score)
        print('check %s, updated? %s, %f'% (url, 'False' if diff == False else 'True', score))
        if diff:
            diffs.append(diff)
            updatedUrls.append(url)

    content = "=====UPDATES ON=====\n" + "\t".join(updatedUrls) + "\n=====DETAILS=====\n".join(diffs)
    if len(updatedUrls) > 0:
        _user = 'sender@xxx.com'
        _password = 'sender_password'

        to = ['recipient@xxx.com']
        subject = 'Web Service Sync'
        ret = send_email(_user, _password, to, subject, content.encode('utf-8'))

    if not exists(join(data_dir, 'web-check.log')):
        open(join(data_dir, 'web-check.log'), 'w').close()
    with open(join(data_dir, 'web-check.log'), 'r+') as fp:
        today = date.today()
        old_content = fp.read()
        fp.seek(0)
        fp.write("\n-------%s------\n" % today.strftime("%d/%m/%Y"))
        fp.write(summary)
        fp.write("======\n")
        fp.write(content)
        fp.write(old_content)
