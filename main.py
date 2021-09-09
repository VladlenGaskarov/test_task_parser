import sys
import ParseUrlData
import ParserSettings


length_base = int(ParserSettings.get_setting('settings.ini', 'Settings', 'length_base'))
punctuation = tuple(ParserSettings.get_setting('settings.ini', 'Settings', 'punctuation'))
url = sys.argv[1]
p = ParseUrlData.ParseUrlData(url)
p.remove_spaces()
p.convert_links(punctuation)
p.format_text(length_base, punctuation)
p.create_file()
