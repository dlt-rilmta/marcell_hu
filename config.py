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

# emMorph2Dep ##########################################################################################################

em_morph2ud = ('emmorph2ud', 'EmMorph2UD', 'emmorph2ud', (),
               {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['upostag', 'feats']})

# emChunk ##############################################################################################################

model_name = os.path.join('models', 'maxnp.szeged.emmorph')
cfg_file = os.path.join('configs', 'maxnp.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_chunk = ('huntag', 'Tagger', 'emChunk', ({'cfg_file': cfg_file, 'model_name': model_name},),
            {'source_fields': set(), 'target_fields': [target_field]})

# emNER ################################################################################################################

model_name = os.path.join('models', 'ner.szeged.emmorph')
cfg_file = os.path.join('configs', 'ner.szeged.emmorph.yaml')
target_field = 'NER-BIO'

em_ner = ('huntag', 'Tagger', 'emNER', ({'cfg_file': cfg_file, 'model_name': model_name},),
          {'source_fields': set(), 'target_fields': [target_field]})

# emCoNLL ##############################################################################################################

em_conll = ('emconll', 'EmCoNLL', 'CoNLL-U converter', (), {'source_fields': {'form'}, 'target_fields': []})

# emTerm ##############################################################################################################

term_list = os.path.join(os.path.dirname(__file__), 'emterm', 'test_termlist.tsv')
em_term = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
           (term_list,), {'source_fields': {'form', 'lemma'}, 'target_fields': ['term']})

# mCoNLL ##############################################################################################################

m_conll = ('marcell_hu', 'MCoNLL', 'CoNLL-U converter for MARCELL', (),
           {'source_fields': set(),
            # {'form', 'wsafter', 'anas', 'lemma', 'xpostag', 'upostag', 'feats', 'NP-BIO', 'NER-BIO'},
            'target_fields': ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head',
                              'deprel', 'deps', 'misc', 'marcell:ne', 'marcell:np']})

# mMeta ##############################################################################################################

m_meta = ('marcell_hu', 'MMeta', 'Add metadata', (), {'source_fields':
                                                          {"id", "form", "lemma", "upos", "xpos", "feats", "head",
                                                           "deprel", "deps", "misc", "marcell:ne", "marcell:np"},
                                                      'target_fields': []})

# Map module personalities to firendly names...
# The first name is the default. The order is the display order of the modules
tools = [(em_token, ('tok', 'emToken')),
         (em_morph, ('morph', 'emMorph')),
         (em_tag, ('pos', 'emTag')),
         (em_chunk, ('chunk', 'emChunk')),
         (em_ner, ('ner', 'emNER')),
         (em_morph2ud, ('conv-morph', 'emmorph2ud')),
         (em_conll, ('conll', 'emCoNLL')),
         (em_term, ('term', 'emTerm',)),
         (em_dummy, ('dummy-tagger', 'emDummy')),
         (m_conll, ('mconll', 'mCoNLL')),
         (m_meta, ('mmeta', 'mMeta'))]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
presets = {'annotate': ('Full pipeline', ['tok', 'morph', 'pos', 'dummy-tagger', 'conll'])}  # TODO értelem szerint!
