#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys


class MCoNLL:

    pass_header = False
    fixed_order_tsv_input = False

    def __init__(self, source_fields=None, target_fields=None):

        #
        self._conll = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head',
                       'deprel', 'deps', 'wsafter', 'NER-BIO', 'NP-BIO']

        self._header = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head',
                       'deprel', 'deps', 'misc', 'marcell:ne', 'marcell:np']

        self._sentence_count = 0

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

        self._sentence_count += 1

        if self._sentence_count == 1:
            yield self._header

        for i, line in enumerate(sen, start=1):

            new_line = []

            for col in self._conll:
                if col == 'id':
                    new_line.append(str(i))
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
        # print(field_names)
        # return [field_names['form'], field_names['wsafter'], field_names['lemma'], field_names['xpostag'],
        #         field_names['upostag'], field_names['feats'], field_names['NP-BIO'], field_names['NER-BIO']]
        field_names = {'form': 0, 'wsafter': 1, 'lemma': 3, 'xpostag': 4,
                       'upostag': 5, 'feats': 6, 'NP-BIO': 7, 'NER-BIO': 8}
        return field_names

