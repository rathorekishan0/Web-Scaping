#before running the program please install the following packages
# for beautifulsoup4 in terminal write the following command-
#   pip install beautifulsoup4
# for urllib.request-
#   pip install urllib3
#for requests-
#   pip install requests
import requests
import os
from bs4 import BeautifulSoup
import urllib.request

# for returnig beautifulsoup
def html(pageurl):
    url = pageurl
    code = requests.get(url)
    plaintext = code.text
    soup= BeautifulSoup(plaintext, 'html.parser')
    return soup

def category_search(pageurl):
    soup=html(pageurl)
    f=open('category.txt','w')
    for head in soup.findAll('div',{"class": "heading"}): #finds divisions having class:heading
        f.write(head.text) #writes it in a file
    f.close()

def course_title(pageurl):
    soup=html(pageurl)
    f=open('course title.txt','w')
    for title in soup.findAll('h2',{"class": "channel-overview-title"}): #finds all headings having class:channel-overview-title
        f.write(title.text+'\n') #writes it in a file
    f.close()

def cover_image(pageurl):
    soup=html(pageurl)
    path = "cover images"
    if not os.path.exists(path):
        os.makedirs(path) #makes a directory named cover images
    for image in soup.findAll('div',{"class": "channel-overview-img"}):
        src='https://see.stanford.edu/'+image.find('img').get('src')
        name=path+'/'+image.find('img').get('alt')+'.jpg'
        urllib.request.urlretrieve(src,name)  #downloads the image and stores it the directory


def course_number(pageurl):
    soup=html(pageurl)
    f=open('course number.txt','w')
    for ul in soup.findAll('ul',{"class": "channel-overview-details"}): #finds all ul tags having class:channel-overview-details
        f.write(ul.find('li').text+'\n') #writes the first li content of the ul
    f.close()

def instructor(pageurl):
    soup=html(pageurl)
    path = "instructor details with photo"
    if not os.path.exists(path):
        os.makedirs(path)  #creates the directory 'instructor details with photo'
    for ul in soup.findAll('ul',{"class": "channel-overview-details"}):
        soup=html(pageurl+'/'+ul.find('li').text) #goes to the individual courses
        innerpath=path +'/'+ul.find('li').text
        if not os.path.exists(innerpath):
            os.makedirs(innerpath) #makes directory for each course
        for div in soup.findAll('div',{'class':'panel-content instructor-bio-panel'}):
            fullpath = os.path.join(innerpath, div.find('p').text + '.txt')
            f = open(fullpath, 'w')
            f.write(div.text) #writes instructor detail
            src = 'https://see.stanford.edu/' + div.find('img').get('src')
            name=innerpath+'/'+div.find('p').text+'.jpg'
            urllib.request.urlretrieve(src,name) #downloads the image
            f.close()

def sessions(pageurl):
    soup=html(pageurl)
    path='Number of course sessions'
    if not os.path.exists(path):
        os.makedirs(path) #makes directory
    for ul in soup.findAll('ul',{"class": "channel-overview-details"}):
        soup=html(pageurl + '/' + ul.find('li').text)
        innerpath=path+'/'+ul.find('li').text+'.txt'
        f=open(innerpath,'w')
        for head in soup.findAll('h2',{'class':'pull-left'}):
            if head.find('span')!=None:  #checks for the specific h2 having a span tag
                session=head.find('span').text
                f.write(''.join(c for c in session if c in '0123456789')) #writes only the number part from the string

def description(pageurl):
    soup=html(pageurl)
    path = 'description'
    if not os.path.exists(path):
        os.makedirs(path)
    for ul in soup.findAll('ul', {"class": "channel-overview-details"}):
        soup=html(pageurl + '/' + ul.find('li').text)
        innerpath=path+'/'+ul.find('li').text+'.txt'
        f=open(innerpath,'w')
        div=soup.find('div',{'class':'panel-content'})
        desc=div.find('p')
        f.write(desc.text)  #writes the description
        f.close()

def exams(pageurl):
    soup=html(pageurl)
    path = 'Exam details'
    if not os.path.exists(path):
        os.makedirs(path)
    for ul in soup.findAll('ul', {"class": "channel-overview-details"}):
        soup=html(pageurl + '/' + ul.find('li').text)
        for div in soup.findAll('div',{'class':'panel-heading'}):
            if div.find('h2').text=='Exams':
                innerpath = path + '/' + ul.find('li').text
                if not os.path.exists(innerpath):
                    os.makedirs(innerpath)
                nextdiv = div.findNext('div') #returns the nextsibling of the div tag having heading as Exams
                for tr in nextdiv.findAll('tr'):  #crates sub-directory for each exam type and stores all the pdf of that type
                    for td in tr.findAll('td'):
                        if not td.find('a'):
                            fullpath = innerpath + '/' + td.text
                            if not os.path.exists(fullpath):
                                os.makedirs(fullpath)
                        else:
                            url='https://see.stanford.edu/'+td.find('a').get('href')
                            name=fullpath+'/'+td.text+'.pdf'
                            urllib.request.urlretrieve(url,name)

url='https://see.stanford.edu/Course'
category_search(url)
course_title(url)
cover_image(url)
course_number(url)
instructor(url)
sessions(url)
description(url)
exams(url)