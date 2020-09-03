"""MARCELL_HU UTOLSÓ MODULJA, MEGADJA A VÉGSŐ INPUTOT"""

class MCorrect:
    pass_header = False

    def __init__(self, source_fields=None, target_fields=None):

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

        for line in sen:
            line[field_names[0]] = line[field_names[0]].replace('×', ';')
            line[field_names[1]] = line[field_names[1]].replace('×', ';')

            yield line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """
        return [field_names['marcell:iate'], field_names['marcell:eurovoc']]