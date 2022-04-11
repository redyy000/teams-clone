import os
import json
from datetime import timezone
import datetime
'''

data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''


dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
time_stamp = int(utc_time.timestamp())

# YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [],
    'dms': [],
    'message_ids': [
        {
            # Unique universal message id
            'message_id': 0,
            # Message type: 1 for channels, 2 for dms
            'message_type': 1,
            # Channel id or dm id
            'source_id': 0
        }

    ],
    'workspace_stats': {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_stamp}],
        'utilization_rate': 0,
    }
}

# YOU SHOULD MODIFY THIS OBJECT ABOVE

# YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH


class Datastore:

    def __init__(self):

        # If the file already exists, then we load that in
        if os.path.exists('src/data.json') and os.stat("src/data.json") != 0:
            with open('src/data.json', 'r', encoding="utf8") as input_file:
                data = json.load(input_file)
        else:
            # Else we use the initial object
            with open('src/data.json', 'w', encoding="utf8") as input_file:
                # Put the initial object into the FILE
                json.dump(initial_object, input_file)
                data = initial_object

        self.__store = data

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

    def save(self):
        data = self.__store

        with open('src/data.json', 'w', encoding="utf8") as input_file:

            json.dump(data, input_file, indent=4)


print('Loading Datastore...')

global data_store
data_store = Datastore()
