#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class EmDummy:
    """
    This is a dummy xtsv module. I can be used as a tutorial to write new modules to xtsv
    As some of the modules use JAVA we need to prepare with the static properties in advance before we init those
     modules. Some of the following properties serves this purpose. They can be left as emtpy string when the module
      does not use JAVA.
    : class_path: Path to append to the end of CLASS_PATH environment variable when loading in JAVA classes
    : vm_opts: Additional JAVA VM options, when needed appended to the end of the options list
    : pass_header: Pass or strip header when generating output. (Default: True)
    : fixed_order_tsv_input: Use the TSV reader code from xtsv, but without header on fixed columns
     One may not pass the (output) header only when
      - the module is the last in the pipeline! Eg. to generate generic fixed-order TSV or ConLL-U formated output
      - one want to continue the pipeline in fixed-order TSV mode
    """
    class_path = ''  # TODO set or omit
    vm_opts = ''  # TODO set or omit
    pass_header = True  # TODO set or omit default: True
    fixed_order_tsv_input = False  # TODO set or omit default: False

    def __init__(self, *_, source_fields=None, target_fields=None):
        """
        The initialisation of the module. One can extend the lsit of parameters as needed. The mandatory fields which
         should be set by keywords are the following:
        :param source_fields: the set of names of the input fields
        :param target_fields: the list of names of the output fields in generation order
        """
        # Custom code goes here

        # Field names for xtsv (the code below is mandatory for an xtsv module)
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        """
        Process one sentence per function call
        :param sen: the list of all tokens in the sentence, each token contain all fields
        :param field_names: the prepared field_names from prepare_fields() to select the appropriate input field
         to process
        :return: the sen object augmented with the output field values for each token
        """
        [tok.append('*') for tok in sen]
        return sen                                   # TODO: Implement or overload on inherit

    def prepare_fields(self, field_names):
        """
        This function is called once before processing the input. It can be used to initialise field conversion classes
         to accomodate the current order of fields (eg. field to features)
        :param field_names: the dictionary of the names of the input fields mapped to their order in the input stream
        :return: the list of the initialised feature classes as required for process_sentence (in most cases the
         columnnumbers of the required field in the required order are sufficient
         eg. return [field_names['form'], field_names['lemma'], field_names['xpostag'], ...] )
        """
        return field_names                           # TODO: Implement or overload on inherit

    def process_token(self, token):  # TODO implement or omit
        """
        This function is called when the REST API is called in 'one word mode' eg. GET /stem/this_word .
        It is not mandatory. If not present but sill called by the REST API an exception is raised.
        See EmMorphPy or HunspellPy for implementation example

        :param token: The input token
        :return: the processed output of the token preferably raw string or JSON string
        """
        return token
