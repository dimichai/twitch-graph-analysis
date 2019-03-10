import sys
import json
from followers_miner import FollowersMiner

def read_lines_from_file(filename):
    with open(filename) as f:
        values = f.readlines()
    values = [x.strip() for x in values]
    return values


def read_json_from_file(filename):
    input_file = open(filename)
    json_data = json.load(input_file)
    return json_data


if __name__ == '__main__':
    # args should contain the twitch client ID, the token file and the filename of the streamer's names
    if len(sys.argv) < 3:
        print('Arguments should be in the following format: [client_id] [token_file] [usernames_file].')
    else:
        clientid = sys.argv[1]
        token_file = sys.argv[2]
        usernames_file = sys.argv[3]

        tokens = read_lines_from_file(token_file)
        usernames = read_json_from_file(usernames_file)

        for user in usernames:
            username = user['name']
            print('Mining followes of: ' + username)
            miner = FollowersMiner(clientid, tokens, username, 1000, None)
            miner.mine_followers()
