#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xtsv import build_pipeline, parser_skeleton


def main():
    argparser = parser_skeleton(description='MMeta - a module which add global and per-sentence metadata to tokenized '
                                            'and lemmatized emtsv output file')
    opts = argparser.parse_args()

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['mmeta']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    # from emdummy import EmDummy
    m_meta = ('mmeta', 'MMeta', 'Add metadata', (), {'source_fields': {'form', 'lemma'},
                                                     'target_fields': []})
    tools = [(m_meta, ('mmeta', 'mMeta'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # from xtsv import process
    # from emdummy import EmDummy
    # output_iterator.writelines(process(input_data, EmDummy(*em_dummy[3], **em_dummy[4])))

    # Alternative2: Run REST API debug server
    # from xtsv import pipeline_rest_api, singleton_store_factory
    # app = pipeline_rest_api('TEST', tools, {},  conll_comments=False, singleton_store=singleton_store_factory(),
    #                         form_title='TEST TITLE', doc_link='https://github.com/dlt-rilmta/emdummy')
    # app.run()


if __name__ == '__main__':
    main()
