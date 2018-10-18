#!/usr/bin/env python3
import os, json
from pyquery import PyQuery
from pprint import pprint

data = {    "name": "Encyclopedia",
            "parent": "null",
            "children": []
}

websites={
}

dir_path = os.path.dirname(os.path.realpath(__file__))

def query_html(filename): # query html file to get info
    file_html_src = (open(dir_path + '/' +filename, 'r')).read()
    dom = PyQuery(file_html_src)
    title = dom("#title").text() if dom("#title").text() else 'Missing Title' 
    author = dom("#author").text() if dom("#author").text() else 'Missing Author'
    onsubject = dom("#onsubject").text() if dom("#onsubject").text() else 'Missing Parent Topic' #if no onsubject give it Missing Parent Topic
    return title, author, onsubject


for root, dirs, files in os.walk(dir_path): # find all html files in subfolders
    for f in files:
        if '.html' in f and dir_path is not root and f[0] is not '.':
            #print(f)            
            directory =  (root.replace(dir_path, ''))[1:]  +'/'
            file_relative_path = ( directory + f )
            title, author, onsubject = query_html(filename=file_relative_path)
            # populate websites dict
            websites[f]={'path': file_relative_path,
                         'title': title, # get title from querying page
                         'author': author,# get author from querying page
                         'onsubject': onsubject
            }
            #print(file_relative_path )

            
onsubject = []
for website in websites.keys(): # search for onsubject
    #print ( websites[website], websites[website]['onsubject'], '\n\n' )
    if websites[website]['onsubject'] is not '' and  websites[website]['onsubject']:
        onsubject.append(websites[website]['onsubject'])
onsubject = list(set(onsubject)) # remove duplicates

# populate the data dictionary by adding th subject (children of Encyclopedia, parent of entries)
for subject in onsubject:
    #print(subject)
    data['children'].append({
        "name": subject,
        "parent": "Encyclopedia",
        "children": []
    })

# populating the dictionay for tree.json
for website in websites.keys(): # loop through all websites
    subject =  websites[website]['onsubject']
    websites[website]
    print('subject:',subject)

    for data_topic in data['children']: # at each subject # loop through the  
        print('data_topic:',data_topic['name'])        
        if subject in data_topic['name']:
            print ('YES',data_topic['name'])
            data_topic['children'].append({
                'parent': subject,
                'name': websites[website]['title'],
                'author': websites[website]['author'],
                'path':  websites[website]['path']
            })
        
        
#pprint(data)

f = open(dir_path + '/' +'tree.json', 'w')
json.dump(data, f, indent=4)
f.close()

