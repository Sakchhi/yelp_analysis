import pandas as pd
import json
import string
import unicodedata
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords, words
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
# from nltk.stem.snowball import SnowballStemmer
import re
from pprint import pprint
import matplotlib.pyplot as plt

with open('contraction_map.json') as f:
    contraction_map = json.load(f)


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


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


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
        text = [w.strip(string.punctuation) for w in text]
        text = [w for w in text if not any(c.isdigit() for c in w)]
        pos_tags = pos_tag(text)
        text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
        text = [w.lower() for w in text]
        stop = stopwords.words("english")
        text = [w for w in text if w not in stop]
        text = [t for t in text if len(t) > 2]
        text = [t for t in text if t != 'nan']
        # stemmer = SnowballStemmer(language="english")

        # all_words = set(words.words())
        # text = [t for t in text if t in all_words]
        # text = [stemmer.stem(t) for t in text]
    except:
        text = None
    return text


if __name__ == '__main__':
    df_raw = pd.read_csv("yelp_merged_reviews_gr1000.csv")
    print(df_raw.columns)
    df_raw.drop('Unnamed: 0', axis=1, inplace=True)
    df_raw.set_index('review_id', inplace=True)

    # df_raw['full_text'] = df_raw.apply(create_full_text, axis=1)
    df_raw = df_raw.head(50)
    df_raw['clean_text'] = df_raw.text.apply(remove_accented_chars)
    df_raw.clean_text = df_raw.clean_text.apply(expand_contractions)
    df_raw.clean_text = df_raw.clean_text.apply(remove_special_characters)
    #
    df_raw['full_text_cleaned'] = df_raw.clean_text.apply(clean_text)
    df_raw['full_text_cleaned_text'] = df_raw.full_text_cleaned.apply(lambda r: ' '.join(r))
    # df_raw.to_excel('yelp_restaurant_reviewes_cleaned.xlsx')

    # print(df_raw.columns)
    for i in range(5):
        print(df_raw.iloc[i].full_text_cleaned)
        print("=======================")
