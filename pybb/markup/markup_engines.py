from pybb.markup.bbcode import BBCodeParser

class CustomBBCodeParser(BBCodeParser):
    def __init__(self):
        super(CustomBBCodeParser, self).__init__()
        self._parser.add_simple_formatter('ul', '<ul>%(value)s</ul>', transform_newlines=False, strip=True)
        self._parser.add_simple_formatter('li', '<li>%(value)s</li>', transform_newlines=False, strip=True)
        #self._parser.add_simple_formatter('img', '<img src="%(value)s">', replace_links=False)
        #<p><a href="%(value)s"><img src="%(value)s" height="100" width="100"/></a></p>
        self._parser.add_simple_formatter('img', '<p class="img_thumb"><a href="%(value)s"><img style="max-width:500px" src="%(value)s""/></a></p>',
                                          replace_links=False)
        self._parser.add_simple_formatter('youtube', """<script language="Javascript">var a = '%(value)s';var temp = new Array();temp = a.split('?v=');document.write('<object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/' + temp[1] + '&rel=0&color1=0xd6d6d6&color2=0xf0f0f0&border=1"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/' + temp[1] + '&rel=0&color1=0xd6d6d6&color2=0xf0f0f0&border=1" type="application/x-shockwave-flash" wmode="transparent" width="425" height="344"></embed></object>');</script> """,
                                          replace_links=False)