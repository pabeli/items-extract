import pandas as pd
import requests
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

def request_data():
    """
    Function that performs the request to MeLi's API
    """
    # The elements we're going to download information
    elements = ['amazon fire tv', 'google home', 'apple tv', 'firetv stick']
    # The dictionary where responses will be stored
    responses = {}
    # For every element picked, the request must be performed
    for element in elements:
        try:
            r = requests.get(
                f"https://api.mercadolibre.com/sites/MLA/search?q={element}&limit=50#json"
            )
        except:
            logging.info(f'Something happened with element {element}')
        # If the request is successfull, the element information will be added
        responses[element] = r.json()
    
    # We pick the columns to be saved
    # Other columns could be added here
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
    
    # Create the dataframe
    df = pd.DataFrame(columns=columns)
    # Set its index
    df.set_index('id')

    # The rows will be saved in this array
    rows = []
    # For every element we asked
    for element in elements:
        # For very item in that element
        for item in responses[element]['results']:
            # Try to perform the request
            try:
                r = requests.get(
                    f"https://api.mercadolibre.com/items/{item['id']}"
                )
            except:
                logging.info(f"Something happened with item {item['id']}")
            
            # Check if the request returned something
            if r.json() is not None:
                response = r.json()
                # Save the data
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
                # Add the new row
                rows.append(row)
    # Create the rows dataframe
    rows_df = pd.DataFrame.from_records(rows)
    # Append to the already created dataframe
    df = df.append(rows_df)
    # Set the index
    df.set_index = 'id'
    return df

            
            