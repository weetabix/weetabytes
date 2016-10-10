#!/usr/bin/python3
import todoist
import json
import re
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description="Test")
parser.parse_args()

api = todoist.TodoistAPI('46f1e8330b161e70ba2be0c608b84ceb4ed8f043')
api.reset_state()
results=api.sync(commands=[])

# Header

print(' {0:^3} ┊{2:<3}┊ {1:^40} {3:^}'.format("","Task Notes","⬆@@","Proje##"))
print(' {:┉^3} ┊{:┉<3}┊ {:┉^40} {:┉^7}'.format("","","",""))


def task_list():

    for i in range(0,len(results['items'])):
        if results['items'][i]['item_order'] != 14:
            prio = "➡" * (results['items'][i]['priority'] - 1)
    #        prio = "▬" * (results['items'][i]['priority'] - 1)
            for j in range(0,len(results['projects'])):
                if results['items'][i]['project_id'] == results['projects'][j]['id']:
                    proj = results['projects'][j]['name']
            print(' {0:<3d} ┊{2:<3}┊ {1:40} {3}'.format(i,results['items'][i]['content'],prio,proj))

def task_add():
    item = api.items.add('Task21','Project', priority=?)                                                                                       
    api.commit()
    projre = re.compile('##(.+?\b)')
    prire = re.compile('%%(\d{1})')
    
def main():
    task_list()



