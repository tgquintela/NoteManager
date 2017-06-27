
"""
Script for transforming notes into markdown.
"""

import sys
import os
from os.path import isfile, isdir

required_pars = ['tagnames', 'listtypte', 'definer', 'md_templates',
                 'format2md_list', ]
volunter_pars = ['tagtitle', 'summarytags', 'filter_summary',
                 'format_summary_md', 'summary_template',
                 'format2md_listsummary']
#default_volunter = {
#    'tagtitle': None,
#    'summarytags': ,
#    'filter_summary': ,
#    'format_summary_md':,
#    'summary_template': ,
#    'format2md_listsummary': 
#                    }


def check_input_all_parameters():
    notparameters = []
    for p in required_pars+volunter_pars:
        if p not in globals():
            notparameters.append(p)
    if len(notparameters) != 0:
        msg = "The next parameters are absence from the file of parameters: "
        pars = ", ".join(notparameters)
        msg += pars
        raise Exception(msg)


def input_arguments_parser(args):
    ## Parse the parameters
    if isfile(args[1]):
        execfile(args[1])
    elif type(args[1]) == dict:
        locals().update(args[1])
    elif type(args[1]) == str:
        exec(args[1])
    ## Only 3 possible inputs and 2 possible cases
    if len(args) == 2:
        ## Input the parameters file
        pathnotes = None
        pathnotes_md = None
    elif len(args) == 4:
        ## Input the parameters file
        pathnotes = args[2]
        pathnotes_md = args[3]
    else:
        raise IOError("Incorrect arguments input.")
    ## Ensure parameters
    assert(isdir(pathnotes))
    if not isdir(pathnotes_md):
        os.mkdir(pathnotes_md)

    ## Update the locals
    globals().update(locals())


if __name__ == "__main__":
    input_arguments_parser(sys.argv)
    check_input_all_parameters()
    transforming2md(tagnames, format2md_list, md_templates, listtypte, definer,
                    tagtitle, summarytags, format2md_listsummary,
                    summary_template, note_template, filter_summary, pathnotes,
                    pathnotes_md)

