import re

from .question import Question

# background colors used by moodle for each group of drag boxes
GROUP_COLORS = [ 'rgb(255, 255, 255)', 'rgb(176, 196, 222)', 'rgb(220, 220, 170)', 'rgb(216, 191, 216)', 'rgb(135, 206, 250)', 'rgb(218, 165, 32)', 'rgb(255, 215, 0)', 'rgb(240, 128, 128)' ]

# style for drag boxes
DRAG_STYLE = "display:inline-block;padding:2px 8px;margin:2px 4px;border:1px solid rgb(0, 0, 0);border-radius:4px;box-sizing:border-box;font-size:15px;line-height:22.5px;"

class DDWtoS(Question):
    """
    Class to manage drag and drop into text questions
    """

    def __init__(self, element):
        super().__init__(element)
        self.choices = [
            {
                "text": dragbox.find('text').text,
                "group": int(dragbox.find('group').text or 1),
                "infinite": dragbox.find('infinite') is not None,
                "color": GROUP_COLORS[(int(dragbox.find('group').text or 1) - 1) % len(GROUP_COLORS)]
            } for dragbox in element.findall('dragbox')
        ]
        self.answers = self.choices
        self.drag_style = DRAG_STYLE
        self.statement = re.sub(r'\[\[(\d+)\]\]', self.__render_drop, self.statement)

    def __render_drop(self, match):
        """
        Render a drop zone with the right choice dropped into it
        - match: regex match for [[n]]
        - return: html
        """
        index = int(match.group(1)) - 1
        if index >= len(self.choices):
            return match.group(0)
        choice = self.choices[index]
        return f'<span style="{DRAG_STYLE}background-color:{choice["color"]};">{choice["text"]}</span>'
