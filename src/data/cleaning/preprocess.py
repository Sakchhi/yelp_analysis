import pandas as pd
import config, run_config
import os


def merge_business_data(reviews_df, biz_df):
    merged_df = pd.merge(reviews_df, biz_df[['business_id', 'stars', 'review_count', 'categories']],
                         how='left', on='business_id')
    return merged_df


if __name__ == '__main__':
    df_reviews = pd.read_csv(os.path.join(config.REVIEWS_EXTRACTED_ROOT, 'yelp_restaurant_reviews_gr1000.csv'))
    print(df_reviews.columns.tolist())
    df_biz = pd.read_excel(os.path.join(config.DATA_DIR, 'raw/extracted/ids', '20200104_Yelp_all_businesses.xlsx'))
    print(df_biz.columns.tolist())
    df_merge = merge_business_data(df_reviews, df_biz)
    print(df_reviews.shape, df_biz.shape, df_merge.shape)
    df_merge.to_csv(os.path.join(config.REVIEWS_EXTRACTED_ROOT, 'yelp_merged_reviews_gr1000.csv'))
