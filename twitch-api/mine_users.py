import string
import sys

import requests


class TwitchUsersMiner:
    USERS_ENDPOINT = 'https://api.twitch.tv/helix/users'
    mined_users = []
    client_id: string
    start_point: string

    def __init__(self, client_id, start_point):
        self.client_id = client_id
        self.start_point = start_point

        user_id = self.get_userid_by_login(start_point)
        self.mine_followers(user_id)

    def get_userid_by_login(self, login):
        """
        Returns the user id of the specified login name.
        :param login: the username whose id will be returned.
        :return: twitch user id of the specified user
        """

        url = f'{self.USERS_ENDPOINT}?login={self.start_point}'
        if login:
            r = requests.get(url, headers={'Client-ID': self.client_id})
            json = r.json()
            if json['data']:
                if len(json['data']) > 0:
                    return json['data'][0]['id']
        return None

    def mine_followers(self, user_id):

        pass


if __name__ == '__main__':
    # args should contain the twitch client ID and starting point username e.g. "shroud"
    if len(sys.argv) < 2:
        print('Client id and starting username not specified.')
    else:
        print('Mining begins from: ' + sys.argv[2])
        miner = TwitchUsersMiner(sys.argv[1], sys.argv[2])
