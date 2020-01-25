import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import config
import run_config


def get_ngram(data):
    tfidf = TfidfVectorizer(ngram_range=(1, 2))
    # tfidf.fit(data)
    tfidf_vec = tfidf.fit_transform(data)
    tfidf_df = pd.DataFrame(tfidf_vec.toarray(), columns=tfidf.get_feature_names())
    print(tfidf.get_feature_names())
    with open(os.path.join(config.LOGS_DIR, 'tfidf_list/{}_tfidf_list_v{}.txt'.format(
            run_config.model_date_to_write, run_config.model_version_to_write)), 'w') as f:
        for i in tfidf.get_feature_names():
            f.write('%s,' % i)
    return tfidf, tfidf_df


if __name__ == '__main__':
    df_raw = pd.read_csv(
        os.path.join(config.CLEANED_REVIEWS_ROOT, "20200124_yelp_restaurant_reviews_cleaned_gr1000_10k_v0.3.csv"))
    # "}.csv".format(run_config.model_date_to_read,
    #                run_config.model_version_to_read)))
    # train_length = df_raw.shape[0]
    df_raw.full_text_cleaned_text.fillna('', inplace=True)
    print(df_raw.columns)

    tfidf_model, df_tfidf = get_ngram(df_raw.full_text_cleaned_text.tolist())
    print(df_tfidf.head())
    pickle.dump(tfidf_model, open(os.path.join(config.MODEL_DIR,
                                               "feature_eng_model/tfidf_model/{}_tfidf_v{}.pickle".format(
                                                   run_config.model_date_to_write,
                                                   run_config.model_version_to_write)), 'wb'))

    print(df_raw.shape, )
    df_tfidf.to_csv(
        os.path.join(config.DATA_DIR, 'processed/feature_engineering/tfidf/{}_tfidf_v{}.csv'.format(
            run_config.model_date_to_write, run_config.model_version_to_write)), index=False)
