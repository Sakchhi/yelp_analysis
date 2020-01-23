from gensim.models import ldamulticore
import pandas as pd


def train_lda(train_corpus4):
    lda_train4 = ldamulticore.LdaMulticore(
        corpus=train_corpus4,
        num_topics=50,
        passes=50,
        eval_every=1,
        per_word_topics=True)
    lda_train4.


if __name__ == '__main__':
    df_raw = pd.read_csv("yelp_restaurant_reviews_cleaned_gr1000.csv", nrows=25000)
    train_lda(df_raw.full_text_cleaned_text)

    print()
