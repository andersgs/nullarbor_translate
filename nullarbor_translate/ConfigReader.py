'''
Read config file and expose the parameters for SOP IDs
'''

import yaml

class ConfigReader:
    def __init__(self):
        self.mlst_sop_id = ''
        self.filenames = {}
    def read_config(self, configfile):
        fi = open(configfile)
        self.cfg = yaml.load(fi)
        fi.close()
    def add_sops(self):
        try:
            sops = self.cfg['sopid']
        except:
            sops = {}
    def add_filenames(self):
        self.filenames = self.cfg['nullarbor_files']
