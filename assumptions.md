- DM Leave and DM Details
dm/leave/v1 and dm/details/v1; Since dm_details requires that the token supplied correlate to a member of the given DM, when everyone leaves a dm thru dm/leave/v1, there is no way to blackbox check that there are no members of the dm remaining, even though the DM still exists; using dm/details/v1 in an attempt to access the dm's data as a member.

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

Users/Stats:
    - For seams stats, since admin/remove does not decrease the number of messages sent in the seams system, calling admin remove in where the removed user has sent multiple messages does not create a new timestamped data dict for messages_exist in workspace_stats.


message/share:
    - The original message is at the front, while the optional added comment is placed after the original message with a space in between. 

notifications for tagging:
    - Edited messages can tag people.
    - Similarly, shared messages with a tag can tag people. 
    - Standups do NOT tag people.


