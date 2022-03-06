auth.py:
    - auth_register_v1:
        - In testing handles, handles must be compared to pre-existing handles. 
        - In doing so, testing requires the access of datastore to iterate and compare to other handle
        - Hence handle-related testing specifically is not black-box, relying on how our group's data is stored.
        
Assumptions for channels_create - Tayla:
auth_user_id begins at 1, remains only positive integers.
Channel name can include spaces, letters, numbers and alphanumerics, but 1>=length<21
Channel name cannot be duplicate
All other functions work / are functional
