import re
import imaplib
import getpass
import email
from datetime import datetime
import pandas as pd
import math


account = imaplib.IMAP4_SSL('imap.gmail.com')

#prompt asking for password; pwd not masked
account.login('nandakumar911@gmail.com', getpass.getpass())

account.select(mailbox='INBOX')
    
rv, mailboxes = account.list()
rv, data = account.search(None,"ALL")

sender_list = []

for num in data[0].split():
    rv, data = account.fetch(num, '(RFC822)')
    #fetch email content
    msg_content = email.message_from_string(data[0][1])
    
    #extract date, convert to local date, extract exact name of sender using regex
    #load to frame
    date_tuple = email.utils.parsedate_tz(msg_content['Date'])
    local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
    date_final = datetime.strftime(local_date,'%m-%d-%Y %H:%M:%S')
    sender_list.append([re.sub(r'<.*>','',msg_content['From']),date_final])

df = pd.DataFrame(sender_list,columns = ['Sender','Sent_Date'])
df['Time_diff'] = ''
df['week_num'] = ''

#calculate days elapsed since first day of mailbox creation
#calculate weeks elapsed since first day of mailbox creation
for num in range(len(df)):
    diff = datetime.strptime(df.iloc[num,1],'%m-%d-%Y %H:%M:%S') - datetime.strptime(df.iloc[1,1],'%m-%d-%Y %H:%M:%S')
    df.iloc[num,2] = diff.days
    df.iloc[num,3] = math.floor(diff.days/7)