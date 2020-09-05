#! /usr/bin/env python3

import re


class MMeta:
    pass_header = True

    def __init__(self, source_fields=None, target_fields=None):

        self._doc_types_hun_eng = {"határozat": "decree",
                                   "törvény": "law",
                                   "állásfoglalás": "position",
                                   "rendelet": "regulation",
                                   "intézkedés": "act",
                                   "közlemény": "notice",
                                   "nyilatkozat": "declaration",
                                   "parancs": "order",
                                   "utasítás": "ordinance",
                                   "szakutasítás": "ordinance",
                                   "végzés": "judgment",
                                   "tájékoztató": "notification",
                                   "ISMERETLEN": "UNDEFINED"}

        self._header = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps',
                        'misc', 'marcell:ne', 'marcell:np', 'marcell:iate', 'marcell:eurovoc']

        self._accent_table = str.maketrans({"á": "a", "ü": "u", "ó": "o", "ö": "o", "ő": "o", "ú": "u", "é": "e", "ű": "u", "í": "i"})

        self._prefix_dict = {"határozat": "hat", "rendelet": "rnd", "törvény": "trv", "végzés": "veg",
                             "közlemény": "koz", "nyilatkozat": "nyil", "utasítás": "ut", "állásfoglalás": "all",
                             "tájékoztató": "taj", "intézkedés": "int", "parancs": "par"}

        self._sentence_count = 0
        self._pat_paragraph = re.compile(r'^\d+[.] *§')
        self._pat_whitespaces = re.compile(r'\W')
        self._doc_type = 'ISMERETLEN'
        self._identifier = ''
        self._paragraph_number = 1

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

        # Collecting and processing of global metadatas
        if self._sentence_count == 1:
            for global_metadata in self._get_global_metadatas(sen):
                yield global_metadata

        # Collecting and processing of metadatas per sentence
        for metadatas_per_sentence in self._get_metadatas_per_sentence(sen):
            yield metadatas_per_sentence

        yield from sen

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """
        return field_names

    def _get_global_metadatas(self, sen):
        """
        Example output global metadata
        # global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC MARCELL:NE MARCELL:NP MARCELL:IATE MARCELL:EUROVOC
        # newdoc id = hu-hat_mk18188_16252018xi29korm
        # date = 2018
        # title = 1625/2018. (XI. 29.) Korm. határozat
        # type = határozat
        # entype = decree
        # issuer = Korm.
        # topic = garanciához kapcsolódó állami készfizető kezesség nyújtásáról
        """

        orig_sent = []
        # lemmas = []
        is_topic = False
        is_title_end = False
        title = ''
        topic = ''
        date = sen[0][2]

        for i, line in enumerate(sen):
            # Iterating over sentence to get the topic, title, documentum type, lemmas,
            # for and the original sentence as text

            space = " " if line[9] == "_" else ""
            orig_sent.append(line[1] + space)

            if is_topic:
                if line[1].replace("*", "") != ".":
                    topic += line[1] + space
                else:
                    is_topic = False

            elif not is_title_end:
                # lemmas.append(line[2])
                if line[2] in self._doc_types_hun_eng.keys():
                    self._doc_type = line[2]
                    title += self._doc_type
                    is_title_end = True
                    is_topic = True

                # átlagos rövid cím legfelső határa: ha nincs törvénytípus, így nem egy hosszú cím lesz az azonosító
                elif i == 9:
                    is_title_end = True
                else:
                    title += line[1] + space

        splitted_title = title.split()

        self._identifier = self._pat_whitespaces.sub('', '_'.join(splitted_title[-1:] + splitted_title[:-1])).lower(). \
            translate(self._accent_table)

        # From here: finalize global metadata values
        columns = f'# global.columns = {" ".join(self._header).upper()}'
        eng_type = self._doc_types_hun_eng[self._doc_type]  # self._doc_types_hun_eng.get(self._doc_type, 'UNKNOWN')
        hun_type = self._doc_type

        issuer = title.split()[-2] if hun_type != 'törvény' else 'parlament'
        issuer = f'# issuer = {issuer}'

        hun_type = f'# type = {hun_type}'
        eng_type = f'# entype = {eng_type}'

        title = f'# title = {title}'
        newdoc_id = f'# newdoc id = hu-{self._identifier}'
        date = f'# date = {date.split("/")[-1].replace(".", "")}'  # lemmas[0].split("/")[-1].replace(".", "")

        global_metadatas = [[columns], [newdoc_id], [date], [title], [hun_type], [eng_type], [issuer]]

        if len(topic) > 0:
            global_metadatas.append([f'# topic = {topic}'])

        return global_metadatas

    def _get_metadatas_per_sentence(self, sen):
        # from here: get metadatas per sentence
        orig_sent = [line[1] + ' ' if line[9] == '_' else line[1] + '' for line in sen]
        sentence = ''.join(orig_sent)
        sent_id = f'# sent_id = {self._identifier}-s{self._sentence_count}'
        par_id = ''
        metadatad_per_sentence = []

        if self._doc_type == "törvény" or self._doc_type == "rendelet":
            paragraph = self._pat_paragraph.match(sentence)

            if paragraph or self._sentence_count == 1:
                if self._sentence_count > 1:
                    self._paragraph_number = int(paragraph.group().split(".")[0])

                par_id = f'{self._identifier}-p{self._paragraph_number}'

            sent_id += f'-p{self._paragraph_number}'

        if par_id != '':
            par_id = f'# newpar id = {par_id}'
            metadatad_per_sentence.append([par_id])

        metadatad_per_sentence.append([sent_id])
        metadatad_per_sentence.append([f'# text = {sentence}'])

        return metadatad_per_sentence
