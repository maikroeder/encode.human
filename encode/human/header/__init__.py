def pre_render(self):
    for variable in self.variables.items():
        self.variables['static.overlay'] = "enter"
