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

# mCoNLL ##############################################################################################################

m_conll = ('marcell_hu', 'MCoNLL', 'CoNLL-U converter for MARCELL', (),
           {'source_fields': set(),
            'target_fields': ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head',
                              'deprel', 'deps', 'misc', 'marcell:ne', 'marcell:np']})

# mMeta ##############################################################################################################

m_meta = ('marcell_hu', 'MMeta', 'Add metadata', (), {'source_fields':
                                                          {"id", "form", "lemma", "upos", "xpos", "feats", "head",
                                                           "deprel", "deps", "misc", "marcell:ne", "marcell:np"},
                                                      'target_fields': []})

# # emTerm for iate #####################################################################################################
#
# term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm', 'iate.tsv')
# em_term_iate = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
#                 (term_list,), {'source_fields': {'form', 'lemma'},
#                                'target_fields': ['marcell:iate']})
#
# # emTerm for eurovoc ##################################################################################################
# term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm', 'eurovoc.tsv')
# em_term_eurovoc = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
#                    (term_list,), {'source_fields': {'form', 'lemma'},
#                                   'target_fields': ['marcell:eurovoc']})

# emTerm for iate #####################################################################################################


term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm', 'iate.tsv')
em_term_iate = ('marcell_hu', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
                   (term_list,), {'source_fields': {'form', 'lemma'},
                                  'target_fields': ['marcell:iate']})
# emTerm for eurovoc ##################################################################################################

term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm', 'eurovoc.tsv')
em_term_eurovoc = ('marcell_hu', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
                   (term_list,), {'source_fields': {'form', 'lemma'},
                                  'target_fields': ['marcell:eurovoc']})

# mCorrect #########################################################################################################
m_correct = ('marcell_hu', 'MCorrect', 'Last module of MARCELL modules, which finalizes the output', (),
             {'source_fields': {"id", "form", "lemma", "upos", "xpos", "feats", "head", "deprel",
                                 "deps", "misc", "marcell:ne", "marcell:np", 'marcell:iate', 'marcell:eurovoc'},
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
         (em_dummy, ('dummy-tagger', 'emDummy')),
         (m_conll, ('mconll', 'mCoNLL')),
         (m_meta, ('mmeta', 'mMeta')),
         (em_term_iate, ('term-iate', 'emTerm',)),
         (em_term_eurovoc, ('term-eurovoc', 'emTerm',)),
         (m_correct, ('mcorrect', 'mCorrect'))]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
presets = {'annotate': ('Full pipeline', ['tok', 'morph', 'pos', 'chunk', 'ner', 'conv-morph',
                                          'mconll', 'mmeta', 'term-iate', 'term-eurovoc', 'mcorrect',
                                          'dummy-tagger', 'conll'])}  # TODO értelem szerint!
