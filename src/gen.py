#!/usr/bin/env python3
import os
import shutil

from pa_tools.pa import pafs
from pa_tools.pa import paths
from pa_tools.pa import pajson

from pa_tools.mod.checker import check_mod
from pa_tools.mod.generator import process_modinfo, process_changes

options, warnings = pajson.loadf('conf.json')
print ('======= Loading Options =======')
for w in warnings:
    print (w)
print ('debug mode: ', options.get('debug_mode', False))
print ('pretty printing: ', options.get('pretty_print_effects', True))
print ('-------------------------------')
print ('PA MEDIA DIR:', paths.PA_MEDIA_DIR)
print ('-------------------------------')
print ('')

def create_source_fs(is_titans):
    # setting up source file system
    src = pafs(paths.PA_MEDIA_DIR)
    if is_titans:
        src.mount('/pa', '/pa_ex1')
        src.mount('/src/pa', 'pa')    
        src.mount('/src/pa', 'pa_ex1')
    else:
        src.mount('/src/pa', 'pa')

    return src

def load_json(loader, path):
    resolved = loader.resolveFile(path)
    json, warnings = pajson.loadf(resolved)
    for w in warnings:
        print (w)
    return json


def generate_mod(is_titans):
    if is_titans:
        print ('TITANS')
        out_dir = '../titans'
    else:
        print('CLASSIC')
        out_dir = '../classic'

    shutil.rmtree(os.path.join(out_dir, 'pa'), ignore_errors=True)
    src = create_source_fs(is_titans)

    process_modinfo('/src/pa/modinfo.json', src, out_dir)
    
    modinfo = load_json(src, '/src/pa/modinfo.json')
    # mount the mod directory
    src.mount('/mod', out_dir)

    sources = load_json(src, '/src/pa/sources.json')
    process_changes(sources, src, out_dir)
    print ('')

    mod_report = check_mod(out_dir)
    print(mod_report.printReport())

    ################# copy mod to pa mod directory

    mod_path = os.path.join(paths.PA_DATA_DIR, modinfo['context'] + '_mods', modinfo['identifier'])
    shutil.rmtree(mod_path, ignore_errors=True)
    shutil.copytree(out_dir, mod_path)

generate_mod(False)
generate_mod(True)
