"""
This is the encode.human Python module.
"""
import pandas as pd
from mrbob.rendering import parse_variables
from encode.human.csvreader import parse

def counter():
    i = 0
    while True:
       yield i
       i += 1

def debug(arg1, arg2):
	import pdb; pdb.set_trace()

def render_subtable(frame):
    return ""
    settings = {'index': ['Lab', 
                          'Biological Replicate', 
                          'Sample Internal Name', 
                          'Read Type',
                          'Insert Length',
                          'Treatment'],
                'meta': ['File URL', 
                         'dateUnrestricted'],
                'label': 'File View',
                'column': 'File Type'}
    context = {'settings':settings}
    context['grouped'] = frame.groupby(settings['index'])
    context['settings'] = settings
    context['template_folder'] = 'template'
    context['dimensions'] = settings['meta']
    context['version'] = 'version'
    context['column_headers'] = sorted(frame[settings['column']].unique())
    return render_template(context, 'subtable')

def level_1(self):
    self.variables = parse_variables(self.variables)
    self.variables['measure'] = lambda x:len(set(x))
    self.variables['render_subtable'] = render_subtable
    self.variables['colours'] = self.variables['colours'].split()
    self.variables['dimensions'] = self.variables['dimensions'].split()
    self.variables['left_row_left'] = self.variables['left_row_left'].split()
    self.variables['left_row_right'] = self.variables['left_row_right'].split()
    self.variables['left_row'] = self.variables['left_row_left'] + self.variables['left_row_right'] 
    self.variables['left_rows'] = list(self.variables['frame'].groupby(self.variables['left_row']).ix.keys())
    self.variables['grouped'] = self.variables['frame'].groupby(self.variables['dimensions'])
    url_template = self.variables['url_template']
    number = 0
    for dimension_id in self.variables['dimensions']:
        dimension = self.variables['dimension'][dimension_id.lower()]
        dimension['url'] = url_template % dimension['encode_id']
        unique_values = list(self.variables['frame'][dimension['id']].unique())
        dimension['unique_values'] = unique_values
        dimension['number'] = number
        if dimension_id == self.variables['colour']:
            dimension['colour_mapping'] = {}
            for index, value in enumerate(unique_values):
                dimension['colour_mapping'][value] = self.variables['colours'][index]
        number = number + 1
    self.variables['counter'] = counter()
    self.variables['debug'] = debug


def level_2(self):
    self.variables = parse_variables(self.variables)
    self.variables['dimensions'] = self.variables['dimensions'].split()
    self.variables['index'] = self.variables['index'].split()
    #self.variables['grouped'] = self.variables['frame'].groupby(self.variables['index'])
    self.variables['column_headers'] = sorted(self.variables['frame'][self.variables['column']].unique())
    number = 0
    for dimension_id in self.variables['dimensions']:
        dimension = self.variables['dimension'][dimension_id.lower()]
        unique_values = list(self.variables['frame'][dimension['id']].unique())
        dimension['unique_values'] = unique_values
        dimension['number'] = number
        number = number + 1
    self.variables['counter'] = counter()
    self.variables['debug'] = debug
    self.variables['template_folder'] = ''

def level_3(self):
    self.variables = parse_variables(self.variables)
    self.variables['dimensions'] = self.variables['dimensions'].split()
    number = 0
    for dimension_id in self.variables['dimensions']:
        dimension = self.variables['dimension'][dimension_id.lower()]
        unique_values = list(self.variables['frame'][dimension['id']].unique())
        dimension['unique_values'] = unique_values
        dimension['number'] = number
        number = number + 1

def get_frame(self):
    # Read the input file in ENCODE format
    file_path = 'encode/human/apache_export/hg19_RNA_dashboard_files.txt'
    frame = pd.DataFrame(parse(file_path), dtype=object)
    frame['dateunrestricted'] = frame['dateUnrestricted']
    frame['biologicalreplicate'] = frame['replicate']
    frame['readtype'] = frame['readType']
    frame['insertlength'] = frame['insertLength'].fillna('')
    frame['fileview'] = frame['view']
    frame['rnaextract'] = frame['rnaExtract']
    frame['filetype'] = frame['type']
    frame['fileurl'] = frame['File URL']
    frame['treatment'] = frame['treatment'].fillna('')
    frame['technology'] = frame['dataType'] + ' (' + frame['grant'] + ')'
    frame['compartment'] = frame['localization'].fillna('cell').map({'cell':'Whole-cell'})
    frame['labExpId'] = frame['labExpId'].map(lambda x: tuple(x.split(',')))
    frame['sampleinternalname'] = frame['labExpId'].map(lambda x: ', '.join(x))
    self.variables['frame'] = frame



def get_frame(self):
    # Read the input file in ENCODE format
    file_path = 'encode/human/apache_export/hg19_RNA_dashboard_files.txt'
    frame = pd.DataFrame(parse(file_path), dtype=object)
    frame['Lab'] = frame['lab']
    frame['Sample Replicate'] = frame['replicate']
    frame['Biological Replicate'] = frame['Sample Replicate']
    frame['Read Type'] = frame['readType']
    frame['Replicate Insert Length'] = frame['insertLength']
    frame['Insert Length'] = frame['Replicate Insert Length'].fillna('')
    frame['File View'] = frame['view']
    frame['File Type'] = frame['type']


    def to_tier(x):
        tier = {'GM1287':'1',
                'H1-hESC':'1',
                'K562':'1',
                'A549':'2',
                'HUVEC':'2',
                'HeLa-S3':'2',
                'HepG2':'2',
                'IMR90':'2',
                'MCF-7':'2',
                'Monocytes-CD14+':'2',
                'SK-N-SH':'2',
        }
        if x in tier:
            return tier[x]
        else:
            return '3'
    frame['Tier'] = frame['cell'].map(to_tier)
    frame['cell'] = frame['cell'].fillna('')
    frame['strain'] = frame['strain'].fillna('')
    frame['age'] = frame['age'].fillna('')
    frame['sex'] = frame['sex'].fillna('')
    frame['dataType'] = frame['dataType'].fillna('')
    frame['grant'] = frame['grant'].fillna('')
    frame['rnaExtract'] = frame['rnaExtract'].fillna('')
    frame['Treatment'] = frame['treatment'].fillna('')
    frame['localization'] = frame['localization'].fillna('cell')
    frame['Compartment'] = frame['localization']
    
    frame['Technology'] = frame['dataType'] + ' (' + frame['grant'] + ')'
    frame['labExpId'] = frame['labExpId'].fillna('')
    frame['labExpId'] = frame['labExpId'].map(lambda x: tuple(x.split(',')))
    frame['Sample Internal Name'] = frame['labExpId'].map(lambda x: ', '.join(x))
 
    frame['rnaextract'] = frame['rnaExtract']
    frame['compartment'] = frame['localization'].fillna('cell')
    frame['technology'] = frame['dataType'] + ' (' + frame['grant'] + ')'
    frame['treatment'] = frame['treatment'].fillna('')

    frame['filetype'] = frame['type']
    frame['fileurl'] = frame['File URL']
    frame['biologicalreplicate'] = frame['replicate']
    frame['sampleinternalname'] = frame['labExpId'].map(lambda x: ', '.join(x))
    frame['readtype'] = frame['readType']
    frame['insertlength'] = frame['insertLength'].fillna('')
    frame['fileview'] = frame['view']
    frame['dateunrestricted'] = frame['dateUnrestricted']

    self.variables['frame'] = frame

