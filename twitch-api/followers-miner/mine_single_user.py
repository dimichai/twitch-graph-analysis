import sys
from .followers_miner import FollowersMiner

if __name__ == '__main__':
    # args should contain the twitch client ID and starting point username e.g. "shroud"
    if len(sys.argv) < 3:
        print('Arguments should be in the following format: [client_id] [token_file] [start_username].')
    else:
        clientid = sys.argv[1]
        token_file = sys.argv[2]
        start = sys.argv[3]

        with open(token_file) as f:
            tokens = f.readlines()

        tokens = [x.strip() for x in tokens]

        print('Mining begins from: ' + start)
        miner = FollowersMiner(clientid, tokens, start)
