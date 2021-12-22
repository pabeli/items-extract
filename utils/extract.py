import os
import pandas as pd
import requests
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

def request_data():
    elements = ['amazon fire tv', 'google home', 'apple tv', 'firetv stick']
    responses = {}
    for element in elements:
        try:
            r = requests.get(
                f"https://api.mercadolibre.com/sites/MLA/search?q={element}&limit=50#json"
            )
        except:
            logging.info(f'Something happened with element {element}')
        
        responses[element] = r.json()
    
    # Columns to be saved
    columns = [
        "id",
        "title",
        "seller_id",
        "price",
        "currency_id",
        "initial_quantity",
        "available_quantity",
        "sold_quantity",
        "condition",
        "accepts_mercadopago",
        ]
    
    df = pd.DataFrame(columns=columns)
    df.set_index('id')

    rows = []
    for element in elements:
        
        for item in responses[element]['results']:
            try:
                r = requests.get(
                    f"https://api.mercadolibre.com/items/{item['id']}"
                )
            except:
                logging.info(f"Something happened with item {item['id']}")
        
            if r.json() is not None:
                response = r.json()
                row = {
                    "id": response['id'],
                    "title": response['title'],
                    "seller_id": response['seller_id'],
                    "price": response['price'],
                    "currency_id": response['currency_id'],
                    "initial_quantity": response['initial_quantity'],
                    "available_quantity": response['available_quantity'],
                    "sold_quantity": response['sold_quantity'],
                    "condition": response['condition'],
                    "accepts_mercadopago": response['accepts_mercadopago']
                }

                rows.append(row)
    
    rows_df = pd.DataFrame.from_records(rows)
    df = df.append(rows_df)
    df.set_index = 'id'
    return df

            
            