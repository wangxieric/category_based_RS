"""
    Create by Xi Wang @ 2018-05-02
"""

from surprise import NMF
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import KFold
from collections import defaultdict
from collections import OrderedDict
'''
    Load user rating from pickle
'''
# Phoenix_rating_hist,LV_rating_hist = pickle.load(open('user_rating_hist_after_filter.p','rb'))
'''
    Create csv file 
'''
# Phoenix_rating_hist.to_csv('Phoenix_rating_hist.csv', sep='\t')
# LV_rating_hist.to_csv('LV_rating_hist.csv', sep='\t')


def precision_recall_at_k(predictions, k=10, threshold=0):
    """
    :param predictions:
    :param k:
    :param threshold:
    :return: precision and recall at k metrics for each user
    """
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        # print(est,true_r)
        user_est_true[uid].append((est,true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items on top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommend items on top k
        n_rel_and_n_rec_k = sum((true_r >= threshold) and (est >= threshold)
                                for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_n_rec_k / n_rec_k if n_rec_k != 0 else 1

        # Recall@k: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_n_rec_k / n_rel if n_rel != 0 else 1

    return precisions, recalls


def get_top_n(predictions, n = 10):
    """
    :param predictions:(list of prediction objects): the list of predictions, as returned by the test method
            of an algorithm.
    :param n: The number of recommendation to output for each user.
    :return: the top-n recommendation for each user from a set of predictions. A dict where keys are user (raw) ids
            and values are list of tuples:[(raw item id, rating estimation), ...] of size n
    """
    # First map the predictions to each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid,est))

    # Then sort the predictions for each user and retrieve the k highest ones
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x:x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n



#file_path = 'Phoenix_rating_hist.csv'
file_path = 'LV_rating_hist_copy.csv'
reader = Reader(line_format='user item rating', sep=' ')
data = Dataset.load_from_file(file_path=file_path, reader=reader)
kf = KFold(n_splits=5)
algo = NMF()
overall_precision = 0.0
overall_recall = 0.0
for trainset, testset in kf.split(data):
    # get the item of all the items
    item_list = list(set([i[1] for i in testset]))
    user_list = list(set([i[0] for i in testset]))

    # Create user visiting history, and mark which venue user have been visited
    user_visiting_hist = {}
    for hist in testset:
        if hist[0] in user_visiting_hist:
            user_visiting_hist[hist[0]].append(hist[1])
        else:
            user_visiting_hist[hist[0]] = [hist[1]]

    algo.fit(trainset)

    # Making recommendation for each user and all venues in test data set
    precision = 0.0
    recall = 0.0
    k = 20
    for user in user_list:
        est_item_rating = {}
        for item in item_list:
            est_item_rating[item] = algo.predict(user, item, clip=False).est
            # print(algo.predict(user, item, clip=False).est)
        sorted_items_dict = OrderedDict(sorted(est_item_rating.items()))
        sorted_items = list(sorted_items_dict.keys())
        count = 0
        for i in sorted_items[:k]:
            if i in user_visiting_hist[user]:
                count += 1
        precision += count/float(k)
        recall += count /float(len(user_visiting_hist[user]))
    print('precision: ', precision/len(user_list), ' recall: ', recall/len(user_list))
    overall_precision += precision/len(user_list)
    overall_recall += recall/len(user_list)
print('overall_precision: ', overall_precision/5, ' overall_recall: ', overall_recall/5)


