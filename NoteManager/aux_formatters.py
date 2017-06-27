
"""
Special formatting functions
----------------------------

"""

import re
joiner = """
"""

def format_index_md(index_note, format2md_listsummary, summary_template,
                    filter_summary):
    init, seps, formats, endit = format2md_listsummary
    seps_ext = ['']+seps
    index_note = filter_summary_sorting(index_note, filter_summary)
    for i in range(len(index_note)):
        aux = ''
        for j in range(len(index_note[i])):
            aux += seps_ext[j]+formats[j][0](index_note[i][j], formats[j][1])
        index_note[i] = init+aux+endit
    index_note = joiner.join(index_note)
    text = summary_template % ("Index", index_note)
    return text


def filter_summarytags(note, summarytags):
    return [note[t] for t in summarytags]


def filter_summary_sorting(notes, filter_summary):
    if filter_summary == -1:
        return notes
    aux = [note[filter_summary] for note in notes]
    idxs = sorted(range(len(aux)), key=lambda k: aux[k], reverse=True)
    notes_sorted = [notes[i] for i in idxs]
    return notes_sorted


############################ Default MD formatters ############################
###############################################################################
def create_md_itemizes(listas, webpath=''):
    """Create an itemize list from the text list."""
    lista = ''
    for e in listas:
        if e:
            lista += '* '+e+'\n'
    return lista


def create_md_tags(listas, webpath=''):
    """Create linked tags from the list parsed. TEMPORAL
    """
    lista = '***Tags***: '+', '.join(listas)
    return lista


def create_md_seealso(listas, webpath=''):
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


####################### Individual elements formatters ########################
###############################################################################
def format_intra_link(element, webpath=''):
    link = element.lower().replace(' ', '_')
    link = '['+element+']('+webpath+'/'+link+')'
    return link


def format_bold_intra_link(element, webpath=''):
    link = element.lower().replace(' ', '_')
    link = '[**'+element+'**]('+webpath+'/'+link+')'
    return link


def format_null(element, webpath=''):
    return element


################################ List formatter ###############################
###############################################################################
def format_lists_elements(listas, format2md_list=None):
    if format2md_list is None:
        format2md_list = ('', format_null, '', ', ', '', True)
    init, formatter_md, webpage, sep, endit, flag_empty = format2md_list
    lista = sep.join([init+formatter_md(e, webpage) for e in listas if e])
    lista += endit
    return lista


def format_md_content_ind(content, tagname, format2md_list, md_template):
    number = len(re.findall("%s", md_template))
    if format2md_list is False:
        if number == 1:
            text = md_template % content
        else:
            assert(number == 2)
            text = md_template % (tagname, content)
    else:
        if len(content) == 1 and content[0] == '' and not format2md_list[5]:
            return ''
        content = format_lists_elements(content, format2md_list)
        if number == 1:
            text = md_template % content
        else:
            assert(number == 2)
            text = md_template % (tagname, content)

    return text


def format_content_md(contents, tagnames, format2md_list, format2md_template):
    assert(len(tagnames) == len(contents))
    assert(len(tagnames) == len(format2md_list))
    assert(len(tagnames) == len(format2md_template))
    texts = []
    for i in range(len(tagnames)):
        text = format_md_content_ind(contents[i], tagnames[i],
                                     format2md_list[i], format2md_template[i])
        texts.append(text)
    return texts
