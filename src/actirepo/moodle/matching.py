from .question import Question

class Matching(Question):
    """
    Class to manage matching questions
    """

    def __init__(self, element):
        super().__init__(element)
        # subquestions without text are distractors: they only add an option
        self.subquestions = [
            {
                "text": self._process_text(subquestion),
                "answer": subquestion.find('answer').find('text').text
            } for subquestion in element.findall('subquestion') if (subquestion.find('text').text or '').strip()
        ]
        self.options = []
        for subquestion in element.findall('subquestion'):
            option = subquestion.find('answer').find('text').text
            if option not in self.options:
                self.options.append(option)
        self.answers = self.subquestions
