from steam import Steam
#from decouple import config

class SteamApi:

    def __init__(self):
        self._steam = Steam("XXX") #NOTE: issues with .env need to hardcode the key for now

    def get_user(self):
        return UserSearch()
    
    def get_user_info(self):
        return UserInfo()

class UserSearch(SteamApi):

    def __init__(self):
        super().__init__()

    def by_url_id(self, username: str) -> dict:
        user = self._steam.users.search_user(username)
        return user
    
class UserInfo(SteamApi):
    
    def __init__(self):
        super().__init__()

    def basic_info(self, steam_id: str) -> dict:
        user = self._steam.users.get_user_details(steam_id)
        return user
    
    def recently_played_games(self, steam_id: str) -> dict:
        user = self._steam.users.get_user_recently_played_games(steam_id)
        return user