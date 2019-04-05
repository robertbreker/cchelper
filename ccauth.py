#!/usr/bin/env python

import pprint
import requests
import json


class CitrixCloudHelper(object):
    def __init__(self, trust_uri, customer_id, client_id, client_secret):
        self.headers = {"Content-Type": "application/json",
                        "Accept": "application/json"}
        self.authenticate(trust_uri, customer_id, client_id, client_secret)

    def authenticate(self, trust_uri, customer_id, client_id, client_secret):
        auth_data = {}
        auth_data['clientId'] = client_id
        auth_data['clientSecret'] = client_secret
        response = self.post(trust_uri, json.dumps(auth_data))
        if response.status_code == 200:
            result = json.loads(response.text)
            # Attach the bearer token to the header for future requests.
            self.headers['Authorization'] = ('CwsAuth Bearer=%s'
                                             % (result['token'])
        else:
            raise Exception("Failed to authenticate with Citrix Cloud."
                            + " Return code: %d" % (response.status_code))

    def get(self, uri):
        response = requests.get(uri, headers=self.headers)
        return response

    def post(self, uri, data):
        response = requests.post(uri, data=data, headers=self.headers)
        return response

    def delete(self, uri):
        response = requests.delete(uri, headers=self.headers)
        return response


def main():
    trust_uri = 'https://trust.citrixworkspacesapi.net/xsrbd0/tokens/clients'
    with open('../config.json') as config_json:
        config = json.load(config_json)

    cloud_helper = CitrixCloudHelper(trust_uri, config['customer_id'],
                                     config['client_id'],
                                     config['client_secret'])
    response = cloud_helper.get(
        "https://registry.citrixworkspacesapi.net/xsrbd0/resourcelocations")
    pprint.pprint(response.content)


if __name__ == "__main__":
    main()
