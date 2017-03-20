#!/usr/bin/env python3
# coding: utf-8

# Appex script to copy a git file, folder, or repo from the Working Copy app

# Inspired by:
# https://github.com/cclauss/Pythonista-and-Working-Copy

import appex, os, shutil, console, sys
from zipfile import ZipFile

BASE_DIR = os.path.abspath(os.path.expanduser('~/Documents/'))

def import_from_working_copy():
    src_path = get_src_path()
    dest_path = get_dest_path(src_path)
    shutil.copy2(src_path, dest_path)
    process_imported_file(dest_path)
    console.hud_alert('Imported', 'success', 1)
    appex.finish()

def process_imported_file(file_path):
    file_root, file_ext = os.path.splitext(file_path)
    if file_ext == '.zip':
        action = console.alert('Extract ZIP File', 'Extract contents to directory and remove ZIP file?', 'Yes', 'No', hide_cancel_button=True)
        if action == 1:
            with ZipFile(file_path, 'r') as zip_file:
                # Delete the directory we're about to expand into if it's present.
                if os.path.exists(file_root):
                    shutil.rmtree(file_root)
                zip_file.extractall(file_root)
            # Delete the ZIP file
            os.remove(file_path)
                

def get_src_path():
    src_path = appex.get_file_path()
    if src_path == None:
        console.alert('No input file provided', 'error')
        appex.finish()
        sys.exit(1)
    return src_path
    
def get_dest_path(src_path):
    dest_path = src_path.split('/tmp/')[-1]
    dest_path = os.path.join(BASE_DIR, dest_path)
    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dest_path

def main():
    if appex.is_running_extension():
        import_from_working_copy()
    else:
        print('''* In Working Copy app select a repo, file, or directory to be copied into Pythonista.\n* Click the Share icon at the upper right.\n* Click Run Pythonista Script.\n* Pick this script and click the run button.\n* When you return to Pythonista the files should be in the main directory.''')

if __name__ == '__main__':
    main()
