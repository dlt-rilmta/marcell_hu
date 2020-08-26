#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys


class MCoNLL:

    pass_header = True

    def __init__(self, source_fields=None, target_fields=None):
        # TODO:
        #  bemeneti oszlopok:
        #  form wsafter anas lemma xpostag upostag feats NP-BIO NER-BIO
        #  amit ilyenné kéne konvertálni: kimeneti oszlopok:
        #  "id", "form", "lemma", "upos", "xpos", "feats", "head", "deprel", "deps", "misc", "marcell:ne", "marcell:np"

        self._col_mapper = {'id': 'ID',
                            'form': 'FORM',
                            'lemma': 'LEMMA',
                            'upostag': 'UPOS',
                            'xpostag': 'XPOS',
                            'feats': 'FEATS',
                            'head': 'HEAD',
                            'deprel': 'DEPREL',
                            'wsafter': 'MISC',
                            'NP-BIO': 'MARCELL:NP',
                            'NER-BIO': 'MARCELL:NE'
                            }

        # The CoNLL columns in order
        self._conll = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD',
                       'DEPREL', 'DEPS', 'MISC', 'MARCELL:NE', 'MARCELL:NP']

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

        word_id = 0
        for line in sen:
            new_line = []

            # new_line = (line[field_names[col]] if col in field_names else '_'
            #             for col in self._conll)

            for col in self._conll:
                if col == 'ID':
                    word_id += 1
                    new_line.append(str(word_id))
                elif col == 'MISC':
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
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """

        # prepared_fields = {self._col_mapper[emtsv_name]: col_num for col_num, emtsv_name in field_names.items()
        #         if emtsv_name in self._col_mapper}

        prepared_fields = {}

        for col_num, emtsv_name in field_names.items():
            if emtsv_name in self._col_mapper:
                prepared_fields[self._col_mapper[emtsv_name]] = col_num

        return prepared_fields
