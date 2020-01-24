import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import config
import run_config


def get_bow(data):
    count = CountVectorizer()
    count.fit(data)
    bag_of_words = count.transform(data)
    bow_df = pd.DataFrame(bag_of_words.toarray(), columns=count.get_feature_names())
    print(count.get_feature_names())
    with open(os.path.join(config.LOGS_DIR, 'bow_list/{}_bow_list_10k_v{}.txt'.format(
            run_config.model_date_to_write, run_config.model_version_to_write)), 'w') as f:
        for i in count.get_feature_names():
            f.write('%s,' % i)
    return count, bow_df


if __name__ == '__main__':
    df_raw = pd.read_csv(os.path.join(config.CLEANED_REVIEWS_ROOT, "{}_yelp_restaurant_reviews_cleaned_gr1000_10k_v{"
                                                                   "}.csv".format(run_config.model_date_to_read,
                                                                                  run_config.model_version_to_read)))
    # train_length = df_raw.shape[0]
    df_raw.full_text_cleaned_text.fillna('', inplace=True)
    print(df_raw.columns)

    count_vec_model, df_bow = get_bow(df_raw.full_text_cleaned_text.tolist())
    print(df_bow.head())
    pickle.dump(count_vec_model, open(os.path.join(config.MODEL_DIR,
                                                   "feature_eng_model/{}_bag_of_words__10k_v{}.pickle".format(
                                                       run_config.model_date_to_write,
                                                       run_config.model_version_to_write)), 'wb'))

    print(df_raw.shape, )
    df_bow.to_csv(
        os.path.join(config.DATA_DIR, 'processed/feature_engineering/{}_bag_of_words_10k_v{}.csv'.format(
            run_config.model_date_to_write, run_config.model_version_to_write)), index=False)
