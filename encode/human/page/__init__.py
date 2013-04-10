import codecs
from mrbob.rendering import parse_variables
from pkg_resources import get_provider

def rendered_var(variables, rendered):
    for render in rendered:
        provider = get_provider('encode.human')
        file_name = provider.get_resource_filename('encode.human', '%s/output/%s' % (render, render))
        variables[render] = codecs.open(file_name, 'r', 'utf-8').read()

def pre_render(self):
    self.variables = parse_variables(self.variables)
    rendered_var(self.variables, ['javascript', 'header', 'overlay', 'primary', 'secondary', 'footer'])
    
