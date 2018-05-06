import numpy as np
import pandas as pd
import math
from datetime import datetime
import categories_hierarchy as hc

class NoPreferencesError(Exception):
    def __init__(self):
        self.value = user
    def __str__(self):
        return repr(self.value)

class CollaborativeFiltering:
    def __init__(self, usr_loc_hist):
        # load categories hierarchy
        self.ch = hc.load()
        # number of users in system
        self.n_users = len(usr_loc_hist['user_id'].unique())
        # user_venue count matrix
        self.uv_cnt = pd.crosstab(usr_loc_hist['user_id'],
                                  usr_loc_hist['business_id'])
        # user location history
        self.usr_loc_hist = usr_loc_hist.groupby['venue_category_name']
