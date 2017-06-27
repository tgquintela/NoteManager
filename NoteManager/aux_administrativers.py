
"""
Administrative functions
------------------------

"""

import os
from os import walk
from os.path import isfile, join


def get_filenames(pathnotes=None):
    if pathnotes is None:
        thisfile = join(os.path.realpath(__file__))
        pathnotes = join('/'.join(thisfile.split('/')[:-1]), '../Notes')
    f = []
    dirnames = os.listdir(pathnotes)
    for e in dirnames:
        for (dirpth, dirns, filenames) in walk(join(pathnotes, e)):
            filenames = [join(join(pathnotes, e), e1) for e1 in filenames]
            f.extend(filenames)
    return f


def parser_parameters(tagnames, format2md_list, md_templates, listtypte,
                      definer, tagtitle):
    if tagtitle is None:
        tagtitle = tagnames[0]
    return tagnames, format2md_list, md_templates, listtypte, definer, tagtitle


def parser_directories(pathnotes_md, pathnotes):
    if pathnotes_md is None:
        thisfile = join(os.path.realpath(__file__))
        pathnotes_md = join('/'.join(thisfile.split('/')[:-1]), '../Notes_md')
    if pathnotes is None:
        pathnotes = join('/'.join(thisfile.split('/')[:-1]), '../Notes')
    return pathnotes_md, pathnotes


def check_parameters(tagnames, format2md_list, md_templates, listtypte,
                     tagtitle, summarytags, format2md_listsummary,
                     filter_summary, summary_template):
    ## Asserts
    assert(len(tagnames) == len(listtypte))
    assert(len(tagnames) == len(md_templates))
    assert(len(tagnames) == len(format2md_list))
    ## Summary coherence
    assert(filter_summary in range(-1, len(summarytags)))
    if tagtitle is not None:
        assert(tagtitle in tagnames)
    assert(len(format2md_listsummary) == 4)
    assert(len(format2md_listsummary[1]) == len(summarytags)-1)
    assert(len(summarytags) == len(format2md_listsummary[2]))
    assert(all([len(e) == 2 for e in format2md_listsummary[2]]))
    ## Summary correspondance
    assert(all([e in tagnames for e in summarytags]))
