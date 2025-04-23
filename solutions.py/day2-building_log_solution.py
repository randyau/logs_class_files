import csv

my_file = csv.reader(open('building_entry_log.csv','r'), delimiter=' ')
user_log = {} # will store user:[ {'enter':time, 'exit':time} ] 

for line in my_file: #assume file is sorted in chronological order
  time, username, action = line
  user_data = user_log.setdefault(username, [ {'enter':None, 'exit':None} ]) #initialize with first empty pair
  if action == 'enters': # if we see enter, update latest data pt w/ enter timestamp, overwrite old one if one exists (ignoring double entries by taking latest one)
    user_data[-1]['enter'] = time
  if action == 'exits': 
    if user_data[-1]['enter'] != None: # there’s an unmatched ‘enter’ waiting
      user_data[-1]['exit'] = time
      user_data.append( {'enter':None, 'exit':None} ) #append a new object
    else: # unpaired exit event, ignore
      continue #move to next iteration

for username, entrylist in user_log.items():
    if entrylist[-1]['enter'] == None or entrylist[-1]['exit'] == None:
        entrylist.pop(-1)
    print (len(entrylist), username)

