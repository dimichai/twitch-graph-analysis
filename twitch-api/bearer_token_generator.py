import string
import sys
import requests


class BearerTokenGenerator:
    ID_ENDPOINT = 'https://id.twitch.tv/oauth2/token'
    client_ids: []
    output_file: string

    def __init__(self, client_ids, output_file):
        self.client_ids = client_ids
        self.output_file = output_file

    def generate_bearer_tokens(self):
        for client_id, secret in clientids:
            print('Generating token for ' + client_id + ' - ' + secret)
            url = f'{self.ID_ENDPOINT}'
            data = {
                'client_id': client_id,
                'client_secret': secret,
                'grant_type': 'client_credentials'
            }
            r = requests.post(url, data=data)
            json = r.json()
            print(json)


if __name__ == '__main__':
    # args should contain the input file (client_ids) and the output file (bearer_tokens file)
    if len(sys.argv) < 2:
        print('You should specify input file (client_ids) and the output file (bearer_tokens file).')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        with open(input_file) as f:
            clientids = f.readlines()

            # you may also want to remove whitespace characters like `\n` at the end of each line
            clientids = [(x.split(';')[0], x.split(';')[1]) for x in clientids]

        generator = BearerTokenGenerator(clientids, sys.argv[2])
        generator.generate_bearer_tokens()
