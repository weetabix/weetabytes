#!/usr/bin/python2.7

# Ryan Weetabix Parkyn 2013 

# Free to use with attribution.

import requests
import re
from bs4 import BeautifulSoup
 
lstfile = open('C:/dir/to/where/you/want/files/', 'w') # Location of where to write data
 
def main():
    headers = {'Accept': 'application/*+xml;version=1.5', 'Host': 'my fqdn'}
    params = {'pageSize': '150', 'type': 'vApp', 'format': 'idrecords'}
    auth = ('username@vdc', 'password')
    proxies = {"https": "https://proxyURL:80/"} #remove proxies=proxies if no proxy
    s = requests.Session()
    r = s.post('https://vcd1.dell.com/api/sessions', proxies=proxies, headers=headers, \
               verify=True, auth=auth)
    s.headers.update({'x-vcloud-authorization': r.headers['x-vcloud-authorization']})
    t = s.get('https://vcd1.dell.com/api/query?', proxies=proxies, headers=headers, \
              verify=True, params=params)
 
    for line in t.iter_lines():
        if line:
            parse(line)
 
def parse(text=""):
    soup = BeautifulSoup(text, "xml")
    tags = soup.find_all('VAppRecord')
    for tag in tags:
        toprint = []
        for attr in ['name', 'networkName', 'id', 'taskStatusName', 'memoryAllocationMB']:
            if attr in tag.attrs:
                toprint.append((attr, tag[attr]))
 
        nsname = re.sub(" ", "_", toprint[0][1]) #remove spaces from names
        lstfile.write(toprint)
 
main()
lstfile.close()
