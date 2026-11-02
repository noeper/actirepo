import re

from .question import Question

# input style used by moodle for cloze subquestions
INPUT_STYLE = "display:inline-block;vertical-align:baseline;height:32px;padding:4px 8px;margin:2px 4px;font-size:15px;font-weight:400;line-height:22.5px;color:rgb(73, 80, 87);background-color:rgb(255, 255, 255);border:1px solid rgb(143, 149, 158);border-radius:4px;box-sizing:border-box;font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Liberation Sans', sans-serif;"

# subquestion pattern: {weight:TYPE:answers} (escaped "\}" are allowed inside answers)
SUBQUESTION_PATTERN = re.compile(r'\{(\d*):([A-Z_]+):((?:\\.|[^\\}])*)\}')

# subquestion types and how they are rendered
SHORTANSWER_TYPES = { 'SA', 'SHORTANSWER', 'SAC', 'SHORTANSWER_C', 'MW', 'MWC' }
NUMERICAL_TYPES = { 'NM', 'NUMERICAL' }
DROPDOWN_TYPES = { 'MC', 'MULTICHOICE', 'MCS', 'MULTICHOICE_S' }
RADIO_TYPES = { 'MCV', 'MULTICHOICE_V', 'MCVS', 'MULTICHOICE_VS', 'MCH', 'MULTICHOICE_H', 'MCHS', 'MULTICHOICE_HS' }
CHECKBOX_TYPES = { 'MR', 'MULTIRESPONSE', 'MRS', 'MULTIRESPONSE_S', 'MRH', 'MULTIRESPONSE_H', 'MRHS', 'MULTIRESPONSE_HS' }

class Cloze(Question):
    """
    Class to manage cloze (embedded answers / multianswer) questions
    """

    def __init__(self, element):
        super().__init__(element)
        # moodle exports it as "cloze", but internally it is "multianswer"
        self.type = 'cloze'
        self.subquestions = []
        self.statement = SUBQUESTION_PATTERN.sub(self.__render_subquestion, self.statement)
        self.answers = self.subquestions

    def __parse_answers(self, text):
        """
        Parse subquestion answers
        - text: answers text (e.g. "=Gigabyte~Asus~%50%MSI#feedback")
        - return: list of answers with text, feedback and fraction
        """
        answers = []
        for answer in re.split(r'(?<!\\)~', text):
            fraction = 0.0
            if answer.startswith('='):
                fraction = 100.0
                answer = answer[1:]
            else:
                match = re.match(r'%(-?[\d.]+)%', answer)
                if match:
                    fraction = float(match.group(1))
                    answer = answer[match.end():]
            parts = re.split(r'(?<!\\)#', answer, maxsplit=1)
            unescape = lambda s: re.sub(r'\\([~#}/"\\])', r'\1', s).strip()
            answers.append({
                "text": unescape(parts[0]),
                "feedback": unescape(parts[1]) if len(parts) > 1 else '',
                "fraction": fraction
            })
        return answers

    def __render_subquestion(self, match):
        """
        Render a subquestion as a form control (showing the right answer)
        - match: regex match for {weight:TYPE:answers}
        - return: html
        """
        type = match.group(2)
        answers = self.__parse_answers(match.group(3))
        self.subquestions.append({ "type": type, "answers": answers })
        best = max(answers, key=lambda answer: answer['fraction'])
        if type in SHORTANSWER_TYPES or type in NUMERICAL_TYPES:
            value = best['text'].replace('"', '&quot;')
            # numerical answers may include a tolerance (e.g. "3.14:0.01")
            if type in NUMERICAL_TYPES:
                value = value.split(':')[0]
            size = max(len(answer['text']) for answer in answers) + 2
            return f'<input type="text" value="{value}" size="{size}" style="{INPUT_STYLE}" />'
        if type in DROPDOWN_TYPES:
            options = ''.join(f'<option{" selected" if answer is best else ""}>{answer["text"]}</option>' for answer in answers)
            return f'<select style="{INPUT_STYLE}">{options}</select>'
        if type in RADIO_TYPES or type in CHECKBOX_TYPES:
            input_type = 'checkbox' if type in CHECKBOX_TYPES else 'radio'
            checked = (lambda answer: answer['fraction'] > 0) if input_type == 'checkbox' else (lambda answer: answer is best)
            vertical = type.startswith(('MCV', 'MULTICHOICE_V', 'MR', 'MULTIRESPONSE')) and not type.startswith(('MRH', 'MULTIRESPONSE_H'))
            tag = 'div' if vertical else 'span'
            options = ''.join(
                f'<{tag} style="margin:2px 8px 2px 0px;white-space:nowrap;"><input type="{input_type}"{" checked" if checked(answer) else ""} style="margin:0px 4px;" />{answer["text"]}</{tag}>'
                for answer in answers
            )
            return f'<span style="display:inline-block;vertical-align:middle;">{options}</span>'
        # unknown subquestion type: mark the gap
        return f'<span style="{INPUT_STYLE}background-color:rgb(255, 243, 205);">[{best["text"]}]</span>'
