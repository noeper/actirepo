from .question import Question

# numbering styles supported by moodle
NUMBERING_STYLES = {
    'abc': lambda i: chr(97 + i) + '.',
    'ABCD': lambda i: chr(65 + i) + '.',
    '123': lambda i: str(i + 1) + '.',
    'iii': lambda i: ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'][i % 10] + '.',
    'IIII': lambda i: ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'][i % 10] + '.',
}

class Ordering(Question):
    """
    Class to manage ordering questions
    """

    def __init__(self, element):
        super().__init__(element)
        # answers are shown in the right order (fraction is the position)
        answers = sorted(element.findall('answer'), key=lambda answer: float(answer.get('fraction')))
        numbering = NUMBERING_STYLES.get(element.findtext('numberingstyle', 'none'), lambda i: '')
        self.answers = [
            {
                "text": answer.find('text').text,
                "number": numbering(i)
            } for i, answer in enumerate(answers)
        ]
        self.horizontal = element.findtext('layouttype', 'VERTICAL') == 'HORIZONTAL'
