# -*- coding: utf-8 -*-
"""
create toc(table of content) about markdown file and directory
write the toc to README.MD and SUMMARY.MD
"""
import argparse
import os
import re
ignore_regx = ''
"""
<!---auto summary start--->

<!---auto summary end  --->
"""
def output_markdown_list(dire, base_dir, markdown_list, iter_depth=0):
    """Main iterator for get information from every file/folder
    """
    global ignore_regx
    for filename in sort_dir_file(os.listdir(dire), base_dir): 
        # add list and sort
        if ignore_regx and re.search(ignore_regx, filename,re.I):
            print('........ignore',filename)
            continue
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path): #is dir
            if mdfile_in_dir(file_or_path):
                # if there is .md files in the folder, output folder name
                markdown_list.append('  ' * iter_depth + '- ' + filename+"\n")
                output_markdown_list(file_or_path, base_dir, markdown_list, 
                                iter_depth + 1) # iteration
        elif is_markdown_file(filename):
            markdown_list.append('  ' * iter_depth + 
                '- [{}]({})\n'.format(is_markdown_file(filename), 
                    os.path.join(os.path.relpath(dire, base_dir), 
                                    filename)))
            # iter depth for indent, relpath and join to write link.

def mdfile_in_dir(dire):
    """Judge if there is .md file in the directory
    i: input directory
    o: return Ture if there is .md file; False if not.
    """
    for root, dirs, files in os.walk(dire):
        for filename in files:
            if re.search('.md$|.MD$', filename):
                return True
    return False

def is_markdown_file(filename):
    """ Judge if the filename is a markdown filename
    i: filename
    o: filename without '.md' or '.MD'
    """
    match = re.search('.md$|.MD$', filename)
    if not match:
        return False
    else:
        return filename[:-3]

def sort_dir_file(listdir, dire):
    # sort dirs and files, first files a-z, then dirs a-z
    list_of_file = []
    list_of_dir = []
    for filename in listdir:
        if os.path.isdir(os.path.join(dire, filename)):
            list_of_dir.append(filename)
        else: 
            list_of_file.append(filename)
    # first file then directory
    list_of_file.sort()
    list_of_dir.sort()
    for dire in list_of_dir:
        list_of_file.append(dire)
    return list_of_file  

def write_md_filename(filename, append):
    """ write markdown filename
    i: filename and append
    p: if append: find former list name and return
       else: write filename
    """
    if append:
        for line in former_summary_list:
            if re.search(filename, line):
                s = re.search('\[.*\]\(',line)
                return s.group()[1:-2]
        else:
            return is_markdown_file(filename)
    else:
        return is_markdown_file(filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ignore', 
                    help='regex for ignore filename', 
                    default="^_|node\_modules|summary|readme")
    parser.add_argument('-d', '--directory', 
                        help='the directory of your GitBook root',
                        default=".")
    parser.add_argument('-o', '--outfiles', 
                    help='the output files such as readme.md summary.md',
                    default=[],
                    action='append')                   
    args = parser.parse_args()
    dir_input = args.directory
    global ignore_regx
    ignore_regx = args.ignore
    outfiles = args.outfiles
    if not outfiles:
        outfiles = ['README.MD','SUMMARY.MD']
    print(args,outfiles,ignore_regx)

    # create mardown outlook 
    markdown_list = ["# SUMMARY\n"]
    output_markdown_list(dir_input, dir_input, markdown_list)

    # replace table of contents to output files
    for f in outfiles:
        with open(f,'w') as file:
            file.writelines(markdown_list)
    return 0

if __name__ == '__main__':
    main()
