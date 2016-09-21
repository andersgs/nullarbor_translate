'''
Read config file and expose the parameters for SOP IDs
'''

import yaml

class ConfigReader:
    def __init__(self):
        self.filenames = {}
    def read_config(self, configfile):
        fi = open(configfile)
        self.cfg = yaml.load(fi)
        fi.close()
    def add_sops(self):
        try:
            self.sops = self.cfg['sopid']
        except:
            self.sops = {}
    def add_filenames(self):
        self.filenames = self.cfg['nullarbor_files']
