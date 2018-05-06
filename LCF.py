import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import operator
'''
    Shuffle pandas dataframe
'''

def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df


def slice_dataframe(percentage, data):
    train_data = data.iloc[:int(percentage * len(data.index))]
    test_data = data.iloc[int(percentage * len(data.index)):]

    return train_data, test_data


'''
    Calculate the similarity between users with cosine similarity
'''


def cal_user_similarity(training_data):
    users = list(training_data.index)
    uv_sim = np.zeros((len(users), len(users)))
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            uv_sim[i, j] = \
            cosine_similarity([training_data.loc[users[i]]], [training_data.loc[users[j]]])[0]
            uv_sim[j, i] = uv_sim[i, j]
    return users, uv_sim

Phoenix_rating_hist,LV_rating_hist = pickle.load(open('user_rating_hist_after_filter.p','rb'))

# obtain training and test dataset
print("loading dataset")
#usr_loc_hist = shuffle(Phoenix_rating_hist)
usr_loc_hist = LV_rating_hist
uv = pd.crosstab(usr_loc_hist['user_id'], usr_loc_hist['business_id'])

for index, row in usr_loc_hist.iterrows():
    uv[row['business_id']][row['user_id']] = row['stars']

all_users = list(uv.index)
all_venues = list(uv)

tk_train, tk_test = slice_dataframe(0.80, usr_loc_hist)
tk_train_pd = pd.crosstab(tk_train['user_id'], tk_train['business_id'])
tk_test_pd = pd.crosstab(tk_test['user_id'], tk_test['business_id'])
all_test_venues = list(tk_test_pd)
# uv_train = tk_train_pd.as_matrix()
# uv_test = tk_test_pd.as_matrix()
# print type(uv_test)
print("Calculating similarity score ",  datetime.now())
users, user_similarity = cal_user_similarity(tk_train_pd)
print("Finish Calculating similarity score",  datetime.now())

'''
    Keep user similarity score in the file
'''
pickle.dump([tk_train, tk_test, users, user_similarity], open("user_similarity_LV.p","wb"))

# tk_train, tk_test, user_similarity = pickle.load(open("user_similarity_Phoenix.p", "rb"))
# tk_train_pd = pd.crosstab(tk_train['user_id'], tk_train['business_id'])
# tk_test_pd = pd.crosstab(tk_test['user_id'], tk_test['business_id'])
# all_test_venues = list(tk_test_pd)

#
# '''
#     Making Recommendation
# '''
#
# def get_venue_score(venue, user_id):
#
#     return sum([user_similarity[user_id, user] * uv.loc[user, venue] for user in all_users if user != user_id])
#     # return sum([user_similarity[user_id, user] * uv.loc[user, venue] for user in all_users if user != user_id])
#     #       / sum([user_similarity[user_id, user] for user in all_users if user != user_id])
#
# def recommend(user_id, n):
#     # venue_score = {}
#     venue_score = {venue : get_venue_score(venue,user_id) for venue in all_test_venues}
#     # venue_score = { venue : [sum(user_similarity[user_id, user] * uv.loc[user, venue]) for user in all_users] for venue in all_test_venues}
#     # for user in all_users:
#     #     if user != user_id:
#     #         # obtain the similarity score from user_similarity
#     #         sim = user_similarity[user_id, user]
#     #         for venue in all_test_venues:
#     #             if venue in venue_score:
#     #                 venue_score[venue] += sim * uv.loc[user, venue]
#     #             else:
#     #                 venue_score[venue] = sim * uv.loc[user, venue]
#     recommend_dict = sorted(venue_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:n]
#     return [key for key, value in recommend_dict]
#
# num_test = tk_test.shape[0]
# n_trials = tk_test_pd.shape[0]
# returned_recs = [None for i in range(n_trials)]
# n_recs = [0.0 for i in range(n_trials)]
# recovered_venues = [0.0 for i in range(n_trials)]
#
# print "Begining Recommendation"
# progress = n_trials
# cnt = 0
# print progress
# for index, event in tk_test_pd.iterrows():
#     print cnt
#     if cnt % (progress / 10) == 0:
#         print('Progress:', cnt * 100 / progress, '%', datetime.now())
#     u = index
#
#     recs = recommend(u, 5)
#
#     # Record recommendations
#     returned_recs[cnt] = recs
#     n_recs[cnt] = len(recs)
#
#     # Compute Reward
#     recs = set(recs)
#     #venue = event['business_id']
#     bt = event.apply(lambda x : x > 0)
#     venue = bt[bt].index.tolist()
#     recovered_venues[cnt] = len([i for i in venue if i in recs])
#     # if venue in recs:
#     #     recovered_venues[cnt] = 1
#     # else:
#     #     recovered_venues[cnt] = 0
#     cnt += 1
# '''
#     Calculate Precision and Recall
# '''
# precision = sum(recovered_venues) / float(sum(n_recs))
# # defined by how many user checkin history have been predicted
# recall = sum(recovered_venues) / float(num_test)
# print(precision, recall)

