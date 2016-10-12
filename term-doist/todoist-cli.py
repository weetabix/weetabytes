#!/usr/bin/python3
import todoist
import json
import re
from pprint import pprint
import argparse
import time

#import api key
import sys
sys.path.insert(0, '/etc/todoist-cli/')
import tcconfig

task = ""
project = ""
priority = None

parser = argparse.ArgumentParser(description='A tool to allow you to add and list tasks from Todoist.\
                                             The default behaviour is to list your tasks. (defaults) are in ()\'s. ')
parser.add_argument('-a', '--add', 
        help='Add task', 
        action='store',
        dest='task',
        nargs='*')
parser.add_argument('-p','--project',
        help='Project (Inbox)',
        action='store',
        dest='project',
        default="Inbox")
parser.add_argument('-P','--priority', 
        help='Priority 1 - 4 Low Med High Urgent (1 "Low Energy")', 
        type=int,
        action='store', 
        dest='priority',
        default=1)

args = parser.parse_args()

#Get a first run of the sync results.
api = todoist.TodoistAPI(tcconfig.api_key)
api.reset_state()
results=api.sync(commands=[])


def reset_sync():
    """Reset the sync state and repull results."""
    api.reset_state()                                                                                                
    results=api.sync(commands=[])  
    print("Reset")
    return results


def task_list():
    """Retrive and print a task list."""
    print(' {0:^3} ┊{2:<3}┊ {1:^40} {3:^}'.format("","Task Notes","Pr⬆","Project"))
    print(' {:┉^3} ┊{:┉<3}┊ {:┉^40} {:┉^7}'.format("","","",""))
    for i in range(0,len(results['items'])):
        if results['items'][i]['item_order'] != 14:
            prio = "➡" * (results['items'][i]['priority'] - 1)
            for j in range(0,len(results['projects'])):
                if results['items'][i]['project_id'] == results['projects'][j]['id']:
                    proj = results['projects'][j]['name']
            print(' {0:<3d} ┊{2:<3}┊ {1:40} {3}'.format(i,results['items'][i]['content'],prio,proj))


def task_add(task_list,project,priority):
    """Add a task to the list."""
    print("task added")
    task = (" ".join(task_list))
    print("task",task)
    print("priority",priority)

    for j in range(0,len(results['projects'])):
        if results['projects'][j]['name'] == project:
            proj = results['projects'][j]['id']
    print("proj:",project,"(",proj,")")
    item = api.items.add(task,proj,priority=priority)    
    api.commit()


if args.task:
    task_add(args.task,args.project,args.priority)
#    results = reset_sync()
#    task_list()
else:
    task_list()
