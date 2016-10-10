#!/usr/bin/python3
import todoist
import json
import re
from pprint import pprint
import argparse
import time

task = ""
project = ""
priority = None
parser = argparse.ArgumentParser(description='A tool to allow you to add and list tasks from Todoist.\
                                             The default behaviour is to list your tasks.')
parser.add_argument('-a', '--add', help='Add task', action='store', dest='task',nargs='*')
parser.add_argument('-p','--project', help='Project (Default Inbox)', action='store', dest='project', default="Inbox")
parser.add_argument('-P','--priority', help='Priority (Default None)', type=int, action='store', dest='priority',default=2)

#parser.add_argument('task', help='Add task', action='store')

args = parser.parse_args()
print(args)
api = todoist.TodoistAPI('46f1e8330b161e70ba2be0c608b84ceb4ed8f043')
api.reset_state()
results=api.sync(commands=[])


def reset_sync():

    api.reset_state()                                                                                                
    results=api.sync(commands=[])  
    print("Reset")
    return results


def task_list():

    print(' {0:^3} ┊{2:<3}┊ {1:^40} {3:^}'.format("","Task Notes","⬆@@","Proje##"))
    print(' {:┉^3} ┊{:┉<3}┊ {:┉^40} {:┉^7}'.format("","","",""))
    for i in range(0,len(results['items'])):
        if results['items'][i]['item_order'] != 14:
            prio = "➡" * (results['items'][i]['priority'] - 1)
            for j in range(0,len(results['projects'])):
                if results['items'][i]['project_id'] == results['projects'][j]['id']:
                    proj = results['projects'][j]['name']
            print(' {0:<3d} ┊{2:<3}┊ {1:40} {3}'.format(i,results['items'][i]['content'],prio,proj))


def task_add(task_list,project,priority):
    print("task_add")
    task = (" ".join(task_list))
    print("task",task)
    print("project",project)
    print("priority",priority)

    for j in range(0,len(results['projects'])):
        if results['projects'][j]['name'] == project:
            proj = results['projects'][j]['id']
    print("proj: ",proj)
    item = api.items.add(task,proj,priority=priority)    
    api.commit()


if args.task:
    task_add(args.task,args.project,args.priority)
    results = reset_sync()
    task_list()
else:
    task_list()
