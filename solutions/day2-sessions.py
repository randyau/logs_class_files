import csv
import datetime
#import dateparser 

my_file = csv.reader(open('../datasets/gardening_blog_log.csv','r'))
sessions = {}
output = []
output.append(["timestamp","user_id","page_url","session_id"])
headers = next(my_file) #skip header line
for timestamp, user, url in my_file:
#    ts = dateparser.parse(timestamp)
    ts  = datetime.datetime.fromisoformat(timestamp)
    user_sessions = sessions.setdefault(user,[ {'session_num':1,'last_evt':ts} ,])
    if user_sessions[-1]['last_evt'] != None \
            and abs((ts - user_sessions[-1]['last_evt']).total_seconds()) > 60*30: #30min session length
        #new session
        user_sessions.append( {'session_num': user_sessions[-1]['session_num']+1 , 'last_evt':ts} )
    else:
        user_sessions[-1]['last_evt'] = ts #update latest timestamp
    session_number = user_sessions[-1]['session_num']
    session_id = str(user) + "s" + f"{session_number:0{5}d}"
    output.append([ts,user,url,session_id])

writer = csv.writer(open('gardening_sessions.csv','w'))
for line in output:
    writer.writerow(line)

                      
