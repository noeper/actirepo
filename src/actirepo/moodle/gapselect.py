import re

from .question import Question
from .cloze import INPUT_STYLE

class GapSelect(Question):
    """
    Class to manage select missing words questions
    """

    def __init__(self, element):
        super().__init__(element)
        self.choices = [
            {
                "text": option.find('text').text,
                "group": option.find('group').text
            } for option in element.findall('selectoption')
        ]
        self.answers = self.choices
        self.statement = re.sub(r'\[\[(\d+)\]\]', self.__render_gap, self.statement)

    def __render_gap(self, match):
        """
        Render a gap as a select with the right choice selected
        - match: regex match for [[n]]
        - return: html
        """
        index = int(match.group(1)) - 1
        if index >= len(self.choices):
            return match.group(0)
        right = self.choices[index]
        options = ''.join(
            f'<option{" selected" if choice is right else ""}>{choice["text"]}</option>'
            for choice in self.choices if choice['group'] == right['group']
        )
        return f'<select style="{INPUT_STYLE}">{options}</select>'
