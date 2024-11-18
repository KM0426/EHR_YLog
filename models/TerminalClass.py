class Terminal:
    def __init__(self,input_no):
        self.hidden_no = input_no
    @property
    def no(self):
        return self.hidden_no
    @no.setter
    def no(self,input_no):
        self.hidden_no = input_no
