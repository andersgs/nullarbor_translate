'''
A class to create an object that can be rendered using a Jinja2 template
'''

import json
import pandas as pd
import os
import re

class NullarborObj:
    def __init__(self, report_folder, job_number):
        self.report_folder = report_folder
        self.job_id = job_number
        pass
    def __parse_mlst__(self,isolate_id, row, allele_cols):
        line = {}
        line['id'] = isolate_id
        line['scheme'] = row['Scheme']
        line["st"] = row['SequenceType']
        line["alleles"] = row[allele_cols].values.tolist()
        if ( row['Quality'] == '&#10004;'):
            line['quality'] = 'PASSED'
        elif (row['Quality'] == '?'):
            line['quality'] = '?'
        elif (row['Quality'] == '&#10008;'):
            line['quality'] = 'FAILED'
        else:
            line['quality'] = 'UNKNOWN'
        return(line)
    def add_mlst(self, mlst_file, mlst_sop = '' ):
        self.mlst_sop = mlst_sop
        mlst_res = pd.read_csv( os.path.join( self.report_folder,  mlst_file ), index_col = 0 )
        self.mlst_header = [re.sub('\.[0-9]', '', i) for i in mlst_res.columns.values.tolist()]
        allele_columns = [col for col in mlst_res.columns if re.match('Allele', col)]
        self.mlst_isolates = [self.__parse_mlst__(i, mlst_res.loc[i], allele_columns) for i in mlst_res.index.values]
    def render_template(self, template):
        tmp = template.render(job_id = self.job_id,
                        mlst_sop_id = self.mlst_sop,
                        mlst_header = self.mlst_header,
                        mlst_isolates = self.mlst_isolates)
        print(tmp)
