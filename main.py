import requests
import json
import os
from datetime import datetime
from datetime import timedelta

class TDClient:
    
    AUTH_URL = 'https://api.tdameritrade.com/v1/oauth2/token'
    CONFIG_DATA = {}
    CONFIG_JSON_FILE = 'config.json'

    def get_config(self):
        if os.path.exists(self.CONFIG_JSON_FILE):
            self.CONFIG_DATA = json.load(open(self.CONFIG_JSON_FILE))
            if self._check_token_expiry():
                self._get_new_token()
        else:
            print('No config file found!')
        return self.CONFIG_DATA


    def _check_token_expiry(self):
        cur_timestamp = datetime.timestamp(datetime.now())
        if float(self.CONFIG_DATA['token_expiry']) > cur_timestamp:
            return False
        else:
            return True


    def _get_new_token(self):
        try:
            del self.CONFIG_DATA['token_expiry']
            del self.CONFIG_DATA['access_token']
            res = requests.post(url=self.AUTH_URL, data=self.CONFIG_DATA)
            res = res.json()
            token_expiry = datetime.now() + timedelta(days=89)
            token_expiry = datetime.timestamp(token_expiry)
            self._save_new_param(res, token_expiry)
        except requests.exceptions.RequestException as err: #TODO: add more specific exception handling
            raise SystemExit(err)


    def _save_new_param(self, res_text, token_expiry):
        
        self.CONFIG_DATA['refresh_token'] = res_text['refresh_token']
        self.CONFIG_DATA['access_token'] = res_text['access_token']
        self.CONFIG_DATA['token_expiry'] = str(token_expiry)
        with open(self.CONFIG_JSON_FILE, 'w') as config_json_file:
            json.dump(self.CONFIG_DATA, config_json_file)


if __name__ == '__main__':
    tdClient = TDClient()
    config = tdClient.get_config()
    print(config['access_token'])
