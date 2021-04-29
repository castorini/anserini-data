import re
import os
import glob
import json

raw = os.getcwd() + '/uncompressed/'

def get_paragraphs(body):
    regex = '<pre>.*?</pre>'
    pattern = re.compile(regex)
    return re.findall(pattern, body)

def get_bullets(body):
    regex = '<ul>.*?</ul>'
    pattern = re.compile(regex)
    return re.findall(pattern, body)

def get_text(body):
    regex = r'<[^>]+>|[^<]+'
    pattern = re.compile(regex)
    return " ".join([t.strip() for t in
              re.findall(pattern, body)
                     if not '<' in t])

def get_title(text):
    regex = '<title>(.+?)</title>'
    pattern = re.compile(regex)
    return re.findall(pattern, text)

def parseHtml(raw_html):
    extracted_text = ''
    title = get_title(raw_html)
    if len(title) > 0:
        extracted_text += title[0] + '\n'
    paragraphs = get_paragraphs(raw_html)
    for paragraph in paragraphs:
        extracted_text += get_text(paragraph).replace('   ',' ').replace('   ',' ').replace('  ', ' ') + '\n'
    bullets = get_bullets(raw_html)
    for bullet in bullets:
        extracted_text += get_text(bullet).replace('   ',' ').replace('   ',' ').replace('  ', ' ') + '\n'
    return extracted_text.replace('    ',' ').replace('   ',' ').replace('  ', ' ')

with open (os.getcwd() + '/jsonl/docs.json', 'w') as output_jsonl_file:
    print(os.getcwd() + '/jsonl/docs.json')
    for root, dirs, files in os.walk(raw):
        for document in files:
            with open (raw + document, 'r') as htmlFile:
                doc_id = document.replace('.html','')
                extracted_text = parseHtml(htmlFile.read().replace('\n',' ').replace('\t',' ').replace('   ',' ').replace('  ', ' '))             
                output_dict = {'id': doc_id, 'contents': extracted_text}
                output_jsonl_file.write(json.dumps(output_dict) + '\n')
