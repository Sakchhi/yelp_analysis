import os
import pickle
import csv

import pandas as pd
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

import config
import run_config


def get_predictions(train_data, train_labels, test_data):
    mnb_model = MultinomialNB()
    mnb_model.fit(train_data, train_labels)
    predictions = mnb_model.predict(test_data)

    pickle_file_name = os.path.join(config.MODEL_DIR, 'classifier_model/{}_mnb_bow_v{}.pickle'.format(
        run_config.model_date_to_read, run_config.model_version_to_read))
    pickle.dump(mnb_model, open(pickle_file_name, 'wb'))
    return predictions


if __name__ == '__main__':
    file_to_read = (os.path.join(config.DATA_DIR, 'processed/feature_engineering/{}_bag_of_words_10k_v{}.csv'.format(
        run_config.model_date_to_read,
        run_config.model_version_to_read)))
    df_bow = pd.read_csv(file_to_read)
    print(df_bow.columns.tolist())
    df_raw = pd.read_csv(os.path.join(config.CLEANED_REVIEWS_ROOT,
                                      "20200124_yelp_restaurant_reviews_cleaned_gr1000_10k_v0.3.csv"))  # .format(
    # run_config.model_date_to_read, run_config.model_version_to_read)))
    print(df_raw.columns.tolist())
    df_feature = df_bow.copy()
    df_feature['label_rating'] = df_raw.stars_x.apply(lambda r: int(r > 3))
    print(df_feature.label_rating.value_counts())
    X_train, X_val, y_train, y_val = train_test_split(df_feature.iloc[:, :-1], df_feature.label_rating, test_size=0.2)

    y_pred = get_predictions(X_train, y_train, X_val)

    accuracy_score = metrics.accuracy_score(y_val, y_pred)
    print(accuracy_score)

    cm = metrics.confusion_matrix(y_val, y_pred)
    tp, fn, fp, tn = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
    fpr = fp / (fp + tn)
    print("FPR = {}".format(fpr))
    print("TPR = {}".format(tp / (tp + fn)))

    f1 = metrics.f1_score(y_val, y_pred)
    print("F1 Score = {}".format(f1))

    columns = ['Run', 'Accuracy', 'FPR', 'F1 Score', 'Preprocessing', 'Feature', 'Model', 'Notes']
    preprocessing_notes = "Snowball Stemmer, wordninja"
    feature_notes = "BoW 2-gram -- Max features 5k"
    model_notes = "MNB"
    misc_notes = ""
    fields = [run_config.model_version_to_write, accuracy_score, fpr, f1,
              preprocessing_notes, feature_notes, model_notes, misc_notes]
    with open(os.path.join(config.LOGS_DIR, r'results_summary.csv'), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
