
"""
# Parameters to parse and create proper notes
That is a temporal file to parse and create notes. It gives to the program the required
parameters to tune the program regarding the needs of the user.

"""

from NoteManager.parser_notes import transforming2md
from NoteManager.aux_formatters import format_null, format_intra_link,\
    format_bold_intra_link


##################### Default parameter definition
### Parser information
## It gives the program the parser information of the not structured file
## in which the original notes are written.
# Tag names of each part of the structured note:
tagnames = ['Title', 'Date', 'Note', 'Tags', 'See also', 'Material', 'Papers',
            'Books']                                            ## Default: []
# For each tagname if it is a list or not.
# If it is should be specified the separator:
listtypte = [False, False, False, ',', ',', '\n', '\n', '\n']   ## Default: []
definer = ':'                                                   ## Default: ':'
tagtitle = 'Title'                                              ## Default: None

### Encoding information to create properly text to markdown
webpath = '/notes'
## Note parts
# How to format each of the tagnames:
md_templates = ["%s", "%s", "%s\n", "%s:\n%s", "#### %s\n%s\n",
                "## %s\n%s\n", "## %s\n%s\n", "## %s\n%s\n"
                ]
# Formatters of the lists in the output note.
# If it is the lists it should be specified the formatting information.
# The formatting information is a 6-tuple with information:
# (init, formatter_md, webpage, sep, endit, flag_empty)
# init: how to initiate each item in list
# formatter_md: function how to build the element name hyperlink
# webpage: webpage root.
# sep: separators between items in list
# endit: how to end each item in list
# flag_empty: if the empty list is a list with one element '' so False
format2md_list = [False, False, False,
                  ('  - ', format_null, '', '\n', '', True),
                  ('', format_intra_link, webpath, ', ', '', True),
                  ('* ', format_null, '', '\n', '', False),
                  ('* ', format_null, '', '\n', '', False),
                  ('* ', format_null, '', '\n', '', False)
                  ]

## Summary coding information
summarytags = ['Title', 'Date']
filter_summary = 1
format_summary_md = [(format_bold_intra_link, webpath), (format_null, '')]
summary_template = "# %s\n%s"
note_template = """---
title: "{Title}"
collection: notes
permalink: /notes/{Filename}
date: {Date}
{Tags}
---

{Note}

{See also}

{Material}

{Papers}

{Books}

"""
# Format each line element of the list
format2md_listsummary = ['* ', ['    '], format_summary_md, '']


