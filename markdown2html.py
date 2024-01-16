#!/usr/bin/python3
''' write a script markdown2html that takes an argument 2 strings:

    first argument is name of the Markdown file
    second argument is output file name
'''

import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            Unordered_start, Ordered_start, paragrapH = False, False, False
            # Bold syntax
            for line in read:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Md5
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md6_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md6_inside[0].encode()).hexdigest())

                # Remove the letter C
                remove_Letter_c = re.findall(r'\(\(.+?\)\)', line)
                remove_C_more = re.findall(r'\(\((.+?)\)\)', line)
                if remove_Letter_c:
                    remove_C_more = ''.join(
                        c for c in remove_C_more[0] if c not in 'Cc')
                    line = line.replace(remove_Letter_c[0], remove_C_more)

                Length = len(line)
                heading = line.lstrip('#')
                heading_Num = Length - len(heading)
                unorDered = line.lstrip('-')
                unorDered_num = Length - len(unorDered)
                Ordered = line.lstrip('*')
                Ordered_num = Length - len(Ordered)
                # Headings, lists
                if 1 <= heading_Num <= 6:
                    line = '<h{}>'.format(
                        heading_Num) + heading.strip() + '</h{}>\n'.format(
                        heading_Num)

                if unorDered_num:
                    if not Unordered_start:
                        html.write('<ul>\n')
                        Unordered_start = True
                    line = '<li>' + unorDered.strip() + '</li>\n'
                if Unordered_start and not unorDered_num:
                    html.write('</ul>\n')
                    Unordered_start = False

                if Ordered_num:
                    if not Ordered_start:
                        html.write('<ol>\n')
                        Ordered_start = True
                    line = '<li>' + Ordered.strip() + '</li>\n'
                if Ordered_start and not Ordered_num:
                    html.write('</ol>\n')
                    Ordered_start = False

                if not (heading_Num or Unordered_start or Ordered_start):
                    if not paragrapH and Length > 1:
                        html.write('<p>\n')
                        paragrapH = True
                    elif Length > 1:
                        html.write('<br/>\n')
                    elif paragrapH:
                        html.write('</p>\n')
                        paragrapH = False

                if Length > 1:
                    html.write(line)

            if Unordered_start:
                html.write('</ul>\n')
            if Ordered_start:
                html.write('</ol>\n')
            if paragrapH:
                html.write('</p>\n')
    exit(0)
