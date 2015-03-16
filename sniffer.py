#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time
from mongodb import db
import sys


def query(method, args={}, access_token=''):
    pars = args
    #pars['access_token'] = unicode(access_token)
    pars['v'] = args.get('v', '5.14')
    prefix = 'https://api.vk.com/method/'
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
    	#print r.get('error')
        return r
    elif r.get('response') is not None:
        return r
    else:
        return None


if __name__ == "__main__":
	publics = json.loads(open('list.txt').read())
	pars = {
		'owner_id': 0,
		'count': 100,
	}
	
	for public in publics:
		pars['owner_id'] = -public['vk_id']
		resp = query('wall.get', pars)
		if resp is None:
			time.sleep(5)
			continue
		resp = resp.get('response')
		if resp is None:
			time.sleep(5)
			continue
		posts = resp['items']
		#print public['caption'] + u', ' + unicode(public['quantity']) + u' members'
		snapshot = {
			'public_id': public['vk_id'],
			'time_diff': 0,
			'likes_count': 0,
			'reposts_count': 0,
			'comments_count': 0
		}
		for post in posts:
			curtime = int(time.time())
			snapshot['time_diff'] = curtime - post['date'] 
			now = time.gmtime(curtime)
			snapshot['view_time'] = now.tm_sec + 60 * (now.tm_min + 60 * now.tm_hour)
			snapshot['post_id'] = post['id']
			if post.get('likes') and post.get('comments') and post.get('reposts'):
				snapshot['likes_count'] = post['likes'].get('count') or 0
				snapshot['reposts_count'] = post['reposts'].get('count') or 0
				snapshot['comments_count'] = post['comments'].get('count') or 0
				db.publics_stats.insert(snapshot)
				del snapshot['_id']
		time.sleep(1)

