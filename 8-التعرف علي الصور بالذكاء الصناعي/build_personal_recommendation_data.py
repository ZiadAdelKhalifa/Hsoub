#the data will contain 33 column 32 for the train 1 for the meal_id as lable
#32 ,2 will be age and gender ,the 30 is the 30 distinct ingredients of the  all meals the client took
#these distinct columns will contain number 
# which means how many times this ingredients exsit in the all meals for the client  


import sqlite3

import pandas as pd


INGREDIENTS = sorted([
    'egg', 'chicken', 'rice', 'tomato', 'cheese', 'potato', 'onion', 'garlic', 'butter', 'corn',
    'lemon', 'cucumber', 'fish', 'pasta', 'spinach', 'ginger', 'parsley', 'carrot', 'cinnamon', 'olives',
    'eggplant', 'mushroom', 'bread', 'beef', 'chocolate', 'apple', 'banana', 'orange', 'broccoli', 'peas'
])

def __get_users_ids(cur):
    user_ids = [
        id[0]
        for id in cur.execute('SELECT DISTINCT user_id FROM cart_order').fetchall()
    ]
    return user_ids

#To extract the meals that contains all the ingredients that the user have  
def __extract_features(orders):
    features = [0] * len(INGREDIENTS)
    for order in orders:
        for i, ingredient in enumerate(INGREDIENTS):
            if ingredient in order:
                features[i] += 1
    
    return features


def __get_user_data(cur, user_id):

    def flatten_orders(orders):
        flattened_orders = []
        for order in orders:
            flattened_orders.extend([(order[1], order[2])]*order[0])
        return flattened_orders

    age, gender = cur.execute(
        f'SELECT age, gender FROM accounts_user WHERE id = {user_id}'
    ).fetchone()    

    orders = cur.execute(
        f'''
            SELECT quantity, ingredients, pages_meal.id
            FROM cart_order
            INNER JOIN pages_meal
            ON cart_order.meal_id = pages_meal.id
            WHERE user_id = {user_id}
        '''
    ).fetchall()

    # repeat by quantity, and keep only ingredients and meal id
    orders = flatten_orders(orders)

    user_data = []
    #so now i have all the orders for one client
    for i, order in enumerate(orders):
        #i will extract all the ingredients of all the meals for the client
        #  excapt the current meal which the model will try to predict the id of this meal

        masked_orders = [x[0] for x in orders[:i] + orders[i+1:]]#for example order num 6 
        #,will take the ingredients of all other orders for this person 
        #and label them with the current order

        features = __extract_features(masked_orders)
        label = order[1]  # meal id for the current order

        # append user info to the data
        features.extend([age, gender, label])
        user_data.append(features)

    return user_data


def __to_csv(data, path):
    columns = INGREDIENTS + ['age', 'gender', 'label']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path)


if __name__ == '__main__':
    conn = sqlite3.connect('food_app/db.sqlite3')
    cur = conn.cursor()

    user_ids = __get_users_ids(cur)

    data = []
    for user_id in user_ids:
        data.extend(__get_user_data(cur, user_id))

    __to_csv(data, 'data.csv')
