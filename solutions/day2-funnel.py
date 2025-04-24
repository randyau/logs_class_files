import csv
import gzip

reader = csv.reader(gzip.open('datasets/simulated_web_log.csv.gz','rt'))
next(reader)
funnels = {} # holds [add_to_cart, go_to_checkout, purchase_complete]
for session_id, user_id, ts, event_type, event_name, url in reader:
    if event_name in ['add_to_cart','go_to_checkout','purchase_complete']:
      user_funnel = funnels.setdefault(user_id, [None, None, None])
      if event_name == 'add_to_cart' and user_funnel[0] == None:
          user_funnel[0]=ts
        #we ONLY allow the next event if its timestamp is later than the previous funnel step
      elif event_name == 'go_to_checkout' and user_funnel[0] != None and ts > user_funnel[0]:
          user_funnel[1]=ts
      elif event_name == 'purchase_complete' and user_funnel[1] != None and ts > user_funnel[1]:
          user_funnel[2]=ts

total_users = 0
successful_users = 0
for user_id, user_funnel in funnels.items():
    print(user_id, user_funnel)
    total_users += 1
    if None not in user_funnel:
        successful_users += 1
print("total users: " + str(total_users) + "\nsuccessful_users: " + str(successful_users))

