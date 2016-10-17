from __future__ import print_function
'''
A module to import new functions dynamically into nullarbor_translate
'''

import sys
import os
import re
import imp

class FilterReader:
    def __init__(self, filters):
        self.filters = filters
        self.n_filters = len(self.filters)

    def add_filters(self, jinja_environment):
        for f in self.filters:
            try:
                # to take advantage of this, I need to hack the path to make
                # it look like a call to a module
                #import pdb; pdb.set_trace()
                f_abs_path = os.path.abspath(f)
                module_path = os.path.dirname(f_abs_path)
                filter_name = os.path.basename(f).strip('.py')
                fp, pathname, description = imp.find_module(filter_name, [module_path])
                new_filter_module = imp.load_module('mdu_tilde', fp, pathname, description)
                new_filter_function = getattr(new_filter_module, filter_name)
                jinja_environment.filters[filter_name] = new_filter_function
                print("Added filter {} to template environment.".format(f), file = sys.stderr)
            except:
                print("Could not load {} filter, please check path".format(f), file = sys.stderr)
