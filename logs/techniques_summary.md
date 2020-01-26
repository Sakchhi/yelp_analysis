###Text Preprocessing
- Tokenization
	- Split by space -- WhiteSpaceTokenizer
	- Split by space and punctutation -- WordPunktTokenizer
	- Split by heuristics -- TreebankWordTokenizer
- Normalization -- Stemming and Lemmatization
- Stemming
	- PorterStemmer
	- SnowballStemmer
- Lemmatization
	- WordNetLemmatizer
- Other steps
	- Lowercasing -- Proper Nouns vs other Nouns
	- Normalizing acronyms


###Feature Extraction
- BoW
- n-grams
- Tfidf