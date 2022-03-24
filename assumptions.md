- DM Leave and DM Details
dm/leave/v1 and dm/details/v1; Since dm_details requires that the token supplied correlate to a member of the given DM, when everyone leaves a dm thru dm/leave/v1, there is no way to blackbox check that there are no members of the dm remaining, even though the DM still exists; using dm/details/v1 in an attempt to access the dm's data as a member.

- User 'user' dictionaries
user/profile/v1: The returned 'user' dictionary has key values:
    'user': {
        'u_id': u_id,
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
    }

Similarly, the users/all/v1 path returns a list of these 'user' dictionary as the value stored in key 'users'

- Time_sent
The 'time_sent' value for messages is int(utc_timestamp), where utc_timestamp is retrieved from the following code from https://www.geeksforgeeks.org/get-utc-timestamp-in-python/, as listed in the specification. 

from datetime import timezone
import datetime
# Getting the current date
# and time
dt = datetime.datetime.now(timezone.utc)
  
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()
  
print(utc_timestamp)

- 

