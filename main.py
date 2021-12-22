from utils.extract import request_data
from utils.load import load_data

import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

if __name__ == '__main__':

    # The extract process
    logging.info('Starting extract data...')
    items_data = request_data()

    # Downloading information into csv
    logging.info('Starting download process...')
    load_data(items_data)
    