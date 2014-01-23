#!/usr/bin/env python

import json
import os
import re
import shutil

source_dir = '../Talks/objc-runtime-2/'
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
markdown = re.sub('\]\((\.\./)*', '](', markdown)
file(os.path.join(target_dir, 'presentation.md'), 'w').write(markdown)