import os

ROOT_DIR = '/home/sirius/Documents/Codes/yelp_analysis'
DATA_DIR = os.path.join(ROOT_DIR, 'Data/')
REVIEWS_EXTRACTED_ROOT = os.path.join(DATA_DIR, 'raw/extracted/reviews')
CLEANED_REVIEWS_ROOT = os.path.join(DATA_DIR, 'processed/preprocess')
MODEL_DIR = os.path.join(ROOT_DIR, 'models/')
UTILITIES_DIR = os.path.join(ROOT_DIR, 'src/utilities/')
OUTPUTS_DIR = os.path.join(ROOT_DIR, 'outputs/')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
