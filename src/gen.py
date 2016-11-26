#!/usr/bin/env python3
import os
import shutil

from pa_tools.pa import pafs
from pa_tools.pa import paths
from pa_tools.pa import pajson

from pa_tools.mod.checker import check_mod
from pa_tools.mod.generator import update_modinfo, process_changes

from icons import generate_strat_icons

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
        src.mount('/src', '.')
        src.mount('/src/pa', 'pa')
        src.mount('/src/pa', 'pa_ex1')
    else:
        src.mount('/src', '.')
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

    # create the base file system
    src = create_source_fs(is_titans)
    modinfo = load_json(src, '/src/base_modinfo.json')
    modinfo.update(load_json(src, '/src/pa/modinfo.json'))
    modinfo = update_modinfo(modinfo)

    destination_path = os.path.join(out_dir, 'modinfo.json')
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, 'w', newline='\n') as dest:
        pajson.dump(modinfo, dest, indent=2)

    # mount the mod directory
    src.mount('/mod', out_dir)

    # remove destination files
    shutil.rmtree(os.path.join(out_dir, 'pa'), ignore_errors=True)

    ## Generate the mod
    sources = load_json(src, '/src/pa/sources.json')
    process_changes(sources, src, out_dir)

    # generate the stratigic icon effects
    print ('==== running strategic icon generator')
    src.unmount('/mod')
    src.mount('/', out_dir)
    process_changes(generate_strat_icons(src), src, out_dir)

    # analyse the mod for missing files
    mod_report = check_mod(out_dir)
    print(mod_report.printReport())

    ################# copy mod to pa mod directory
    mod_path = os.path.join(paths.PA_DATA_DIR, modinfo['context'] + '_mods', modinfo['identifier'])
    shutil.rmtree(mod_path, ignore_errors=True)
    shutil.copytree(out_dir, mod_path)

generate_mod(False)
generate_mod(True)
