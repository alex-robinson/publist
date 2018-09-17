#!/usr/bin/env python
#!/opt/local/bin/python
# -*- coding: utf-8 -*-



#wget http://www.thomsonscientific.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER\&mode=print\&Page=1
#35 pages total 

# Updated in 2016:
#wget http://ip-science.thomsonreuters.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER\&mode=print\&Page=1
#44 pages total


# To generate master journal table
# 1. Download files in print mode from Thomson-Reuters, as above
# 2. Join files into one: cat jlresults.cgi\?PC\=MASTER\&mode\=print\&Page\=* > tmp
# 3. Extract only the lines with journal titles using grep: grep "<DT><strong>" tmp > tmp1 
# 4. Replaces html tags with nothing: 
#        sed s/
# That's it!

from subprocess import call

def download_weblist():
    for k in arange(1,36):
        filename = "jlresults.cgi?PC=MASTER&mode=print&Page={0}".format(k)
        filenew  = "ThomsonReutersMasterList/Page{0}.txt".format(str(k).zfill(2))
        http = "http://www.thomsonscientific.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER&mode=print&Page={0}".format(k)

        call(["wget",http])
        call(["mv",filename,filenew])

    return

def extract_titles_old(filename="ThomsonReutersMasterList/ISImaster_2013-06-24.txt"):

    titles = []

    f = open(filename)
    for line in f.readlines():
        tmp = line.split()
        titles.append( " ".join(tmp[1:]) )

    return(titles)

def extract_titles(filename="ThomsonReutersMasterList/ISImaster_2016-09-12.txt"):

    titles = [line.rstrip('\n') for line in open(filename)]
    return(titles)


def is_ISI(titles,name):
    '''Check if a given name is in the ISI database (as title or abbreviation).'''

    check = name.strip().upper() in titles
    return(check)

# Load the ISI titles into a list
#ISI = extract_titles("ThomsonReutersMasterList/ISImaster_2013-06-24.txt")
ISI = extract_titles("ThomsonReutersMasterList/ISImaster_2016-09-12.txt")


