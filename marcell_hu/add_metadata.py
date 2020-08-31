#! /usr/bin/env python3

import os
import re


class MMeta:
    pass_header = False

    def __init__(self, source_fields=None, target_fields=None):

        self.doc_types_hun_eng = {"határozat": "decree",
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

        self.header = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps',
                       'misc', 'marcell:ne', 'marcell:np', 'marcell:iate', 'marcell:eurovoc']

        self.sentence_count = 0
        self.pat_paragraph = re.compile(r'^\d+[.] *§')
        self.doc_type = ''

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

        # # todo identifier-hez kell a fájlnév. hogyan tudok hozzájutni?
        fname_wo_out = 'fájl_név001.txt'  # "_".join(os.path.basename(doc[0]).split("_")[1:])
        identifier = os.path.splitext(fname_wo_out)[0]

        orig_sent = []

        if self.sentence_count == 1:
            sen = sen[1:]
            # from here: collect and process global metadatas (per document)
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

            lemmas = []
            is_topic = False
            title_end = False
            title = ""
            topic = ""

            for line in sen:
                space = " " if line[9] == "_" else ""
                orig_sent.append(line[1] + space)

                if is_topic:
                    if line[1].replace("*", "") != ".":
                        topic += line[1] + space
                    else:
                        is_topic = False

                elif not title_end:
                    lemmas.append(line[2])
                    if self._is_huntype(line[2]):
                        self.doc_type = line[2]
                        title += self.doc_type
                        title_end = True
                        is_topic = True
                    else:
                        title += line[1] + space

            for metadata in self._get_metadatas(topic, identifier, lemmas,
                                               '# global.columns = ' + ' '.join(self.header), title.split()):
                yield metadata

        #     end of collecting and processing of global metadatas

        else:
            for line in sen:
                space = " " if line[9] == "_" else ""
                orig_sent.append(line[1] + space)

        # from here: get metadatas per sentence
        paragraph_num = 1
        sentence = "".join(orig_sent)

        if self.doc_type == "törvény" or self.doc_type == "rendelet":
            paragraph = self.pat_paragraph.match(sentence)
            par_id = ""
            if self.sentence_count > 1 and paragraph:
                paragraph_num = int(paragraph.group().split(".")[0])

                if paragraph_num != 1:
                    par_id = "# newpar id = " + identifier + '-p' + str(paragraph_num)
            elif self.sentence_count == 1:
                par_id = "# newpar id = " + identifier + '-p' + str(paragraph_num)

            for metadata in ([par_id],
                             ["# sent_id = " + identifier + "-s" + str(self.sentence_count) + '-p' + str(
                                 paragraph_num)],
                             ["# text = " + sentence]):
                yield metadata
        else:
            for metadata in (["# sent_id = " + identifier + "-s" + str(self.sentence_count)],
                             ["# text = " + sentence]):
                yield metadata

        # end of collect and process of metadatas per sentence

        for line in sen:
            yield line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """
        return field_names

    def _get_eng_type(self, word):
        if self._is_huntype(word):
            return self.doc_types_hun_eng[word]
        return "UNKNOWN"

    def _is_huntype(self, word):
        return word in self.doc_types_hun_eng.keys()

    def _get_metadatas(self, topic, identifier, lemmas, columns, title):
        eng_type = self._get_eng_type(lemmas[-1])
        hun_type = lemmas[-1]

        if hun_type != 'törvény':
            issuer = "# issuer = " + title[-2]
        else:
            issuer = "# issuer = parlament"

        title = "# title = " + " ".join(title)
        newdoc_id = "# newdoc id = hu-" + identifier
        date = "# date = " + lemmas[0].split("/")[-1].replace(".", "")
        hun_type = "# type = " + hun_type
        eng_type = "# entype = " + eng_type

        metadatas = [[columns], [newdoc_id], [date], [title], [hun_type], [eng_type], [issuer]]

        if topic:
            metadatas.append(["# topic = " + topic])

        return metadatas
