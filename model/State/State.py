class State:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def get_color_representation(self):
        return self.color

    def get_value(self):
        return self.value
