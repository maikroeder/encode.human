from time import localtime, strftime

def pre_render(self):
	date = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	self.variables['generated_date'] = date