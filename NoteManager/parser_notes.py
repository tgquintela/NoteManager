
"""
Tools to parse properly notes.

"""

import json
import os
from os import walk
from os.path import isfile, join, basename, splitext

from aux_formatters import create_md_tags, create_md_seealso,\
    create_md_itemizes, format_null, format_intra_link, format_content_md,\
    format_index_md, filter_summarytags
from aux_administrativers import get_filenames, parser_parameters,\
    parser_directories, check_parameters


### Encode information to create properly text to html
#format2html = []
#webpath = ''
#definer = ':'
#
#tagnames = ['Title', 'Date', 'Note', 'Tags', 'See also', 'Material', 'Papers',
#            'Books']
#listtypte = [False, False, False, ',', ',', '\n', '\n', '\n']
### Encode information to create properly text to markdown
#format2md_f = [False, False, False, create_md_tags, create_md_seealso,
#               create_md_itemizes, create_md_itemizes, create_md_itemizes]
#format2md_template = ["# %s\n", "%s\n", "%s\n", "***%s***: %s\n",
#                      "#### %s\n%s\n", "## %s\n%s\n", "## %s\n%s\n",
#                      "## %s\n%s\n"
#                      ]
#format2md_list = [False, False, False, ('', format_null, '', ', ', ''),
#                  ('* ', format_intra_link, webpath, '\n', ''),
#                  ('* ', format_null, '', '\n', ''),
#                  ('* ', format_null, '', '\n', ''),
#                  ('* ', format_null, '', '\n', '')
#                  ]
#
#summarytags = ['Title', 'Date']
format_summary_md = [(format_intra_link, ''), (format_null, '')]
#summary_template = "# %s\n %s"
format2md_listsummary = ['* ', ['    '], format_summary_md, '\n']
joiner = """
"""


def parse_note(filename, tagnames, listtypte, definer=':'):
    """Main function to parse notes files."""
    ## 0. Get text from file
    file_ = open(filename, 'r')
    text = file_.read()

    ## 1. Get ranges
    inds = []
    for p_i in range(len(tagnames)):
        ## Get indice
        ind = text.find(tagnames[p_i]+definer)
        ## Append indices
        inds.append(ind)
        inds.append(ind+len(tagnames[p_i])+1)
    inds.append(len(text))
    inds = inds[1:]

    ## 2. Get the structure split
    note = {}
    for i in range(len(tagnames)):
        aux_text = text[inds[2*i]:inds[2*i+1]].strip()
        if listtypte[i] is False:
            note[tagnames[i]] = aux_text
        else:
            aux_list = aux_text.split(listtypte[i])
            aux_list = [aux.strip() for aux in aux_list]
            note[tagnames[i]] = aux_list
    return note


def semistructured2note(note_info, tagnames, format2md_list, md_templates):
    """Transform the semistructured note parsed by `parse` function into a
    markdown note.
    """
    contents = [note_info[e] for e in tagnames]
    texts = format_content_md(contents, tagnames, format2md_list, md_templates)
    text = joiner.join(texts)
    return text


def semistructured2notedict(note_info, tagnames, format2md_list, md_templates):
    """Transform the semistructured note parsed by `parse` function into a
    markdown note.
    """
    contents = [note_info[e] for e in tagnames]
    texts = format_content_md(contents, tagnames, format2md_list, md_templates)
    notedict = dict(zip(tagnames, texts))
    return notedict


def transforming2md(tagnames=[], format2md_list=[], md_templates=[],
                    listtypte=[], definer=':', tagtitle=None, summarytags=[],
                    format2md_listsummary=[], summary_template="%s\n%s",
                    note_template="{Text}", filter_summary=None,
                    pathnotes=None, pathnotes_md=None):
    ### 0. Parser parameters
    tagnames, format2md_list, md_templates, listtypte, definer, tagtitle =\
        parser_parameters(tagnames, format2md_list, md_templates, listtypte,
                          definer, tagtitle)
    pathnotes_md, pathnotes = parser_directories(pathnotes_md, pathnotes)
    check_parameters(tagnames, format2md_list, md_templates, listtypte,
                     tagtitle, summarytags, format2md_listsummary,
                     filter_summary, summary_template)
    ### 1. Remove files folder of markdown translated notes
    ## Cleaning folder Notes_md
    for (dirpath, dirnames, filenames) in walk(pathnotes_md):
        for file_md in filenames:
            os.remove(join(pathnotes_md, file_md))
        for folder in dirnames:
            for (dirpathsub, _, filenamessub) in walk(folder):
                for file_md in filenamessub:
                    os.remove(join(folder, file_md))
            os.remove(join(pathnotes_md, folder))
    os.makedirs(join(pathnotes_md, 'notes'))

    ### 2. Parser and transformation
    filenames = get_filenames(pathnotes)
    notes_data = []
    index_note = []
    for filename in filenames:
        filepath = join(pathnotes, filename)
        note_info = parse_note(filepath, tagnames, listtypte, definer)
        namefile = note_info[tagtitle].lower().replace(' ', '_')
        if namefile == '':
#            print(filepath)
            continue

        ## Format text
        note = semistructured2note(note_info, tagnames, format2md_list,
                                   md_templates)
        notedict = semistructured2notedict(note_info, tagnames, format2md_list,
                                           md_templates)
        notedict.update({'Text': note, 'Filename': namefile})

        ## Summary adding to index note
        summarytagsinfo = filter_summarytags(note_info, summarytags)
        index_note.append(summarytagsinfo)
        notes_data.append(notedict)

    notes_data = sorted(notes_data, key=lambda k: k['Date'])
    for i, notedict in enumerate(notes_data):
        notedict['order_item'] = i
        notes_data[i] = notedict
        ## Create note from template
        note = note_template.format(**notedict)
        ## Store individual note
        file_ = open(join(pathnotes_md,
                          'notes',
                          notedict['Filename']+'.md'),
                     'w+')
        file_.write(note)
        file_.close()

    ## Format index note
    index_md = format_index_md(index_note, format2md_listsummary,
                               summary_template, filter_summary)
    ## Store index
    file_ = open(join(pathnotes_md, 'index.md'), 'w+')
    file_.write(index_md)
    file_.close()
    ## Store collection
    file_ = open(join(pathnotes_md, 'collection.json'), 'w+')
    json.dump(notes_data, file_)
    file_.close()
