#!/opt/local/bin/python
# -*- coding: utf-8 -*-

# Import libraries
from pybtex.database.input import bibtex
from pybtex.database import Person

# from pybtex.style.formatting import lastfirst

#import sys
import argparse
import time 

# Load additional functions
execfile("lastfirst.py")
execfile("unicode_to_latex.py")

# Define aliases
parser = bibtex.Parser()
lastfirst = NameStyle().format

thisyear = time.localtime().tm_year

script_description = '''
This script will generate a list of publications 
in a specified style and order based on bibtex entries.
Note: Requires the pybtex python library.
'''

def main():

    ## Define command line options/arguments
    argparser = argparse.ArgumentParser(description=script_description)
    argparser.add_argument('-s','--style',nargs=1,default='copernicus',help="Specify the citation style to be used. Currently only 'copernicus' is available.")
    argparser.add_argument('--output',nargs=1,default=None,help="Specify the output filename. If not specified, output will be printed to screen.")
    argparser.add_argument('bibtex_file', nargs='+', help='Bibtex files that will be used to generate publication list.')
    argparser.add_argument('--version', action='version', version='%(prog)s 0.1')
    

    # Test args
    args = argparser.parse_args(["-s copernicus","mypublications.bib"])
    #args = argparser.parse_args()

    # Load bibliography data from all files
    for filename in args.bibtex_file: bib_data = parser.parse_file(filename)

    # Extract entry list from bibliography data
    all_entries = bib_data.entries.items()

    # Isolate different entry types 
    bib_articles = bibSubset(all_entries,bibtype="article")

    for key, value in bib_articles:

        print "\n" + key 
        print copernicus(value)

        if key == "Alvarez-Solas2012": cit = value 
        
    return


############################################
##
## GENERAL FUNCTIONS FOR PARSING BIB DATA
##
############################################

def get_historial(entries,types=None,years=5):
    '''Make a nice historial list for web or word file for the last N years.'''
    
    # Get a list of years to output
    allyears = arange(thisyear-years-1,thisyear)

    # Get a list of bibtypes to loop over
    if types is None:
        types = ["article","book"]
    text = "" 
    for year in allyears:
        text = text + "\n{0}".format(year)


    return(text)

def bibSubset(entries,bibtype=None,year=None,isi=True):
    '''Extract only specific bib entry types from a set of bibtex entries.'''

    # Make sure desired years come in list and string format
    if not year is None:
        if type(year) == "int": year = [year]
        year = [str(y) for y in year]

    subset = []
    for entry in entries:
        
        # By default, the entry should be added to subset
        add = True

        # Check if this entry is a desired publication type
        if add and not bibtype is None:
            if not entry[1].type in bibtype: add = False 
        
        # Check if this entry is from a desired year        
        if add and not year is None:
            if not str(entry[1].fields['year']) in year: add = False 

        # Check if article is ISI, if desired
        if add and bibtype == "article" and isi:
                if entry[1].fields['journal'].lower().find("discussions") > 0: add = False

                # Other ISI tests...

        # If entry passed all filtering tests, add the entry to the list
        if add: subset.append(entry)

    # Sort entries by year
    subset_sorted = sorted(subset, cmp=sort_by_year)

    return(subset_sorted)

# Convert year strings to values
def convert_to_year(x):
    if type(x) == "str":
        x = x.lower()
        if x == "submitted": 
            year = "3000"
        elif x in ["in press","press","online","advanced online publication"]:
            year = "2999"
    else:
        year = str(x)

    return(year)

# Define sorting by year function
def sort_by_year(y, x):

    xyear = convert_to_year(x[1].fields['year'])
    yyear = convert_to_year(y[1].fields['year'])

    return int(xyear) - int(yyear)

def format_people(authors,abbr=True):
    '''Format people as "LastName, F."
       Should be input as "Last1, First1 and Last2, First2 and Last3, First3.
    '''

    name = []
    for author in authors:
        name.append( lastfirst(author, abbr=abbr).format().plaintext() )

    n = len(name)
    if n == 1:
        text = "".join(name)
    else:
        text = u"{0} and {1}".format(", ".join(name[0:(n-1)]),name[n-1])

    return(text)

def remove_curly(text):
    n = len(text)
    if text[0] == "{": text = text[1:n]
    n = len(text)
    if text[len(text)-1] == "}": text = text[0:(n-1)]
    return(text)

def remove_xb0(text):
    text = text.replace(u'\xb0',u' ')
    return(text)

def remove_xba(text):
    text = text.replace(u'\xba','o')
    return(text)

def remove_doublehyphen(text):
    text = text.replace("--","-")
    return(text)

def clean_latex(text):
    text = remove_doublehyphen(text)
    text = text.replace("\~{n}",latex_to_unicode("\\~{n}"))
    text = text.replace("\~ {n}",latex_to_unicode("\\~{n}"))
    text = text.replace("\'{A}",latex_to_unicode("\\'{A}"))
    text = text.replace("\'{E}",latex_to_unicode("\\'{E}"))
    text = text.replace("\'{I}",latex_to_unicode("\\'{I}"))
    text = text.replace("\'{O}",latex_to_unicode("\\'{O}"))
    text = text.replace("\'{U}",latex_to_unicode("\\'{U}"))
    text = text.replace("\'{a}",latex_to_unicode("\\'{a}"))
    text = text.replace("\'{e}",latex_to_unicode("\\'{e}"))
    text = text.replace("\'{\\i}",latex_to_unicode("\\'{\\i}"))
    text = text.replace("\'{o}",latex_to_unicode("\\'{o}"))
    text = text.replace("\'{u}",latex_to_unicode("\\'{u}"))
    text = text.replace("\ n",latex_to_unicode("\\~{n}"))
    text = text.replace("\\ {n}",latex_to_unicode("\\~{n}"))
    #text = text.replace(u'\xf1',"n")

    text = text.replace("\'{}","")
    #text = text.replace("{","")
    #text = text.replace("}","")

    text = text.replace("<nbsp>"," ")

    return(text)

def clean(text):
    text = remove_curly(text)
    text = clean_latex(text)
    #text = remove_xb0(text)
    #text = remove_xba(text)
    
    text = text.encode('utf-8')
    return(text)

######################
## STYLE DEFINTIONS ##
######################

class copernicus:
    '''Class defining output formats following Copernicus style for various 
       bibtex types (article, book, etc).
    '''

    def __init__(self,entry):
        self.type = entry.type 
        self.persons = entry.persons
        self.fields = entry.fields 

        # Initialize all formatted fields as empty strings
        self.formatted = {'address':"",'author':"",'booktitle':"",
                          'chapter':"",'doi':"",'edition':"",'editor':"",
                          'institution':"",'journal':"",'location':"",'month':"",
                          'number':"",'pages':"",'publisher':"",'school':"",
                          'title':"",'volume':"",'year':"" }

    def __repr__(self):
        
        fields   = self.fields
        all      = self.formatted 

        if 'address' in fields.keys(): 
            all['address'] = clean(" {0},".format(fields['address']))
        
        if 'author' in self.persons.keys():
            all['author'] = clean(format_people(self.persons['author']))
            all['author'] = "{0}:".format(all['author'])
        
        if 'booktitle' in fields.keys(): 
            all['booktitle'] = clean(fields['booktitle'])
            all['booktitle'] = " {0},".format(all['booktitle'])
            
        if 'chapter' in fields.keys(): 
            all['chapter'] = clean(" {0},".format(fields['chapter']))
        
        if 'doi' in fields.keys(): 
            all['doi'] = clean(fields['doi'])
            all['doi'] = all['doi'].replace("doi:","")
            all['doi'] = all['doi'].replace("DOI:","")
            all['doi'] = " doi:{0},".format(all['doi'])
        
        if 'edition' in fields.keys(): 
            all['edition'] = clean(" {0},".format(fields['edition']))
        
        if 'editor' in self.persons.keys():
            all['editor'] = clean(format_people(self.persons['editor']))
            all['editor'] = "{0} (Eds.)".format(all['editor'])
        
        if 'institution' in fields.keys(): 
            all['institution'] = clean(" {0},".format(fields['institution']))
        
        if 'journal' in fields.keys(): 
            all['journal'] = clean(" {0},".format(fields['journal']))

        if 'location' in fields.keys(): 
            all['location'] = " {0},".format(fields['location'])
        
        if 'month' in fields.keys(): 
            all['month'] = clean(" {0},".format(fields['month']))

        if 'number' in fields.keys(): 
            all['number'] = clean(" {0},".format(fields['number']))

        if 'pages' in fields.keys(): 
            all['pages'] = clean(fields['pages'])
            all['pages'] = " {0},".format(all['pages'])
            
        if 'school' in fields.keys(): 
            all['school'] = clean(" {0},".format(fields['school']))
        
        if 'title' in fields.keys(): 
            all['title'] = clean(fields['title'])
            all['title'] = " {0},".format(all['title'])

        if 'volume' in fields.keys(): 
            all['volume'] = clean(" {0},".format(fields['volume']))
        
        all['year'] = " in progress."
        if 'year' in fields.keys(): 
            all['year'] = clean(" {0}.".format(fields['year']))

        ## Now that all fields have been formatted,
        ## output the citation according to the type
        text = self.format(all)

        return(text)


    def format(self,all):

        if self.type.lower() == "article": 
            text = "{0}{1}{2}{3}{4}{5}{6}{7}".format(all['author'],all['title'],all['journal'],
                                                 all['volume'],all['number'],all['pages'],
                                                 all['doi'],all['year'])

        elif self.type.lower() == "book":
            text = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(
                                           all['author'],all['editor'],all['title'],
                                           all['edition'],all['publisher'],
                                           all['location'],all['year'])
        
        elif self.type.lower() == "inbook":
            text = "{0}{1}, in:{2}{3}{4}{5}{6}{7}{8}".format(
                                           all['author'],all['title'],all['booktitle'],
                                           all['edition'],all['editor'],all['publisher'],
                                           all['location'],all['pages'],all['year'])
        
        elif self.type.lower() == "inproceedings":
            text = "{0}{1}{2}{3}{4}{5}{6}".format(all['author'],all['title'],all['booktitle'],
                                           all['address'],all['doi'],all['month'],all['year'])

        elif self.type.lower() == "phdthesis":
            text = "{0}{1} PhD thesis,{2}{3}{4}{5}".format(
                                           all['author'],all['title'],#all['type'],
                                           all['school'],all['address'],
                                           all['pages'],all['year'])

        elif self.type.lower() == "techreport":
            text = "{0}{1} Report,{2}{3}{4}{5}".format(
                                           all['author'],all['title'],
                                           all['institution'],all['address'],
                                           all['pages'],all['year'])

        elif self.type.lower() == "unpublished":
            text = "{0}{1}{2}{3}{4}".format(all['author'],all['title'],
                                            all['volume'],all['pages'],all['year'])

        else: 
            text = "No format defined for: {0}".format(self.type)

        return(text)



if __name__ == "__main__":
    main()
# Done!



