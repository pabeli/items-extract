from logging import error
import pandas as pd
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

def load_data(df: pd.DataFrame):
    try:
        df.to_csv('items_data.csv', index=False)
    except:
        logging.info('Something bad happened')