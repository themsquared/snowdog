import json
import os
import requests

from datadog import initialize, api

LIMIT = os.getenv('LIMIT', 0) 

DD_API_KEY = os.getenv('DD_API_KEY', '<YOUR_API_KEY>')
DD_APP_KEY = os.getenv('DD_APP_KEY', '<YOUR_APP_KEY>')

BASE_URL = 'https://' + os.getenv('SERVICENOW_INSTANCE', 'instance_id') + \
           '.service-now.com/api/now/table/cmdb_ci_linux_server?sysparm_query=host_name='
SNOW_USER = 'admin'
SNOW_PWD = os.getenv('SERVICENOW_PASS', 'password')
SNOW_HEADERS = {"Accept":"application/json"}

def get_dd_host_tags(host):
    res = api.Tag.get(host)
    if res and res.get('tags', None):
        return res['tags']
    return []

def set_dd_host_tags(host, tags):
    res = api.Tag.update(host, tags=tags)
    if res and res.get('host', None):
        print 'Success updating {} tags:'.format(res['host'])
        print res['tags']

def combine_tags(dog_tags, snow_tags):
    # TODO: Dedupe and determine if key:values should be overwritten or cumulative
    return dog_tags + snow_tags

def get_snow_host(hostname):
    snow_url = BASE_URL + hostname
    response = requests.get(snow_url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS)
    if response.status_code != 200:
        print 'Error: {} {}'.format(response.status_code, response.json())
        return {}
    return response.json()

if __name__ == '__main__':
    options = {
        'api_key': DD_API_KEY,
        'app_key': DD_APP_KEY
    }

    initialize(**options)

    hosts = api.Infrastructure.search(q='hosts:')['results']['hosts']
    
    cnt = 0
    for host in hosts:
        if cnt >= LIMIT && LIMIT > 0: # Only helpful for testing.
           break # Bail out. We hit our limit.

        print 'Querying ServiceNow for host {}'.format(host)
        snow_tags = []
        host_json = get_snow_host(host)
        if host_json.get('result', None):
            result = host_json['result'][0]
            for k, v in result.iteritems():
                if v and not isinstance(v, dict):
                    snow_tags.append('{}:{}'.format(k, v))

        dog_tags = []
        if len(snow_tags):
            dog_tags = get_dd_host_tags(host)

        new_tags = combine_tags(dog_tags, snow_tags)
        set_dd_host_tags(host, new_tags)
        cnt += 1
