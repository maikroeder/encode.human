from mrbob.rendering import parse_variables

def pre_render(self):
    self.variables = parse_variables(self.variables)
    self.variables['dimensions'] = self.variables['dimensions'].split()
    about = u""
    for dimension in range(0, len(self.variables['dimensions'])):
        about += u'    $("#about_dimension_%s[rel]").overlay();\n' % dimension
    overlay = u'\n$(document).ready(function() {\n%s});\n' % about
    self.variables['overlay_javascript'] = overlay
    