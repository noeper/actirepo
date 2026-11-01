from .question import Question

class Numerical(Question):
    """
    Class to manage numerical questions
    """

    def __init__(self, element):
        super().__init__(element)
        self.answers = [
            {
                "text": answer.find('text').text,
                "tolerance": answer.find('tolerance').text if answer.find('tolerance') is not None else '0',
                "fraction": float(answer.get('fraction'))
            } for answer in element.findall('answer')
        ]
        self.first_answer = max(self.answers, key=lambda answer: answer['fraction'])['text']
        self.units = [ unit.find('unit_name').text for unit in element.findall('units/unit') ]
