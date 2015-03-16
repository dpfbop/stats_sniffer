#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

def query(method, args={}):
    pars = args
    prefix = 'http://allsocial.ru/'
    timeout = 2
    try:
        r = requests.get(unicode(prefix + method), params=pars, timeout=timeout)
    except Exception as e:
        return None
    try:
        r = r.json()
    except:
        return None

    if r.get('error') is not None:
        return r
    elif r.get('response') is not None:
        return r
    else:
        return None

if __name__ == "__main__":
	pars = {
		'direction':1,
		'is_closed':-1,
		'list_type':1,
		'offset':0,
		'order_by':'quantity',
		'period':'day',
		'platform':1,
		'range':'1000000:6342150',
		'type_id':-1
	}
	publics = []
	for offset in range(0, 500, 25):
		pars['offset'] = offset
		publics += query('entity', pars)['response']['entity']

	print len(publics)
	for i in range(len(publics)):
		print unicode(i + 1) + u': ' + unicode(publics[i]['caption'])


	f = open('list.txt', 'w+')
	f.write(json.dumps(publics))
