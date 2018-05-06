"""
    Created by Xi Wang 2018-04-22
    Yelp Data filtering for dataset reproduction
"""
import json
import pandas as pd
import datetime
import pickle

'''
    Obtain the venue located city from the venue profile
    form: { business_id : city_name }
'''
venue_location = {}
with open('dataset/business.json','r') as jf:
    for line in jf:
        data = json.loads(line)
        venue_location[data['business_id']] = data['city']
jf.close()

'''
    Create the dataframe for the rating history of two cities: Phoenix and Las Vegas
    form: 
                user_id     business_id     stars
        index   
        0        u0          b0              r0

'''
# columns = ['user_id', 'business_id', 'stars']
# Phoenix_rating_hist = pd.DataFrame(columns=columns)
# LV_rating_hist = pd.DataFrame(columns=columns)
#
# Phoenix_rating_hist_list = []
# LV_rating_hist_list = []
#
# print('start processing review data', datetime.datetime.now())
# with open('dataset/review.json','r') as jf:
#     for line in jf:
#         data = json.loads(line)
#         if venue_location[data['business_id']] == 'Phoenix':
#             Phoenix_rating_hist_list.append([data['user_id'], data['business_id'], data['stars']])
#
#         elif venue_location[data['business_id']] == 'Las Vegas':
#             LV_rating_hist_list.append([data['user_id'], data['business_id'], data['stars']])
# jf.close()
#
# Phoenix_rating_hist = Phoenix_rating_hist.append(pd.DataFrame(Phoenix_rating_hist_list,columns=columns),
#                                                     ignore_index=True)
# LV_rating_hist = LV_rating_hist.append(pd.DataFrame(LV_rating_hist_list,columns=columns), ignore_index=True)
#
# print(Phoenix_rating_hist.shape)
# print(LV_rating_hist.shape)
# print('Finish processing review data', datetime.datetime.now())
# pickle.dump([Phoenix_rating_hist, LV_rating_hist], open('user_rating_hist.p','wb'))

'''
    The pickle unable to deal with the '.p' file which is created by pickle with python 2.7 version
'''
Phoenix_rating_hist, LV_rating_hist = pickle.load(open('user_rating_hist.p','rb'))
print(Phoenix_rating_hist.shape)
print(LV_rating_hist.shape)
'''

    Remove users with less than 20 ratings and venues with less than 5 ratings 
    in the Phoenix dataset

'''

print('Start Filtering Phoenix dataset', datetime.datetime.now())

# Filter Venues

Phoenix_filtered_venue = Phoenix_rating_hist['business_id'].value_counts()
Phoenix_filtered_venue = Phoenix_filtered_venue[Phoenix_filtered_venue < 5].index.tolist()

print(Phoenix_rating_hist.shape)
print(list(Phoenix_rating_hist))

filtered_index = []
for index, row in Phoenix_rating_hist.iterrows():
    #print row
    if row['business_id'] in Phoenix_filtered_venue:
        filtered_index.append(index)

Phoenix_rating_hist = Phoenix_rating_hist.drop(filtered_index)

# Filter Users
Phoenix_filtered_user = Phoenix_rating_hist['user_id'].value_counts()
Phoenix_filtered_user = Phoenix_filtered_user[Phoenix_filtered_user < 20].index.tolist()

filtered_index = []
for index, row in Phoenix_rating_hist.iterrows():
    if row['user_id'] in Phoenix_filtered_user:
        filtered_index.append(index)

Phoenix_rating_hist = Phoenix_rating_hist.drop(filtered_index)

print('Finish filtering Phoenix dataset', datetime.datetime.now())

'''

    Remove users with less than 20 ratings and venues with less than 5 ratings 
    in the Las Vegas dataset

'''
print('Start filtering Las Vegas dataset', datetime.datetime.now())

# Filter Venues

LV_filtered_venue = LV_rating_hist['business_id'].value_counts()
LV_filtered_venue = LV_filtered_venue[LV_filtered_venue < 5].index.tolist()

filtered_index = []
for index, row in LV_rating_hist.iterrows():
    if row['business_id'] in LV_filtered_venue:
        filtered_index.append(index)

LV_rating_hist = LV_rating_hist.drop(filtered_index)

# Filter Users

LV_filtered_user = LV_rating_hist['user_id'].value_counts()
LV_filtered_user = LV_filtered_user[LV_filtered_user < 20].index.tolist()

filtered_index = []
for index, row in LV_rating_hist.iterrows():
    if row['user_id'] in LV_filtered_user:
        filtered_index.append(index)

LV_rating_hist = LV_rating_hist.drop(filtered_index)
print('Finish filtering Las Vegas dataset', datetime.datetime.now())

pickle.dump([Phoenix_rating_hist,LV_rating_hist], open('user_rating_hist_after_filter.p','wb'))
#Phoenix_rating_hist,LV_rating_hist = pickle.loads(open('user_rating_hist_after_filter.p','rb'))


