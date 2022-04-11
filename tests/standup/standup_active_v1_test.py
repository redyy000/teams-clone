import pytest
import src.standup
import src.error

@pytest.fixture
def init_function():
    pass
    #register user
    #make channels
    #start standup

def test_standup_active_channel_invalid():
    #channel id invalid --> input error
    pass

def test_standup_active_invalid_token():
    #test token invalid --> access error
    pass

def test_standup_active_user_invalid():
    #test user not in channel --> access error
    pass

def test_standup_active_success():
    #note thread test time < 3 seconds

    #test endpoints
    #test shows correct status when active
    #test shows correct status when invalid 
    pass
