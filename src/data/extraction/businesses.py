import config, run_config

import pandas as pd
import json
import os


def get_business_data(file_name_business_data):
    fp = open(os.path.join(config.DATA_DIR, 'raw/original/business.json'))
    all_data = list()
    for line in fp:
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
    fp.close()
    # create the DataFrame
    df = pd.DataFrame(all_data, columns=['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude',
                                         'longitude', 'stars', 'review_count', 'is_open', 'attributes', 'categories',
                                         'hours'])

    df.to_excel(file_name_business_data, index=False)


def get_restaurants(raw_data_file, file_name_restaurant):
    df_raw = pd.read_excel(raw_data_file)
    restaurant_biz_ids = []
    restaurant_num_comments = []
    for i in range(len(df_raw)):
        if type(df_raw.iloc[i][-2]) != float:
            if ("restaurants" in df_raw.iloc[i][-2].lower()) or ("restaurant" in df_raw.iloc[i][-2].lower()):
                restaurant_biz_ids.append(df_raw.iloc[i][0])
                restaurant_num_comments.append(df_raw.iloc[i][-5])
    pd.DataFrame({'business_id': restaurant_biz_ids, 'num_comments': restaurant_num_comments}).to_excel(os.path.join(
        config.DATA_DIR, 'raw/extracted/ids', file_name_restaurant), index=False)


if __name__ == '__main__':
    file_name = os.path.join(config.DATA_DIR, 'raw/extracted/ids', '20200104_Yelp_all_businesses.xlsx')
    restaurant_file_name = '20200104_Yelp_restaurant_business.xlsx'
    get_business_data(file_name)
    get_restaurants(file_name, restaurant_file_name)
