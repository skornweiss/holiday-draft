from __future__ import division

holidays = ["Thanksgiving", "Christmas", "New Years"]
holidays_nospace = map(lambda x: x.replace(' ', '_'), holidays)
number_working = 15


import csv
import os
import copy
print(os.getcwd())


randomized_csv = open('random.csv')
selection_csv = open('holiday.csv')

randomized = csv.DictReader(randomized_csv)
selections = csv.DictReader(selection_csv)

#eliminate duplicate selection submissions and retain the most recent
#at the same time, pair the rankings with a full name and a rank number

rand_dict = {}
for x in randomized:
    fname = x['First Name']
    lname = x['Last Name']
    fullname = (fname.strip() + ' ' + lname.strip()).lower()
    #print(fullname)
    rank = eval(x['Rank'])
    rand_dict[rank] = fullname

print(rand_dict, len(rand_dict))

# calculate the number of people who can be off for a single holiday
number_off = len(rand_dict) - number_working

# create blank lists that will hold lists of names of people off for each holiday and add them to a list of lists called holiday_lists
holiday_lists = []
for x in holidays_nospace:
    exec("{0} = []".format(x.replace(' ', '_')))
    exec("holiday_lists.append({0})".format(x))

# have to put something in here to eliminate duplicates
#for x in selections:

ranks = {}
for x in selections:
    fname = x['First Name']
    lname = x['Last Name']
    fullname = (fname.strip() + ' ' + lname.strip()).lower()
    #print(fullname)
    ranks[fullname] = {}
    for y in holidays:
        ranks[fullname][int(x[y])] = y

ranks_copy = copy.deepcopy(ranks)


tracker_list = rand_dict.keys()
index = -1
rank_tracker = tracker_list[index]
direction = 'pos'
while tracker_list:
    if direction == 'pos' and index < len(tracker_list)-1:
        index += 1
    elif direction == 'pos' and index >= len(tracker_list) -1:
        direction = 'neg'
        #index -= 1
    elif direction == 'neg' and index > 0:
        index -= 1
    elif direction == 'neg' and index == 0:
        direction = 'pos'
        index += 1
    rank_tracker = tracker_list[index]
    #print(rank_tracker, direction)
        
    # get the drafter if they exist
    if rand_dict.has_key(rank_tracker):
        drafter = rand_dict[rank_tracker]
    # if they don't exist, go to the next one
    else:
        continue

    # get the drafter's picks if they exist
    if ranks.has_key(drafter):
        picks = ranks[drafter]
    # if they don't exist, continue - for now do not remove this person from the draft and go to the next person
    else:
        #try:
            #a = tracker_list.pop(index)
            #print(a, rand_dict[a])
            #print(len(rand_dict))
            #print(a)
        #except:
        #    pass
        continue

    # try to give the drafter their top pick and if that pick is full, go to the next one
    choice_counter = 1
    top_choice = False
    while ranks[drafter]:
        # check to see if the pick exists and if it does, use it as the top choice
        if ranks[drafter].has_key(choice_counter):
            top_choice = ranks[drafter].pop(choice_counter).replace(' ', '_')
        # if it doesn't, go to the next one
        else:
            choice_counter += 1
            continue

        # check to see if the holiday is open, if it is, give this person their choice and go to the next person
        if len(eval(top_choice.replace(' ', '_'))) < number_off:
            exec("{0}.append(drafter)".format(top_choice))
            #print(rank_tracker, drafter, top_choice)
            break
        # if it's not available, go to the next choice
        else:
            #print("Not available", rank_tracker, drafter, top_choice)
            choice_counter += 1


    # check to see if all holidays are full and if they are, quit the draft
    if not filter(lambda x: len(x)<number_off, holiday_lists):
        print('filled')
        break
    #print(drafter, top_choice)


wfile = open('holiday_schedule_off.csv', 'w')
outputlist = []
for x in holidays_nospace:
    hlist = eval(x)
    hlist.reverse()
    hlist.append(x)
    hlist.reverse()
    hlist = map(lambda x: x.title(), hlist)
    outputlist.append(hlist)
    #print(x, len(hlist), hlist)

outputlist = map(list, zip(*outputlist))
writer = csv.writer(wfile)
for x in outputlist:
    writer.writerow(x)
    

wfile.close()


# statistics
off_list = []
on_list = []
got_first_choice = []
got_second_choice = []
for x in rand_dict.values():
    count = 0
    cur_list_off = [x,]
    cur_list_on = [x,]
    for y in holidays:
        hlist = eval(y.replace(' ', '_'))
        #print(x, hlist.count(x))
        count += hlist.count(x)
        #print(ranks_copy[x][1], hlist.count(x))
        if ranks_copy[x][1] == y and hlist.count(x):
            got_first_choice.append(x)
        if ranks_copy[x][2] == y and hlist.count(x):
            got_second_choice.append(x)
        if hlist.count(x):
            cur_list_off.append(y)
        else:
            cur_list_on.append(y)
            
    #print(x, count)
    off_list.append(cur_list_off)
    on_list.append(cur_list_on)

print("first", got_first_choice)
print("second", got_second_choice)
#print(len(got_first_choice))
#print(len(got_second_choice))
got_both_1and2 = set(got_first_choice).intersection(set(got_second_choice))
print(got_both_1and2)
print(len(rand_dict.values()))
percent_first = (len(got_first_choice)/len(rand_dict.values()))*100
percent_first_and_second = (len(got_both_1and2)/len(rand_dict.values()))*100
print("% 1st", percent_first)
print("% 1st and 2nd", percent_first_and_second)

on_schedule = []
for x in holidays_nospace:
    cur_list = []
    exec("a = set({0})".format(x))
    exec("{0}on = set([y.lower() for y in rand_dict.values()]).difference(a)".format(x))
    cur_list.append(x)
    cur_list.extend(list(eval("{0}on".format(x))))
    on_schedule.append(cur_list)
#print(on_schedule)
wfile = open('holiday_schedule_on.csv', 'w')
writer = csv.writer(wfile)
map(writer.writerow, map(list, zip(*on_schedule)))
wfile.close()

#for x in off_list:
#    print(x)
wfile = open('off_list.csv', 'w')
writer = csv.writer(wfile)
map(writer.writerow, off_list)
wfile.close()

wfile=open('on_list.csv', 'w')
writer = csv.writer(wfile)
map(writer.writerow, on_list)
wfile.close()




    
    
    
    
    
        
    
    
    
    

    



    


