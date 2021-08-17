import sys
import ParseUrlData

length_base = 80
punctuation1 = ('.', '!', '?')
# url = sys.argv[1]
url = "https://kotaku.com/valve-patched-a-steam-exploit-that-let-users-add-unlimi-1847490455"
p = ParseUrlData.ParseUrlData(url)
p.remove_spaces()
p.convert_links(punctuation1)
p.format_text(length_base, punctuation1)
p.create_file()
