'''
Created on Apr 17, 2018

@author: yingc
'''
a = [1,2,3]
print a[-1]
import json

with open('subm_index.txt', 'r') as f:
    line = f.read()
    line ={"data": {"test": 1, "hello": "I have r\" !"}, "id": 4}
    print line
    #line = line.replace('\0', '')

    print line
    data_item = json.loads(line)
    #subreddit_id = (data_item['subreddit_id'].split('_', 1)[-1]).encode('utf-8')
    print data_item