import os

book_title = 'woterbuch_de_ru'
book_src_folder = book_title
book_file = book_title + '.fb2'
book_sources = os.listdir(book_src_folder)
book_sources.sort()

chapters = []
for source in book_sources:
    with open(os.path.join(book_src_folder, source), 'r') as source_file:
        chapters.append(source_file.readlines())
book_header = \
    '<?xml version="1.0" encoding="utf-8"?>\n' + \
    '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">\n' + \
    '<body>\n'

book_contents = []
for chapter in chapters:
    book_chapter = '<section>\n<title>' + chapter[0] + '</title>\n<empty-line/>\n<p>\n'
    for word in chapter[1:]:
        book_chapter += word + '<br/>\n'
    book_chapter += '</p></section>\n'
    book_contents.append(book_chapter)

book_footer = '</body></FictionBook>'

if os.path.exists(book_file):
    os.remove(book_file)
with open(book_file, 'w') as output_file:
    output_file.write(book_header)
    output_file.writelines(book_contents)
    output_file.write(book_footer)


