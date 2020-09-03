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

        self._accent_dict = {"á": "a", "ü": "u", "ó": "o", "ö": "o", "ő": "o", "ú": "u", "é": "e", "ű": "u", "í": "i"}

        self._sentence_count = 0
        self._pat_paragraph = re.compile(r'^\d+[.] *§')
        self._pat_whitespaces = re.compile(r'\W')
        self._doc_type = ''
        self._identifier = ''

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

    def _get_eng_type(self, word):
        if self._is_huntype(word):
            return self._doc_types_hun_eng[word]
        return "UNKNOWN"

    def _is_huntype(self, word):
        return word in self._doc_types_hun_eng.keys()

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
        title_end = False
        title = ''
        topic = ''
        date = ''

        for i, line in enumerate(sen):
            # Iterating over sentence to get the topic, title, documentum type, lemmas,
            # for and the original sentence as text

            if i == 0:
                date = line[2]

            space = " " if line[9] == "_" else ""
            orig_sent.append(line[1] + space)

            if is_topic is True:
                if line[1].replace("*", "") != ".":
                    topic += line[1] + space
                else:
                    is_topic = False

            elif title_end is False:
                # lemmas.append(line[2])
                if self._is_huntype(line[2]):
                    self._doc_type = line[2]
                    title += self._doc_type
                    title_end = True
                    is_topic = True
                else:
                    title += line[1] + space

        self._identifier = self._pat_whitespaces.sub('', '_'.join(title.split())).lower(). \
            translate(str.maketrans(self._accent_dict))

        # From here: finalize global metadata values
        columns = '# global.columns = ' + ' '.join(self._header).upper()
        eng_type = self._get_eng_type(self._doc_type)
        hun_type = self._doc_type

        issuer = title.split()[-2] if hun_type != 'törvény' else 'parlament'
        issuer = "# issuer = " + issuer

        hun_type = "# type = " + hun_type
        eng_type = "# entype = " + eng_type

        title = "# title = " + title
        newdoc_id = "# newdoc id = hu-" + self._identifier
        date = "# date = " + date.split("/")[-1].replace(".", "")  # lemmas[0].split("/")[-1].replace(".", "")

        global_metadatas = [[columns], [newdoc_id], [date], [title], [hun_type], [eng_type], [issuer]]

        if topic != '':
            global_metadatas.append(["# topic = " + topic])

        return global_metadatas

    def _get_metadatas_per_sentence(self, sen):
        orig_sent = []
        for line in sen:
            space = " " if line[9] == "_" else ""
            orig_sent.append(line[1] + space)

        # from here: get metadatas per sentence
        paragraph_num = 1
        sentence = "".join(orig_sent)

        if self._doc_type == "törvény" or self._doc_type == "rendelet":
            paragraph = self._pat_paragraph.match(sentence)
            par_id = ""
            if self._sentence_count > 1 and paragraph:
                paragraph_num = int(paragraph.group().split(".")[0])

                if paragraph_num != 1:
                    par_id = "# newpar id = " + self._identifier + '-p' + str(paragraph_num)
            elif self._sentence_count == 1:
                par_id = "# newpar id = " + self._identifier + '-p' + str(paragraph_num)

            return ([par_id],
                    ["# sent_id = " + self._identifier + "-s" + str(self._sentence_count) + '-p' + str(
                        paragraph_num)],
                    ["# text = " + sentence])
        else:
            return (["# sent_id = " + self._identifier + "-s" + str(self._sentence_count)],
                    ["# text = " + sentence])
