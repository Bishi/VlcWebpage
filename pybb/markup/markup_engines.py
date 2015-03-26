from pybb.markup.bbcode import BBCodeParser

class CustomBBCodeParser(BBCodeParser):
    def __init__(self):
        super(CustomBBCodeParser, self).__init__()
        self._parser.add_simple_formatter('ul', '<ul>%(value)s</ul>', transform_newlines=False, strip=True)
        self._parser.add_simple_formatter('li', '<li>%(value)s</li>', transform_newlines=False, strip=True)
        #self._parser.add_simple_formatter('img', '<img src="%(value)s">', replace_links=False)
        #<p><a href="%(value)s"><img src="%(value)s" height="100" width="100"/></a></p>
        self._parser.add_simple_formatter('img', '<p class="img_thumb"><a href="%(value)s"><img style="max-width:500px" src="%(value)s""/></a></p>', replace_links=False)