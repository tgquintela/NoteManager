

"""
Tools to parse properly notes.

"""

import os
from os.path import isfile, join
from os import walk

folder_name = ''
list_parameters = []


parts = ['Title', 'Date', 'Note', 'Tags', 'See also', 'Material', 'Papers', 'Books']
listtypte = [False, False, False, ',', ',', '\n', '\n', '\n']
webpath = ''


def parser_notes(list_parameters=[], sep=':'):
    pass


def parse(filename):
    """Main function to parse notes files."""
    ## 0. Get text from file
    file = open(filename, 'r')
    text = file.read()

    ## 1. Get ranges
    inds = []
    for p_i in range(len(parts)):
        ## Get indice
        ind = text.find(parts[p_i]+':')
        ## Append indices
        inds.append(ind)
        inds.append(ind+len(parts[p_i])+1)
    inds.append(len(text))
    inds = inds[1:]

    ## 2. Get the structure split
    note = {}
    for i in range(len(parts)):
        aux_text = text[inds[2*i]:inds[2*i+1]].strip()
        if listtypte[i] is False:
            note[parts[i]] = aux_text
        else:
            aux_list = aux_text.split(listtypte[i])
            aux_list = [aux.strip() for aux in aux_list]
            note[parts[i]] = aux_list
    return note


def semistructured2note(note_info):
    """Transform the semistructured note parsed by `parse` function into a
    markdown note.
    """
    file = open('Tools/final_note_template', 'r')
    text = file.read()

    title = note_info['Title']
    date = note_info['Date']
    note = note_info['Note']
    tags = note_info['Tags']
    tags = create_md_tags(tags)

    extra = ''
    for e in parts[4:]:
        ## Extract contents
        if e == parts[4]:
            contents = create_md_seealso(note_info[e])
            ## Build with title
            if contents:
                extra += '#### '+e+'\n'+contents+'\n'
        else:
            contents = create_md_itemizes(note_info[e])
            ## Build with title
            if contents:
                extra += '## '+e+'\n'+contents+'\n'
    ## Build document
    text = text % (title, date, note, tags, extra)

    return text


def create_md_itemizes(listas):
    """Create an itemize list from the text list."""
    lista = ''
    for e in listas:
        if e:
            lista += '* '+e+'\n'
    return lista

def create_md_tags(listas):
    """Create linked tags from the list parsed. TEMPORAL
    """
    lista = '***Tags***: '+', '.join(listas)
    return lista


def create_md_seealso(listas):
    """Create linked see also from the list parsed.
    """
    lista = []
    for e in listas:
        if e:
            link = e.lower().replace(' ', '_')
            lista.append('['+e+']('+webpath+'/'+link+')')
    if lista:
        lista = ', '.join(lista)
    else:
        lista = ''
    return lista


def get_filenames():
    thisfile = join(os.path.realpath(__file__))
    pathnotes = join('/'.join(thisfile.split('/')[:-1]), '../Notes')
    f = []
    dirnames = os.listdir(pathnotes)
    for e in dirnames:
        for (dirpth, dirns, filenames) in walk(join(pathnotes, e)):
            filenames = [join(join(pathnotes, e), e1) for e1 in filenames]
            f.extend(filenames)
    return f


def transforming2md():
    ## Cleaning folder Notes_md
    thisfile = join(os.path.realpath(__file__))
    pathnotes_md = join('/'.join(thisfile.split('/')[:-1]), '../Notes_md')
    pathnotes_md = '/home/antonio/code/temporal_tasks/temporal_tasks/Notes_md'
    for (dirpath, dirnames, filenames) in walk(pathnotes_md):
        for file_md in filenames:
            os.remove(join(pathnotes_md, file_md))

    pathnotes = join('/'.join(thisfile.split('/')[:-1]), '../Notes')
    filenames = get_filenames()
    for filename in filenames:
        filename = join(pathnotes, filename)
        note_info = parse(filename)
        namefile = note_info['Title'].lower().replace(' ', '_')
        if namefile == '':
            print filename
        note = semistructured2note(note_info)
        file = open(join(pathnotes_md, namefile+'.md'), 'w+')
        file.write(note)
        
    
if __name__ == "__main__":
    transforming2md()

        
