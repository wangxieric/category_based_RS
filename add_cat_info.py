import pickle
import pandas as pd
import categories_hierarchy as hc
import json

# Phoenix_rating_hist,LV_rating_hist = pickle.load(open('user_rating_hist_after_filter.p','rb'))
hierarchy = hc.load()
file = open('/Users/xiwang/git-code/Dataset/poi_data/yelp_dataset_round11/business.json', 'r')

category_alias_map = {}
with open('./data/categories.json', 'rb') as f:
    categories = json.load(f)
    for category in categories:
        category_alias_map[category['title']] = category['alias']
f.close()

location_category = {}
unmatched_cat = set()
count_business = 0
count_no_cat_business = 0
for line in file.readlines():
    location = json.loads(line)
    min_level = 10
    count_business += 1
    if len(location['categories']) > 0:
        general_cat = ' '
        for category in location['categories']:
            if category in category_alias_map and hierarchy.get_level_num(category_alias_map[category]) < min_level:
                general_cat = category_alias_map[category]
            else:
                # print('No Match Category Exception: ', category)
                unmatched_cat.add(category)
        if general_cat == ' ':
            print('No Category Exception: ', location['business_id'])
            location_category[location['business_id']] = None
            count_no_cat_business += 1
        else:
            location_category[location['business_id']] = general_cat
    else:
        # print('No Category Exception: ', location['business_id'])
        location_category[location['business_id']] = None
        count_no_cat_business += 1
file.close()

print(count_business)  # 156639
print(count_no_cat_business)  # 378
print(len(unmatched_cat), unmatched_cat)
# 22 {'Rolfing', 'Flowers', 'Mags', 'Ethnic Food', '& Probates', 'Used', 'Spin Classes', 'Trusts', 'Books',
#       'Ethic Grocery', 'Vinyl Siding', 'Ethnic Grocery', 'Music & Video', 'Golf Equipment Shops',
#       'Dry Cleaning & Laundry', 'Wills', 'Psychics & Astrologers', 'Vintage & Consignment', 'Beer',
#       'Pet Boarding/Pet Sitting', 'Leisure Centers', 'Wine & Spirits'}

# pickle.dump(location_category, open('yelp_round11_loc_cat.p', 'wb'))

