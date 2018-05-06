"""
    Created by Xi Wang @ 2018-04-23
    Aim at preprocess gowalla dataset
"""
import pandas as pd

header = [
    'id',           # venue id
    'lat',          # venue latitude
    'lng',          # venue longitude
    'name',         # venue name
    'city_state'    # venue located state and city, separated by ','
]

venue_information = pd.read_csv('./gowalla/gowalla_spots_subset2.csv',
                                names = header,
                                header = 0,
                                delimiter='\t')

print(venue_information.shape)

Chicago_venue = set()
San_Francisco_venue = set()

for index, row in venue_information.iterrows():
    city, state = row['city_state'].split(",")
    if city == 'Chicago':
        Chicago_venue.add(row['id'])
    elif city == 'San Francisco':
        San_Francisco_venue.add(row['id'])

print(len(Chicago_venue))
print(len(San_Francisco_venue))
