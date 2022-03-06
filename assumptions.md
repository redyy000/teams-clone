auth.py:
    - auth_register_v1:
        - In testing handles, handles must be compared to pre-existing handles. 
        - In doing so, testing requires the access of datastore to iterate and compare to other handle
        - Hence handle-related testing specifically is not black-box, relying on how our group's data is stored.
        
