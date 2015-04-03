from pybb.markup.bbcode import BBCodeParser
import bbcode, re


class CustomBBCodeParser(BBCodeParser):
    def __init__(self):
        super(CustomBBCodeParser, self).__init__()
        self._parser.add_simple_formatter('ul', '<ul>%(value)s</ul>', transform_newlines=False, strip=True)
        self._parser.add_simple_formatter('li', '<li>%(value)s</li>', transform_newlines=False, strip=True)
        #self._parser.add_simple_formatter('img', '<img src="%(value)s">', replace_links=False)
        #<p><a href="%(value)s"><img src="%(value)s" height="100" width="100"/></a></p>
        self._parser.add_simple_formatter('img', '<p class="img_thumb"><a href="%(value)s"><img style="max-width:500px" src="%(value)s""/></a></p>',
                                          replace_links=False)
        #self._parser.add_simple_formatter('youtube', """<script language="Javascript">var a = '%(value)s';var temp = new Array();temp = a.split('?v=');document.write('<object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/' + temp[1] + '&rel=0&color1=0xd6d6d6&color2=0xf0f0f0&border=1"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/' + temp[1] + '&rel=0&color1=0xd6d6d6&color2=0xf0f0f0&border=1" type="application/x-shockwave-flash" wmode="transparent" width="425" height="344"></embed></object>');</script> """,
        #                                  replace_links=False)
        #self._parser.add_simple_formatter('size', ' <font size="6">%(value)s</font> ', replace_links=False)

        self._parser.add_formatter('youtube', render_youtube, replace_links=False)
        self._parser.add_formatter('size', render_size, replace_links=False)


def render_youtube(tag_name, value, options, parent, context):
    videoid = youtube_url_validation(value)
    return '<div class="flex-video widescreen"><iframe width="560" height="315" id="ytplayer" type="text/html" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe></div>' % (videoid)


def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    return youtube_regex_match

def render_size(tag_name, value, options, parent, context):
    try:
        text_size = options['size']
    except:
        text_size = "6"
    return '<font size="%s">%s</font>' % (text_size, value)