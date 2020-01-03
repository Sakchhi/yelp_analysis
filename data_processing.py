import pandas as pd
import os
import json


def create_dataframes():
    for filename in os.listdir('Data'):
        if filename.split('.')[1] == 'json':
            try:
                fp = open(os.path.join('Data', filename))
                for i in range(5):
                    print(fp.readline())
            finally:
                fp.close()
            # print(content)


def create_reviews_df():
    try:
        # fp = open('Data/review.json')
        d = pd.read_json('Data/review.json', lines=True)
        df_reviews = pd.DataFrame()
        # for i in range(5):
        #
        #     rev = dict(fp.readline())
        #     print(type(rev))
        #     print(pd.DataFrame(list(rev.items())))
    finally:
        # fp.close()
    print(df_reviews)
    print(d.head())


if __name__ == "__main__":
    # for (root,dirs,files) in os.walk('Data'):
    #     print(root)
    #     print(dirs)
    #     print(files)
    #     print('--------------------------------')
    # create_dataframes()
    create_reviews_df()