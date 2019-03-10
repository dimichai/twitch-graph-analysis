import json
import string
import requests
import time


class FollowersMiner:
    USERS_ENDPOINT = 'https://api.twitch.tv/helix/users'
    client_id: string
    mined_users = []
    access_tokens = []
    start_point: string
    mined_limit: int
    cursor: string

    def __init__(self,
                 client_id: string,
                 access_tokens: list,
                 start_point: string,
                 mined_limit: int,
                 cursor: string):
        """
        :param client_id: string the client id
        :param access_tokens: list of bearer tokens to use in the pool
        :param start_point: string the username of the channel to mine followers from
        :param mined_limit: int limit the number of users mined
        :param cursor: the pagination cursor for resuming the mining
        """
        self.client_id = client_id
        self.start_point = start_point
        self.access_tokens = access_tokens
        self.current_token_index = 0
        self.mined_limit = mined_limit
        self.cursor = cursor

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

    def _get_current_token(self) -> string:
        """
        Returns the current bearer token in the rolling tokens pool.
        :return:
        """
        if self.current_token_index > len(self.access_tokens) - 1:
            self.current_token_index = [0]
        return self.access_tokens[self.current_token_index]

    def mine_followers(self):
        user_id = self.get_userid_by_login(self.start_point)
        # Pagination cursor from Twitch API
        total_mined = 0
        valid_requests = 0

        start_time = time.time()
        while total_mined < self.mined_limit:
            url = f'{self.USERS_ENDPOINT}/follows?to_id={user_id}'
            if self.cursor:
                url += '&after=' + self.cursor

            print('Sending request to: ' + url)

            headers = {'Authorization': 'Bearer ' + self._get_current_token()}
            r = requests.get(url, headers=headers)
            json_data = r.json()
            try:
                self.cursor = json_data['pagination']['cursor']
                valid_requests += 1

                # for user in json_data['data']:
                with open('data/' + self.start_point + '.json', 'w') as f:
                    json.dump(json_data['data'], f)

                    total_mined += 20

                print('Mined so far: ' + str(total_mined))
            except:
                print(json_data)
                if json_data['error']:
                    # Update current token index
                    print('Timed out - Switching to the next token.')
                    self.current_token_index += 1

        end_time = time.time()
        print('Total users mined: ' + str(total_mined))
        print('Total valid requests: ' + str(valid_requests))
        print('Total time elapsed:' + str(end_time - start_time))
        print('Cursor to use for the next request: ' + self.cursor)
