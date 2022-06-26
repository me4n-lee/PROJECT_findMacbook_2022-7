from urllib.request import urlopen
from bs4 import BeautifulSoup
from github import Github, Issue
import datetime
from pytz import timezone
from dateutil.parser import parse
import os

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
    published_at = row.select('div.date-created span.timeago')[0].get_text()
    item = " " +  str(title).replace('href="','href="' + site).replace("\n", "").replace('  ', '').strip() + '<br/>\n'
    if '15.4형 MacBook Pro' in str(title) or '16형 MacBook Pro' in str(title) :
        issue_body += item
    else: 
        print('[filtered] 2 ', item)

print('———————————————————————————————————')

issue_title = "[리퍼비시] 맥북 15인치이상 리스트 모음(%s)" % (today.strftime("%Y년 %m월 %d일 %H시"))
print(issue_title)
print(issue_body)

GITHUB_TOKEN = os.environ['GIT_TOKEN']
REPO_NAME = "me4n-findmacbook"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)