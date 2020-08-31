#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys


class MCoNLL:

    pass_header = False
    fixed_order_tsv_input = True

    def __init__(self, source_fields=None, target_fields=None):

        #
        self._conll = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head',
                       'deprel', 'deps', 'wsafter', 'NER-BIO', 'NP-BIO']

        self.header = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head',
                       'deprel', 'deps', 'misc', 'marcell:ne', 'marcell:np']

        self.sentence_count = 0

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        """
        Reorder the needed fields and put _ when a mandatory field missing (eg. not created yet)
        :param sen: The sentence splitted to tokens and fields
        :param field_names: The name of the fields mapped to the column indices
        :return: A generator yields the output line-by-line
        """

        self.sentence_count += 1

        if self.sentence_count == 1:
            yield self.header

        word_id = 0

        for line in sen:

            new_line = []

            for col in self._conll:
                if col == 'id':
                    word_id += 1
                    new_line.append(str(word_id))
                elif col == 'wsafter':
                    if line[field_names[col]] == '""':
                        new_line.append('SpaceAfter=No')
                    else:
                        new_line.append('_')
                elif col in field_names:
                    new_line.append(line[field_names[col]])

                else:
                    new_line.append('_')

            yield new_line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL n
        ames tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """
        field_names = {'form': 0, 'wsafter': 1, 'lemma': 3, 'xpostag': 4,
                       'upostag': 5, 'feats': 6, 'NP-BIO': 7, 'NER-BIO': 8}
        return field_names

