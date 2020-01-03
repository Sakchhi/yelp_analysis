import pandas as pd
import json


def get_business_data():
    stop = 1000000

    ifile = open('Data/business.json')
    all_data = list()
    for i, line in enumerate(ifile):
        if i % 10000 == 0:
            print(i)
        if i == stop:
            break
            # convert the json on this line to a dict
        data = json.loads(line)
        # extract what we want
        business_id = data['business_id']
        name = data['name']
        address = data['address']
        city = data['city']
        state = data['state']
        postal_code = data['postal_code']
        latitude = data['latitude']
        longitude = data['longitude']
        stars = data['stars']
        review_count = data['review_count']
        is_open = data['is_open']
        attributes = data['attributes']
        categories = data['categories']
        hours = data['hours']
        # add to the data collected so far
        all_data.append([business_id, name, address, city, state, postal_code, latitude,
                         longitude, stars, review_count, is_open, attributes, categories,
                         hours])
    # create the DataFrame
    df = pd.DataFrame(all_data, columns=['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude',
                                         'longitude', 'stars', 'review_count', 'is_open', 'attributes', 'categories',
                                         'hours'])

    df.to_excel('Yelp_all_businesses.xlsx', index=False)


restaurant_biz_ids = []
def filter_restaurants(row):
    if not row[-2]:
        if ("restaurants" in row[-2].lower()) or ("restaurant" in row[-2].lower()):
            print(row[0])


def get_restaurants():
    df_raw = pd.read_excel('Yelp_all_businesses.xlsx')
    print(df_raw.iloc[1][-2])

if __name__=='__main__':
    get_restaurants()