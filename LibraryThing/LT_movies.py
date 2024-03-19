import pandas as pd

def LT():

    dt = {'date':'int'}
    cat = pd.read_json('librarything_lsky2061.json',orient='index',convert_axes=False,dtype=dt,convert_dates=False)


    print(cat.head())
    print(cat['date'])


#Index(['books_id', 'title', 'sortcharacter', 'public', 'primaryauthor',
#       'primaryauthorrole', 'authors', 'collections_idA', 'collections',
#       'originalisbn', 'isbn', 'asin', 'ean', 'publication', 'date', 'summary',
#       'language', 'language_codeA', 'originallanguage',
#       'originallanguage_codeA', 'ddc', 'lcc', 'subject', 'genre', 'genre_id',
#       'source', 'workcode', 'entrydate', 'format', 'copies',
#       'physical_description', 'height', 'thickness', 'length', 'dimensions',
#       'weight', 'awards', 'tags', 'tagidA', 'upc', 'pages', 'rating',
#       'dateread', 'review', 'reviewlang', 'secondaryauthor',
#       'secondaryauthorroles', 'series', 'originaltitle', 'volumes',
#       'privatecomment'],
#      dtype='object


         
         
