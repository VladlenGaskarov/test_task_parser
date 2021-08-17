import os
import requests
from bs4 import BeautifulSoup as BeSo
import re
from urllib.parse import urlsplit


class ParseUrlData:
    def __init__(self, url1):
        self.url = url1
        r = requests.get(self.url)
        soup = BeSo(r.content, 'html.parser')
        self.tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
        self.tags_txt = list(map(lambda tag: tag.text, self.tags))
        self.url_part = urlsplit(self.url)
        self.domain = self.url_part.netloc
        self.finally_text = ''
        while re.fullmatch(r'h\d', self.tags[-1].name) is not None:
            self.tags.pop()

    def create_file(self):
        path = os.getcwd() + '/' + self.domain + '/'
        path_parts = str(self.url_part.path).strip('/').split('/')
        file_name = path_parts[-1] + '.txt'
        path_parts.pop()
        path += '/'.join(path_parts)
        try:
            os.makedirs(path)
        except WindowsError as e:
            print(e)
        file = open(path + '/' + file_name, 'w')
        file.write(self.finally_text)
        file.close()

    def remove_spaces(self):
        for i, tag in enumerate(self.tags):
            self.tags_txt[i] = re.sub(r'\s', ' ', self.tags_txt[i].strip().replace('\n', ' '))

    def convert_links(self, punctuation):
        for i, tag in enumerate(self.tags):
            for a in tag.find_all('a'):
                if a.attrs['href'][0] == '/':
                    preset = '[' + self.domain + a.attrs['href'].strip() + ']'
                else:
                    preset = '[' + a.attrs['href'].strip() + ']'
                self.tags_txt[i] = self.tags_txt[i].replace(a.text, preset)
                if a.text[-1] in punctuation:
                    self.tags_txt[i] = self.tags_txt[i] + a.text[-1]

    def format_text(self, length_base, punctuation):
        tag_final = ''
        length = length_base
        tags_txt = self.tags_txt
        for i, tag in enumerate(self.tags):
            while len(tags_txt[i]) > length_base:
                first_word = tags_txt[i].split(' ')[0]
                if len(first_word) > length_base:
                    tag_final = tag_final + first_word + '\n'
                    tags_txt[i] = tags_txt[i][len(first_word):].strip()
                elif tags_txt[i][length - 1] == " ":
                    tag_final = tag_final + tags_txt[i][0:length - 1] + '\n'
                    tags_txt[i] = tags_txt[i][length:]
                    length = length_base
                else:
                    length = length-1
            try:
                if tags_txt[i][-1] in punctuation or re.fullmatch(r'h\d', tag.name) is not None:
                    self.finally_text += tag_final + tags_txt[i] + '\n' * 2
            except IndexError:
                pass
            tag_final = ''
