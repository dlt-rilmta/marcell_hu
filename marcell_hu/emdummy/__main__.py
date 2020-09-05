#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xtsv import build_pipeline, parser_skeleton


def main():

    argparser = parser_skeleton(description='EmDummy - a template module for xtsv')
    opts = argparser.parse_args()

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['dummy']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    # from emdummy import EmDummy
    em_dummy = ('emdummy', 'EmDummy', 'EXAMPLE (The friendly name of EmDummy used in REST API form)',
                ('Params', 'goes', 'here'), {'source_fields': {'form'},  # Source field names
                                             'target_fields': ['star']})  # Target field names
    tools = [(em_dummy, ('dummy', 'dummy-tagger', 'emDummy'))]

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
