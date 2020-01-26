import itertools

import config, run_config

import os
import pandas as pd
import json
import string
import unicodedata
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
import re
import spacy
import wordninja

nlp = spacy.load('en')

with open(os.path.join(config.UTILITIES_DIR, 'contraction_map.json')) as f:
    contraction_map = json.load(f)

with open(os.path.join(config.UTILITIES_DIR, 'stop_words.txt'), 'rb') as f:
    stop_words_list = []
    for line in f:
        stop_words_list.append(line.decode("utf-8").strip())


def remove_accented_chars(text):
    pattern = r'(&#x\d\d\d\w)'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def remove_special_characters(text, remove_digits=True):
    text = text.replace('/', ' ')
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def expand_contractions(text, contraction_mapping=contraction_map):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def clean_text(text):
    try:
        text = re.split(r'\s+|[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]*', text)

        # text = [w.strip(string.punctuation) for w in text]
        text = [w for w in text if not any(c.isdigit() for c in w)]
        # text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
        # print(text)
        # pos_tags = pos_tag(text)
        # lemmatizer = WordNetLemmatizer()
        # stemmer = SnowballStemmer(language="english")

        text = [w.lower() for w in text]
        text = [' '.join(wordninja.split(word)) for word in text]
        # stop = stopwords.words("english")
        # text = [w for w in text if w not in stop]
        text = [w for w in text if w not in stop_words_list]
        text = [t for t in text if len(t) > 2]
        text = [t for t in text if t != 'nan']
        # text = [stemmer.stem(t) for t in text]

        # all_words = set(words.words())
        # text = [t for t in text if t in all_words]
        # text = [stemmer.stem(t) for t in text]
    except:
        text = []
    return text


def chunk_preprocessing(df_chunk):
    df_chunk.drop('Unnamed: 0', axis=1, inplace=True)
    df_chunk.set_index('review_id', inplace=True)

    df_chunk['clean_text'] = df_chunk.text.astype(str).apply(remove_accented_chars)
    df_chunk['clean_text'] = df_chunk.clean_text.apply(expand_contractions)
    punct_regex = r'\W+'
    df_chunk['clean_text'] = df_chunk.clean_text.apply(lambda r: re.sub(punct_regex, ' ', r))
    df_chunk.clean_text = df_chunk.clean_text.apply(remove_special_characters)

    df_chunk['full_text_cleaned'] = df_chunk.clean_text.apply(clean_text)
    # for i in range(5):
    #     print(df_chunk.iloc[i].full_text_cleaned)

    df_chunk['full_text_cleaned_text'] = df_chunk.apply(lambda r: ' '.join(r[-1]), axis=1)

    return df_chunk


if __name__ == '__main__':
    df_raw = pd.read_csv(os.path.join(config.REVIEWS_EXTRACTED_ROOT, "yelp_merged_reviews_gr1000.csv"), nrows=10000)

    df_processed = chunk_preprocessing(df_raw.copy())
    for i in range(5):
        print(df_processed.iloc[i].full_text_cleaned_text, end='\n\n')
    df_processed.to_csv(
        os.path.join(config.DATA_DIR, 'processed/preprocess',
                     '{}_yelp_restaurant_reviews_cleaned_gr1000_10k_v{}.csv'.format(run_config.model_date_to_write,
                                                                                    run_config.model_version_to_write)))
