

import string


def load_ISI(filename):

    
    out = {}

    f = open(filename)
    for line in f.readlines():
        
        
        i = line.find("<DT>")
        if i >= 0: 
            title = string.capwords(line[(i+4):].strip().lower())
            title = title.replace(" Of"," of")
            title = title.replace(" The"," the")

        i = line.find("<DD>")
        if i >= 0: 
            abbr = string.capwords(line[(i+4):].strip().lower())
            abbr = abbr.replace(" Of"," of")
            abbr = abbr.replace(" The"," the")
            out[title] = abbr
        
    return(out)

def is_ISI(ISI,name):
    '''Check if a given name is in the ISI database (as title or abbreviation).'''

    test = string.capwords(name.strip().lower())
    test = test.replace(" Of"," of")
    test = test.replace(" The"," the")
    test = test.replace(".","")
    check = ISI.has_key(test) or test in ISI.values()

    return(check)

filename = "A-Z_abrvjt.txt"
ISI = load_ISI(filename)