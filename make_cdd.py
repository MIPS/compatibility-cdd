#!/usr/bin/python
"""
Utility for building the CDD from component markdown files.

From the compatibility/cdd directory, run python make-cdd.py.

Each generated CDD file is marked with a hash based on the content of the input files.

TODO(gdimino): Clean up and comment this code.
"""

from bs4 import BeautifulSoup
import hashlib
import markdown
import os
import pprint
import re
import tidylib
import subprocess

# TODO (gdimino): Clean up this code using templates
# from jinja2 import Template

HEADERS_FOR_TOC = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
ANDROID_VERSION = "7.0, (N)"
TOC_PER_COL = 34

def get_section_info(my_path):
  # (_, _, filenames) = os.walk(my_path).next()
  section_info = [];
  # Get section info from every file whose name contains a number. TODO: fix
  # this ugly hack.
  # for rootdir, subdirs, files in os.walk(my_path):
  for dir in get_immediate_subdirs(my_path):
    # for dir  in subdirs:
    if (not dir.isalpha() and dir != 'older-versions' and dir != '.git'):
      child_data = []
      print 'dir = ' + dir
      for file in os.listdir(dir):
        if '.md' in file:
          if file == 'index.md':
            number =  0
          else:
            number = int((file.split('_')[1]))
          print 'file = ' + file + ', dir = ' + dir
          html_string = markdown.markdown(unicode(open(my_path + '/' + dir + '/' + file, 'r').read(), 'utf-8'))
          child_data.append({'file': file,
                             'number': number,
                             'title': dir.split('_')[-1],
                             'html': html_string,
                             'children':[]})
      child_data.sort(key=lambda child: child['number'])
      section_info.append({'id': dir,
                           'number': int(''.join((dir.split('_')[:-1])).replace("_", ".")),
                           'title': dir.split('_')[-1],
                           'html': '',
                           'children':child_data})
  section_info.sort(key=lambda section: section['number'])
  return section_info


def get_soup(section_info):
  html_body_text = '''<!DOCTYPE html>
<head>
<title>Android ''' + ANDROID_VERSION + ''' Compatibility Definition</title>
<link rel="stylesheet" type="text/css" href="source/android-cdd.css"/>
</head>
<body>
<div id="main">'''

  for section in section_info:
     for child in section['children']:
       html_body_text += child['html']
  html_body_text +=  '</div></body><html>'
  return BeautifulSoup(html_body_text)


def add_id_to_section_headers(soup):
  header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
  for tag in soup.find_all(header_tags):
    tag['id'] = create_id(tag)

def old_generate_toc(soup):
  toc_html = ''
  header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
  for tag in soup.find_all(header_tags):
    tag_html = '<p class="toc_' + tag.name + '"><a href= "#' + create_id(tag) + '">' + tag.contents[0] + '</a></p>'
    toc_html = toc_html + tag_html
  return (BeautifulSoup(toc_html).body.contents, '')

def generate_toc(soup):
  toc_html = '<div id="toc">'
  header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
  toc_entries =  soup.find_all(header_tags)
  toc_chunks = [toc_entries[i:i + TOC_PER_COL] for i in xrange(0, len(toc_entries), TOC_PER_COL)]
  print 'Number of chunks =  %d' % len(toc_chunks)
  for chunk in toc_chunks:
    if not toc_chunks.index(chunk) %2:
      toc_html = toc_html + ('<div id="toc_left">')
      for tag in chunk:
        toc_html = toc_html + '<p class="toc_' + tag.name + '"><a href= "#' + create_id(tag) + '">' + tag.contents[0] + '</a></p>'
      toc_html = toc_html + ('</div>')
    else:
      toc_html = toc_html + ('<div id="toc_right">')
      for tag in chunk:
        toc_html = toc_html + '<p class="toc_' + tag.name + '"><a href= "#' + create_id(tag) + '">' + tag.contents[0] + '</a></p>'
      toc_html = toc_html + ('</div>')
      toc_html = toc_html + '<div style="clear: both; page-break-after:always; height:1px"></div>'
  toc_html = toc_html + '<div style="clear: both"></div>'
  return (BeautifulSoup(toc_html).body.contents)

def old_add_toc(soup):
  toc = soup.new_tag('div', id='toc')
  toc_left = soup.new_tag('div', id='toc_left')
  toc_right = soup.new_tag('div', id='toc_right')
  toc.append(toc_left)
  toc.append(toc_right)
  # toc_left.contents, toc_right.contents = generate_toc(soup)
  toc_left.contents, toc_right.contents = generate_toc(soup)
  toc_title =  BeautifulSoup("<h6>Table of Contents</h6>").body.contents[0]
  soup.body.insert(0,toc)
  soup.body.insert(0, toc_title)
  return soup

def add_toc(soup):
  toc_contents = generate_toc(soup)[0]
  toc_title =  BeautifulSoup("<h6>Table of Contents</h6>").body.contents[0]
  soup.body.insert(0, toc_contents)
  soup.body.insert(0, toc_title)
  return soup

def create_id(header_tag):
  return header_tag.contents[0].lower().replace('. ', '_').replace(' ', '_').replace('.', '_')

# Utilities
def get_immediate_subdirs(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

# Odds and ends

def check_section_numbering(soup):
  header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
  for tag in header_tags:
    headings = soup.find_all(tag)
    header_numbers = []
    for heading in headings:
      header_numbers.append(re.sub(r"([\d.]*).*", r"\1"), heading.contents)
  return true

def elim_para_whitespace(html):
  new_html = re.sub(re.compile(r"(<p[^>]*>)\s*\n\s*(<a[^>]*>)\n([^<]*)\n\s*(</a>)\n\s*(</p>)", re.M),r"\1\2\3\4\5\n", html)
  return new_html

def main():
  my_path = os.getcwd()
  section_info = get_section_info(my_path)
  soup = get_soup(section_info)
  add_id_to_section_headers(soup)
  add_toc(soup)
  html = soup.prettify(formatter='html')
  # Add a hash to the filename, so that identidal inputs produce the same output
  # file.
  output_filename = "test-generated-cdd-%s.html" % hashlib.md5(html).hexdigest()[0:5]
  output = open(output_filename, "w")
  output.write(html.encode('utf-8'))
  output.close()
  # Code to generate PDF, needs work.
  # subprocess.call('wkhtmltopdf -B 1in -T 1in -L .75in -R .75in page ' + output_filename +  ' --footer-html source/android-cdd-footer.html /tmp/android-cdd-body.pdf')


if __name__ == '__main__':
  main()




