
"""
Trash parser

"""


#def semistructured2note(note_info):
#    """Transform the semistructured note parsed by `parse` function into a
#    markdown note.
#    """
#    file = open('Tools/final_note_template', 'r')
#    text = file.read()
#
#    title = note_info['Title']
#    date = note_info['Date']
#    note = note_info['Note']
#    tags = note_info['Tags']
#    tags = create_md_tags(tags)
#
#    extra = ''
#    for e in parts[4:]:
#        ## Extract contents
#        if e == parts[4]:
#            contents = create_md_seealso(note_info[e], webpath)
#            ## Build with title
#            if contents:
#                extra += '#### '+e+'\n'+contents+'\n'
#        else:
#            contents = create_md_itemizes(note_info[e])
#            ## Build with title
#            if contents:
#                extra += '## '+e+'\n'+contents+'\n'
#    ## Build document
#    text = text % (title, date, note, tags, extra)
#
#    return text


#def semistructured2dict(note_info):
#
#    title = note_info['Title']
#    date = note_info['Date']
#    note = note_info['Note']
#    tags = note_info['Tags']
#    tags = create_md_tags(tags)


#def transforming2dict():
#    ## Get the files we want to parse
#    pathnotes = join('/'.join(thisfile.split('/')[:-1]), '../Notes')
#    filenames = get_filenames()
#    json_file = '/home/antonio/code/temporal_tasks/temporal_tasks/notes.json'
#    ## Parse files
#    notes = []
#    for filename in filenames:
#        filename = join(pathnotes, filename)
#        note_info = parse(filename)
#
#        note = semistructured2dict(note_info)
#        notes.append(note)
#
#    ## Input the general information
#
#    ## Store in json file
#    json_data = {'notes': notes}
#    with open(json_file, 'w') as f:
#        json.dump(json_data, f)
#
#    ## Create the information to recommend words (TODO)
#    ## Store the information to recommend words (TODO)

## TODO:
# index


#if __name__ == "__main__":
#    transforming2md()
