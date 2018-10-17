#!/usr/bin/env python3
from jinja2 import Template
import os
from pyquery import PyQuery


dir_path = os.path.dirname(os.path.realpath(__file__))

def query_html(filename):
    file_html_src = (open(dir_path + '/' +filename, 'r')).read()
    dom = PyQuery(file_html_src)
    title = dom("#title").text()
    author = dom("#author").text()
    onsubject = dom("#onsubject").text()
    return title, author, onsubject

with open(dir_path + '/' +'template.html') as file_:
        template = Template(file_.read())
        
websites={}
for root, dirs, files in os.walk(dir_path):
    for f in files:
        if '.html' in f and dir_path is not root and f[0] is not '.':
            #print(f)            
            directory =  (root.replace(dir_path, ''))[1:]  +'/'
            file_relative_path = ( directory + f )
            title, author, onsubject = query_html(filename=file_relative_path)

            websites[f]={'path': file_relative_path,
                         'title': title, # get title from querying page
                         'author': author,# get author from querying page
                         'onsubject': onsubject.title() #
            }
            #print(file_relative_path )


#print(websites)
onsubject = []

for website in websites.keys():
    #print ( websites[website], websites[website]['onsubject'], '\n\n' )
    if websites[website]['onsubject'] is not '' and  websites[website]['onsubject']:
        onsubject.append(websites[website]['onsubject'])


onsubject = list(set(onsubject)) # remove duplicates
#print(onsubject)


list_on_topic = Template('''
<h2 id="parenttopic">Entries According to Main Topic (h2 with id="ontopic")</h2>            
<ul>
{% for subject in onsubject %}
    <li><h3>{{ subject }}</h3>
    <ul> 
    {% for key, val in users.items() %}
       {% if val.onsubject == subject %}
         <li><b>Title:</b> 
         <a target="_new" href="{{val.path}}">
         {% if val.title|length > 0 %}
         {{ val.title }}
         {% else %}
         <s>Missing title</s>
         {% endif %}
         </a> 
              <b>Author:</b> 
                  {% if val.author|length > 0 %}
                  {{ val.author }}
                  {% else %}
                  <s>Missing author name</s>
                  {% endif %}
              <b>Main Topic</b> 
                  {% if val.onsubject|length > 0 %}
                  {{ val.onsubject }}
                  {% else %}
                  <s>Missing Parent topic (id="onsubject")</s>
                  {% endif %}
         </li>
       {% endif %}
    {% endfor %}
    </ul>          
    </li>
{% endfor %}
</ul>'''
)
#print(onsubject)


#print(list_on_topic_render)

list_all_entries = Template( '''
<h2 id="listall">List of All Entries</h2>            
<ul>
{% for key, val in users.items() %}
<li><b>Title:</b> 
<a target="_new" href="{{val.path}}">
{% if val.title|length > 0 %}
{{ val.title }}
{% else %}
<s>Missing title</s>
{% endif %}
</a> 
     <b>Author:</b> 
{% if val.author|length > 0 %}
{{ val.author }}
{% else %}
<s>Missing author name</s>
{% endif %}
 
     <b>Main Topic</b>{% if val.onsubject|length > 0 %}
{{ val.onsubject }}
{% else %}
<s>Missing Parent topic (id="onsubject")</s>
{% endif %}

</li>
  {% endfor %}
</ul>
''')

table_all_entries = Template( '''
<h2 id="table">Table of of All Entries</h2>            
<table id="myTable" class="tablesorter"> 
<thead> 
<tr> 
    <th>Title</th> 
    <th>Parent Topic (id="ontopic")</th> 
    <th>Author</th>

</tr> 
</thead> 
<tbody> 
{% for key, val in users.items() %}
<tr>
    <th>
     <a target="_new" href="{{val.path}}">
     {% if val.title|length > 0 %}
     {{ val.title }}
     {% else %}
     <s>Missing title</s>
     {% endif %}
     </a> 
    </th>

    <th>
     {% if val.onsubject|length > 0 %}
     {{ val.onsubject }}
     {% else %}
     <s>Missing Parent topic (id="onsubject")</s>
     {% endif %}
    </th>

    <th>     
     {% if val.author|length > 0 %}
     {{ val.author }}
     {% else %}
     <s>Missing author name</s>
     {% endif %}
    </th>
</tr>
{% endfor %}
<tbody> 
</table>
''')

list_on_topic_render = list_on_topic.render(onsubject=onsubject, users=websites)

table_html_render = table_all_entries.render(users=websites)
#print(table_html_render)

#list_html_render = list_all_entries.render(users=websites)
#print(list_html_render)


index = template.render(content= table_html_render + list_on_topic_render)
#print(index)

index_file = open('index-01.html','w')
index_file.write( index)
index_file.close()




