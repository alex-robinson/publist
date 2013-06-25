#wget http://www.thomsonscientific.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER\&mode=print\&Page=1
#35 pages total 

from subprocess import call

def download_weblist():
    for k in arange(1,36):
        filename = "jlresults.cgi?PC=MASTER&mode=print&Page={0}".format(k)
        filenew  = "ThomsonReutersMasterList/Page{0}.txt".format(str(k).zfill(2))
        http = "http://www.thomsonscientific.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER&mode=print&Page={0}".format(k)

        call(["wget",http])
        call(["mv",filename,filenew])

    return

def extract_titles(filename="ThomsonReutersMasterList/ISImaster_2013-06-24.txt"):

    titles = []

    f = open(filename)
    for line in f.readlines():
        tmp = line.split()
        titles.append( " ".join(tmp[1:]) )

    return(titles)


def is_ISI(titles,name):
    '''Check if a given name is in the ISI database (as title or abbreviation).'''

    check = name.strip().upper() in titles
    return(check)

# Load the ISI titles into a list
ISI = extract_titles("ThomsonReutersMasterList/ISImaster_2013-06-24.txt")
