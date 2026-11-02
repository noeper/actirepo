from .question import Question

class Description(Question):
    """
    Class to manage descriptions (text only, no answers)
    """

    def __init__(self, element):
        super().__init__(element)
        self.answers = []
