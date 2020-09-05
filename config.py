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
# print_header=False, force_id=False, add_space_after_no=False, extra_columns=None,
em_conll = ('emconll', 'EmCoNLL', 'CoNLL-U converter', (),
            {'force_id': True,
             'add_space_after_no': True,
             'extra_columns': {'NER-BIO-FIXED': 'MARCELL:NER', 'NP-BIO-FIXED': 'MARCELL:NP',
                               'marcell:iate': 'MARCELL:IATE', 'marcell:eurovoc': 'MARCELL:EUROVOC'},
             'source_fields': {'form', 'wsafter', 'anas', 'lemma', 'xpostag', 'upostag', 'feats'},
             'target_fields': []})

# mMeta ##############################################################################################################

m_meta = ('marcell_hu.mmeta', 'MMeta', 'Add metadata', (), {'source_fields': {'form', 'lemma'},
                                                               'target_fields': []})

# emTerm for iate #####################################################################################################

term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm_term_lists', 'iate.tsv')
em_term_iate = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
                (term_list,), {'termid_separator': ';',
                               'source_fields': {'form', 'lemma'},
                               'target_fields': ['marcell:iate']})

# emTerm for eurovoc ##################################################################################################
term_list = os.path.join(os.path.dirname(__file__), 'marcell_hu', 'emterm_term_lists', 'eurovoc.tsv')
em_term_eurovoc = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
                   (term_list,), {'termid_separator': ';',
                                  'source_fields': {'form', 'lemma'},
                                  'target_fields': ['marcell:eurovoc']})

# emIOBUtils ###########################################################################################################

emiobutils_maxnp = ('emiobutils', 'EmIOBUtils', 'IOB format converter and fixer for maxNP', (),
                    {'out_style': 'IOB2', 'source_fields': {'NP-BIO'}, 'target_fields': ['NP-BIO-FIXED']})

emiobutils_ner = ('emiobutils', 'EmIOBUtils', 'IOB format converter and fixer for NER', (),
                  {'out_style': 'IOB2', 'source_fields': {'NER-BIO'}, 'target_fields': ['NER-BIO-FIXED']})

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
         (m_meta, ('mmeta', 'mMeta')),
         (em_term_iate, ('term-iate', 'emTerm',)),
         (em_term_eurovoc, ('term-eurovoc', 'emTerm',)),
         (emiobutils_maxnp, ('fix-np', 'fix-chunk', 'emIOBUtils-NP')),
         (emiobutils_ner, ('fix-ner', 'fix-ner', 'emIOBUtils-NER'))]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
presets = {'annotate': ('Full pipeline', ['tok', 'morph', 'pos', 'chunk', 'ner', 'conv-morph',
                                          'mmeta', 'term-iate', 'term-eurovoc',
                                          'dummy-tagger', 'conll'])}  # TODO értelem szerint!
