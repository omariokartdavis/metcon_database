
# coding: utf-8

# Full working code listed first. Steps shown after. The code will pull all workouts from 2018 and 2017 on crossfit.com/workout/ while skipping rest days and unnecessary content.

# In[100]:


import urllib.request
from bs4 import BeautifulSoup as bs
import re

# code for 2018
page_number = 1
while page_number <= 12:
    mainsite_workouts = '{}{}'.format("https://www.crossfit.com/workout/2018?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page)
    
    for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        for day in eachworkout.select('h3'):
            print(day.get_text())
        for paragraph in eachworkout.select('p'):
            if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare')):
                continue
            print(paragraph.get_text())
    page_number += 1

# code for 2017. difference is the skip parameters for paragraphs. 2017 pages use different layout of scaling and tips etc.
page_number = 1
while page_number <= 12:
    mainsite_workouts = '{}{}'.format("https://www.crossfit.com/workout/2017?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page)
    
    for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        for day in eachworkout.select('h3'):
            print(day.get_text())
        for paragraph in eachworkout.select('p'):
            if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare|Post|Tips and Scaling')):
                continue
            print(paragraph.get_text())
    page_number += 1


# In[2]:


import urllib.request


# In[3]:


from bs4 import BeautifulSoup as bs


# In[93]:


mainsite_workouts = "https://www.crossfit.com/workout/"


# In[94]:


page = urllib.request.urlopen(mainsite_workouts)


# In[95]:


soup = bs(page)


# In[7]:


print(soup.prettify())


# In[9]:


print(soup.get_text())


# In[11]:


soup.title


# In[47]:


soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling


# In[59]:


for eachpart in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class*="content"]'):
    print(eachpart.get_text())


# In[64]:


for eachpart in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-sm-6"]'):
    print(eachpart.get_text())


# In[48]:


import re


# In[49]:


for eachpart in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-sm-6"]'):
    for paragraph in eachpart.select('p'):
        if paragraph.find_all(string=re.compile("Related")):
            continue
        print(paragraph.get_text())


# The above code works to pull all text data for workouts and gets rid of the "Related content" posts.
# Next step is to figure out how to also get rid of "Rest Day" posts

# In[63]:


for eachpart in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-sm-6"]'):
    for paragraph in eachpart.select('p'):
        if paragraph.find_all(string=re.compile('Related|Rest Day|\"|Post thoughts to comments|Scroll for scaling options')):
            continue
        print(paragraph.get_text())


# The above code gets all metcon text from crossfit.com/workout/ and removes any rest days and unneccessary comments from the posts. Next step is to find out how to keep the day and date info with each post, but not to duplicate the day and date since each workout has two seperate columns that get "found" (The workout and then the scaling)

# In[67]:


for eachpart in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-sm-6"]'):
    print(eachpart.parent.previous_sibling.previous_sibling.get_text())


# In[72]:


for eachworkout in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
    for day in eachworkout.select('h3'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        print(day.get_text())


# The below code works to pull every workout for the past month from crossfit.com/workout/. It will skip over any rest days and unneccessary comments such as "Related Content" that would link to technique posts for movements.

# In[73]:


for eachworkout in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
    for day in eachworkout.select('h3'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        print(day.get_text())
    for paragraph in eachworkout.select('p'):
        if paragraph.find_all(string=re.compile('Related|Rest Day|\"|Post thoughts to comments|Scroll for scaling options')):
            continue
        print(paragraph.get_text())


# The below code works to pull every workout for the past month from crossfit.com/workout/. It will skip over any rest days and unneccessary comments such as "Related Content" that would link to technique posts for movements.

# In[80]:


import urllib.request
from bs4 import BeautifulSoup as bs
import re

mainsite_workouts = "https://www.crossfit.com/workout/"
page = urllib.request.urlopen(mainsite_workouts)
soup = bs(page)

for eachworkout in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
    if eachworkout.find_all(string=re.compile('Rest Day')):
        continue
    for day in eachworkout.select('h3'):
        print(day.get_text())
    for paragraph in eachworkout.select('p'):
        if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare')):
            continue
        print(paragraph.get_text())


# Next steps: get BeautifulSoup to scroll the web page

# In[88]:


page_number=1
while page_number < 12:
    print('{}{}'.format("https://www.crossfit.com/workout/2018?page=", page_number))
    page_number += 1


# The below code loads all workouts from 2018 from crossfit.com/workouts/. Skipping rest days and unnecessary content

# In[90]:


page_number = 1
while page_number <= 12:
    mainsite_workouts = '{}{}'.format("https://www.crossfit.com/workout/2018?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page)
    
    for eachworkout in soup.body.div.next_sibling.next_sibling.section.next_sibling.next_sibling.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        for day in eachworkout.select('h3'):
            print(day.get_text())
        for paragraph in eachworkout.select('p'):
            if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare')):
                continue
            print(paragraph.get_text())
    page_number += 1


# Next steps: simplify
# 
# the `soup.body.div...` line does not need all the identifiers of the above code as the sections I'm looking for on the page are the only ones with that specific class identifier. Therefore I can just use `soup.select()`

# In[96]:


for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
    if eachworkout.find_all(string=re.compile('Rest Day')):
        continue
    for day in eachworkout.select('h3'):
        print(day.get_text())
    for paragraph in eachworkout.select('p'):
        if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare')):
            continue
        print(paragraph.get_text())


# In[97]:


page_number = 1
while page_number <= 12:
    mainsite_workouts = '{}{}'.format("https://www.crossfit.com/workout/2018?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page)
    
    for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        for day in eachworkout.select('h3'):
            print(day.get_text())
        for paragraph in eachworkout.select('p'):
            if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare')):
                continue
            print(paragraph.get_text())
    page_number += 1


# Next steps: make it work for 2017. 2017 page uses different tips and scaling paragraphs.

# In[99]:


page_number = 1
while page_number <= 12:
    mainsite_workouts = '{}{}'.format("https://www.crossfit.com/workout/2017?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page)
    
    for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile('Rest Day')):
            continue
        for day in eachworkout.select('h3'):
            print(day.get_text())
        for paragraph in eachworkout.select('p'):
            if paragraph.find_all(string=re.compile('Related|Scroll for scaling options|Compare|Post|Tips and Scaling')):
                continue
            print(paragraph.get_text())
    page_number += 1


# Next steps: simplify 2017 and 2018 to use same loop.

# Next steps: find a way to add tags. maybe this needs to be done on the database level. as in a genre for a book. have a manytomanykey between movements and their tags.
