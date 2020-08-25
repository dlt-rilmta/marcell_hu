#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os

# DummyTagger (EXAMPLE) ################################################################################################

# Setup the tuple: module name (ending with the filename the class defined in),
# class, friendly name, args (tuple), kwargs (dict)
em_dummy = ('marcell_hu', 'EmDummy', 'EXAMPLE (The friendly name of DummyTagger used in REST API form)',
            ('Params', 'goes', 'here'),
            {'source_fields': {'form'}, 'target_fields': ['star']})

# emToken ##############################################################################################################

em_token = ('quntoken', 'EmTokenPy', 'emToken', (), {'source_fields': set(), 'target_fields': ['form', 'wsafter']})

# emMorph ##############################################################################################################

em_morph = ('emmorphpy', 'EmMorphPy', 'emMorph', (), {'source_fields': {'form'}, 'target_fields': ['anas']})

# emTag ################################################################################################################

em_tag = ('purepospy', 'PurePOS', 'emTag (PurePOS)', (),
          {'source_fields': {'form', 'anas'}, 'target_fields': ['lemma', 'xpostag']})

# emCoNLL ##############################################################################################################

em_conll = ('emconll', 'EmCoNLL', 'CoNLL-U converter', (), {'source_fields': {'form'}, 'target_fields': []})

# emTerm ##############################################################################################################

term_list = os.path.join(os.path.dirname(__file__), 'emterm', 'test_termlist.tsv')
em_term = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
           (term_list,), {'source_fields': {'form', 'lemma'}, 'target_fields': ['term']})

# Map module personalities to firendly names...
# The first name is the default. The order is the display order of the modules
tools = [(em_token, ('tok', 'emToken')),
         (em_morph, ('morph', 'emMorph')),
         (em_tag, ('pos', 'emTag')),
         (em_conll, ('conll', 'emCoNLL')),
         (em_term, ('term', 'emTerm',)),
         (em_dummy, ('dummy-tagger', 'emDummy')),
         ]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
presets = {'annotate': ('Full pipeline', ['tok', 'morph', 'pos', 'dummy-tagger', 'conll'])}  # TODO értelem szerint!
