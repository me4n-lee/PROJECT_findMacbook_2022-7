from urllib.request import urlopen
from bs4 import BeautifulSoup
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
res = urlopen(site + '/kr/shop/refurbished/mac/macbook-pro')
soup = BeautifulSoup(res, 'html.parser')
article_list = soup.select('.rf-refurb-category > div > div > div > ul > li')
issue_body = ''

for row in article_list:
    title = row.select('h3 > a')[0]
    item = " " +  str(title).replace('href="','href="' + site).replace("\n", "").replace('  ', '').strip() + '<br/>\n'
    if 'MacBook Pro' in str(title):
        if '15.4' in str(title):
            issue_body += item
        else:
              print('[filtered] 1', item)
    else: 
        print('[filtered] 2 ', item)

print('———————————————————————————————————')

issue_title = "[리퍼비시] 맥북 15인치이상 리스트 모음(%s)" % (today.strftime("%Y년 %m월 %d일 %H시"))
print(issue_title)
print(issue_body)

GITHUB_TOKEN = os.environ['GIT_TOKEN']
REPO_NAME = "findmacbook"
repo = Github(GIT_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)