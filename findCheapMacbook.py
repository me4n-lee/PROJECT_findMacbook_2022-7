from urllib.request import urlopen
from bs4 import BeautifulSoup
from github import Github, Issue
import datetime
from pytz import timezone
from dateutil.parser import parse
import os
import requests as rq
from noti import send
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 이메일 로그인 계정 입력
sender = os.environ['EMAIL_SENDER']  #"me4n.send.only@gmail.com" #str(input('이메일 : '))
password = os.environ['EMAIL_PASSWORD'] #str(input('비밀번호 : '))
# 수신자 이메일 입력
receiver = os.environ['EMAIL_RECEIVER'] #"mobius.in@mobius96.com" #str(input('수신자 이메일 : '))

def smtp_setting(gmail, email, password):
  mail_type = None
  #port = 587
  port = 465

  if type == 'naver':
    mail_type = 'smtp.naver.com'
  elif type == 'gmail':
    mail_type = 'smtp.gmail.com'
  else:
    mail_type = 'smtp.gmail.com'
    
  # SMTP 세션 생성
  #smtp = smtplib.SMTP(mail_type, port)
  smtp = smtplib.SMTP_SSL(mail_type, port)
  smtp.set_debuglevel(True)

  # SMTP 계정 인증 설정
  smtp.ehlo()
  #smtp.starttls() # TLS 사용시 호출
  smtp.login(email, password) # 로그인

  return smtp

def send_multipart_mail(sender, receiver, email, password, subject, content):
  try:
    # SMTP 세션 생성
    smtp = smtp_setting('gmail', email, password)

    # 이메일 데이터 설정
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender  # 송신자
    msg['To'] = receiver  # 수신자
    #msg['To'] = ",".join(receiver)    # 여러명의 수신자일 경우

    # 일반 텍스트 형식의 문자열
    part1 = MIMEText(content['plain'], 'plain')
    # HTML 형식의 문자열
    part2 = MIMEText(content['html'], 'html')

    msg.attach(part1)
    msg.attach(part2)

    # 메일 전송
    smtp.sendmail(sender, receiver.split(","), msg.as_string())
    #smtp.sendmail(sender, receiver, msg.as_string())
  except Exception as e:
    print('error', e)
  finally:
    if smtp is not None:
      smtp.quit()

KST = timezone('Asia/Seoul')
today = datetime.datetime.now(KST)

def isDateInRange(created_at):
    suffix_KST = '.000001+09:00'
    created_at = parse(created_at + suffix_KST)
    yesterday = today - datetime.timedelta(1)
    return today > created_at and created_at > yesterday

site = 'https://www.apple.com/'
res = urlopen(site + '/kr/shop/refurbished/mac/15%ED%98%95-16%ED%98%95-macbook-pro')
soup = BeautifulSoup(res, 'html.parser')
article_list = soup.select('.rf-refurb-category > div > div > div > ul > li')
issue_body = ''

for row in article_list:
    title = row.select('h3 > a')[0]
    item = " " +  str(title).replace('href="','href="' + site).replace("\n", "").replace('  ', '').strip() + '<br/>\n'
    if '15.4형 MacBook Pro' in str(title) or '16형 MacBook Pro' in str(title) :
        issue_body += item
    else: 
        print('[filtered] 2 ', item)

print('———————————————————————————————————')

issue_title = "[리퍼비시] 맥북 15인치이상 리스트 모음(%s)" % (today.strftime("%Y년 %m월 %d일 %H시"))
print(issue_title)
print(issue_body)

if issue_body != '':
    send(issue_title + '\n' + issue_body)

if issue_body != '':
    send_multipart_mail(sender, receiver, sender, password,  issue_title, {'plain': issue_body1, 'html': issue_body2})

GITHUB_TOKEN = os.environ['GIT_TOKEN']
REPO_NAME = "me4n-findmacbook"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)