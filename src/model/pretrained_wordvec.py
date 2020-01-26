import config, run_config

import os
import pickle
import csv
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import spacy
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

nlp = spacy.load('en')


def get_vectors(row):
    doc = nlp(row)
    full_w2v = np.array([w.vector for w in doc])
    return pd.Series(full_w2v.mean(axis=0))


def get_predictions(train_data, train_labels, test_data):
    log_reg_model = LogisticRegression()
    log_reg_model.fit(train_data, train_labels)
    predictions = log_reg_model.predict(test_data)

    pickle_file_name = os.path.join(config.MODEL_DIR, 'classifier_model/{}_logreg_pretrained_spacy96_v{}.pickle'.format(
        run_config.model_date_to_read, run_config.model_version_to_read))
    pickle.dump(log_reg_model, open(pickle_file_name, 'wb'))
    return predictions


if __name__ == '__main__':
    df_raw = pd.read_csv(os.path.join(config.CLEANED_REVIEWS_ROOT,
                                      "20200125_yelp_restaurant_reviews_cleaned_gr1000_10k_v1.3.csv"))  # .format(
    # run_config.model_date_to_read, run_config.model_version_to_read)))
    df_raw.full_text_cleaned_text.fillna('', inplace=True)
    print(df_raw.columns.tolist())
    df_feature = pd.DataFrame(df_raw.full_text_cleaned_text.values, columns=['text'])
    df_feature['label_rating'] = df_raw.stars_x.apply(lambda r: int(r > 3))
    print(df_feature.label_rating.value_counts())
    df_wordvec = df_raw.full_text_cleaned_text.apply(lambda r: get_vectors(r))
    print(df_wordvec.shape)
    X_train, X_val, y_train, y_val = train_test_split(df_wordvec, df_feature.label_rating, test_size=0.2,
                                                      random_state=42)

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
    preprocessing_notes = "NO STEMMER, wordninja, Custom stopwords"
    feature_notes = "Pretrained Spacy Word2Vec -- 96 avg"
    model_notes = "Logistic Regression"
    misc_notes = ""
    fields = [run_config.model_version_to_write, accuracy_score, fpr, f1,
              preprocessing_notes, feature_notes, model_notes, misc_notes]
    with open(os.path.join(config.LOGS_DIR, r'results_summary.csv'), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    df_predictions = pd.DataFrame({"Predictions": y_pred, "Labels": y_val}, index=df_raw.loc[X_val.index]['review_id'])
    df_predictions.to_excel(os.path.join(config.OUTPUTS_DIR,
                                         '{}_LogisticRegression_pretrained_spacy96_v{}.xlsx'.format(
                                             run_config.model_date_to_write,
                                             run_config.model_version_to_write)))
