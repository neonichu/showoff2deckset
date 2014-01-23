#!/usr/bin/env python

import json
import os
import re
import shutil
import sys

if not len(sys.argv) > 1:
	print 'Usage: %s /path/to/showoff/directory' % sys.argv[0]
	sys.exit(1)
source_dir = sys.argv[1]

metadata = json.loads(file(os.path.join(source_dir, 'showoff.json')).read())
target_dir = metadata['name']

try:
	os.mkdir(target_dir)
except:
	pass

for file_path in os.listdir(source_dir):
	full_path = os.path.join(source_dir, file_path)
	if os.path.splitext(file_path)[1] in ['.jpg', '.png']:
		shutil.copyfile(full_path, os.path.join(target_dir, file_path))

markdown = ''
for section in metadata['sections']:
	md_path = os.path.join(source_dir, section['section'])
	for file_path in os.listdir(md_path):
		full_path = os.path.join(md_path, file_path)
		if os.path.splitext(file_path)[1] in ['.jpg', '.png']:
			shutil.copyfile(full_path, os.path.join(target_dir, file_path))
		if os.path.splitext(file_path)[1] != '.md':
			continue
		markdown += file(full_path).read()

markdown = re.sub('!SLIDE.*', '---', markdown)
markdown = re.sub('^---', '', markdown)
markdown = re.sub('.notes.*', '', markdown)
markdown = re.sub('<img src="(.*?)" .*?/>', '![](\g<1>)', markdown)
markdown = re.sub('\]\((\.\./)*', '](', markdown)

slides = markdown.split('---')
output = ''
for idx, slide in enumerate(slides):
	if '@@@ ' in slide:
		slide = re.sub('@@@ ', '```', slide)
		slide += '\n\t```'
	output += slide
	if idx + 1 < len(slides):
		output += '\n---\n'
output = '\n'.join([x.strip() for x in output.split('\n') if x.strip()])
output = re.sub('---', '\n---\n', output)
file(os.path.join(target_dir, 'presentation.md'), 'w').write(output)
