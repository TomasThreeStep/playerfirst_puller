def clean_compare_high(inp):
    if isinstance(inp, str):
        return inp.lower().replace("'","").replace("-","").replace(".","").replace(' ','').lower()\
            .replace("highschool","").replace("school","").replace("st","").replace("saint","")\
            .replace("college","").replace("prep","").replace("Institute","").replace("charter","")\
            .replace("township","").replace("twp","").replace("acadmey","").replace("hs","").replace('community','').replace('cc','')
    if inp == None:
        return  ""

def clean_compare(inp):
    if isinstance(inp, str):
        return inp.lower().replace("'","").replace("-","").replace(".","").replace(' ','')
    if inp == None:
        return  ""

def compare(a,b):
    if a == None:
        return False
    if b == None:
        return  False

    if isinstance(a, str) and isinstance(b, str):
         a = clean_compare(a)
         b = clean_compare(b)
         if a == "":
             return False
         if b == "":
             return False
         return a in b or b in a
    else:
        return a == b


def compare_high(a,b):
    if a == None:
        return False
    if b == None:
        return  False

    if isinstance(a, str) and isinstance(b, str):
         a = clean_compare_high(a)
         b = clean_compare_high(b)
         if a == "":
             return False
         if b == "":
             return False
         return a in b or b in a
    else:
        return a == b