"""
    Created on Thu April 26, 2018

    @author xiwang
"""
from collections import OrderedDict
import json


def _create_hierarchy(hierarchy, category, parent):
    if 'alias' in category:
        hierarchy.add_node(category['alias'])
    if 'parents' in category and len(category['parents']) > 0:
        hierarchy.add_edge(category['parents'][0], category['alias'])


def load():
    h = CategoryHierarchy()
    with open('./data/categories.json','rb') as f:
        categories = json.load(f)
    for category in categories:
        _create_hierarchy(h, category, None)
    return h


class CategoryHierarchy:
    def __init__(self):
        self.hierarchy = OrderedDict()

    def add_node(self, name):
        self.hierarchy[name] = {'children':[], 'parents': None}

    def add_edge(self, from_name, to_name):
        if from_name not in self.hierarchy:
            self.add_node(from_name)
        self.hierarchy[from_name]['children'].append(to_name)
        if to_name not in self.hierarchy:
            self.add_node(to_name)
        self.hierarchy[to_name]['parent'] = from_name

    def keys(self):
        return self.hierarchy.keys()

    def __len__(self):
        return len(self.hierarchy)

    def get_level_num(self, category):
        if category in self.hierarchy:
            level = 0
            # print(category)
            if 'parent' in self.hierarchy[category]:
                parent = self.hierarchy[category]['parent']
                while parent:
                    level += 1
                    if 'parent' in self.hierarchy[parent]:
                        parent = self.hierarchy[parent]['parent']
                    else:
                        parent = False
            return level
        else:
            return 0

    # level distance to Lowest Common Ancestor
    def dist_to_LCA(self, n1, n2, l):
        if n1 == n2:
            return l
        else:
            l1 = self.get_level_num(n1)
            l2 = self.get_level_num(n2)
            if l1 < l2:
                # l2 is farther away from the node
                return self.dist_to_LCA(n1, self.hierarchy[n2]['parent'], l+1)
            elif l1 > l2:
                # l1 is farther away from the node
                return self.dist_to_LCA(self.hierarchy[n1]['parent'],n2,l+1)
            else:
                return self.dist_to_LCA(self.hierarchy[n1]['parent'], self.hierarchy[n2]['parent'], l+1)
