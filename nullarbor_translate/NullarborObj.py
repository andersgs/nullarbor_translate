'''
A class to create an object that can be rendered using a Jinja2 template
'''

import json
import pandas as pd
import os
import re
from Bio import SeqIO

class NullarborObj:
    def __init__(self, report_folder, job_number):
        self.report_folder = report_folder
        self.job_id = job_number
        pass
    def __read_csv__(self, filename, index_col = 0 ):
        return( pd.read_csv( os.path.join( self.report_folder,  filename ), index_col = index_col ) )
    def __parse_mlst__(self,isolate_id, row, allele_cols):
        isolate = {}
        isolate['id'] = isolate_id
        isolate['scheme'] = row['Scheme']
        isolate["st"] = row['SequenceType']
        isolate["alleles"] = row[allele_cols].values.tolist()
        if ( row['Quality'] == '&#10004;'):
            isolate['quality'] = 'PASSED'
        elif (row['Quality'] == '?'):
            isolate['quality'] = '?'
        elif (row['Quality'] == '&#10008;'):
            isolate['quality'] = 'FAILED'
        else:
            isolate['quality'] = 'UNKNOWN'
        return(isolate)
    def __parse_resistome__(self, isolate_id, row):
        isolate = {}
        isolate['id'] = isolate_id
        isolate['n_genes'] = int( row['Found'] )
        if isolate['n_genes'] == 0:
            isolate['results'] = []
            isolate['partials'] = []
        else:
            results_ix = row[1:] == '&#10004;' # finds full gene/allele match
            isolate['results'] = row[1:][results_ix].index.values.tolist()
            partials_ix = row[1:] == '?' # finds partial matches
            isolate['partials'] = row[1:][partials_ix].index.values.tolist()
        return( isolate )
    def __parse_ref__(self, seq_id, row):
        ref = {}
        ref['id'] = seq_id
        ref['description'] = row['Description']
        ref['length'] = row['Length']
        return( ref )
    def add_mlst(self, mlst_file ):
        mlst_res = self.__read_csv__( mlst_file )
        self.mlst_header = [re.sub('\.[0-9]', '', i) for i in mlst_res.columns.values.tolist()]
        allele_columns = [col for col in mlst_res.columns if re.match('Allele', col)]
        self.mlst_isolates = [self.__parse_mlst__(i, mlst_res.loc[i], allele_columns) for i in mlst_res.index.values]
    def add_newick( self, newick_file ):
        fi = open( newick_file, 'r')
        self.newick = ''
        for l in fi:
            self.newick += l.strip()
        fi.close()
    def add_core_aln( self, core_aln_file ):
        self.core_aln = []
        fi = open( core_aln_file, 'r' )
        seqs = SeqIO.parse( fi, 'fasta' )
        for s in seqs:
            tmp = {}
            tmp["id"] = s.id
            tmp["seq"] = str(s.seq)
            self.core_aln.append(tmp)
        fi.close()
    def add_resistome( self, resistome_file ):
        resistome_res = self.__read_csv__( resistome_file )
        # address the issue of extra spaces in the header
        clean_cols = [h.strip() for h in resistome_res.columns.values.tolist()]
        resistome_res.columns = clean_cols
        # parse the resistome
        self.resistome_isolates = [self.__parse_resistome__(i, resistome_res.loc[i]) for i in resistome_res.index.values]
    def add_reference( self, reference_file ):
        ref_tab = self.__read_csv__( reference_file )
        self.reference = [self.__parse_ref__(i, ref_tab.loc[i]) for i in ref_tab.index.values if i != 'TOTAL']
    def add_jobinfo( self, jobinfo_file ):
        jobinfo_tab = self.__read_csv__( jobinfo_file, index_col = None )
        self.jobinfo = {}
        self.jobinfo['author'] = jobinfo_tab.Author.iloc[0]
        self.jobinfo['date'] = jobinfo_tab.Date.iloc[0]
        self.jobinfo['isolates'] = jobinfo_tab.Isolates.iloc[0]
        self.jobinfo['host'] = jobinfo_tab.Host.iloc[0]
        self.jobinfo['folder'] = jobinfo_tab.Folder.iloc[0]
    def add_sops( self, sop_ids ):
        self.sop_id = sop_ids
    def render_template(self, template):
        tmp = template.render(nullarbor = self)
        print(tmp)
