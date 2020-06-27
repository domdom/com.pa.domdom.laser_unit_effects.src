#!/usr/bin/env python3
import os
import shutil
from distutils import dir_util

from pa_tools.pa import pafs
from pa_tools.pa import paths
from pa_tools.pa import pajson
from pa_tools.pa import spec

from pa_tools.mod.checker import check_mod
from pa_tools.mod.generator import update_modinfo, process_changes

from pa_tools.mod.utils import deploy_debug, create_pafs, restore

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
    src = create_pafs(is_titans)
    src.mount('/src', '.')
    src.mount('/src/pa', 'pa')

    if is_titans:
        src.mount('/src/pa', 'pa_ex1')

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

    # mount the mod directory
    src.mount('/mod', out_dir)

    modinfo = load_json(src, '/src/base_modinfo.json')
    modinfo.update(load_json(src, '/src/pa/modinfo.json'))
    modinfo = update_modinfo(modinfo, load_json(src, '/mod/modinfo.json'))

    destination_path = os.path.join(out_dir, 'modinfo.json')
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, 'w', newline='\n') as dest:
        pajson.dump(modinfo, dest, indent=2)

    # remove destination files
    shutil.rmtree(os.path.join(out_dir, 'pa'), ignore_errors=True)

    ## Generate the mod
    sources = load_json(src, '/src/pa/sources.json')
    process_changes(sources, src, out_dir)

    # generate the stratigic icon effects
    print ('==== running strategic icon generator')
    src.mount('/', out_dir)
    process_changes(generate_strat_icons(src), src, out_dir)

    if options.get('debug_mode', False):
        deploy_debug(out_dir, is_titans)
    else:
        restore();
        # optimize_mod(src, out_dir)
        # analyse the mod for missing files
        mod_report = check_mod(out_dir)
        print(mod_report.printReport())


def optimize_mod(loader, out_dir):
    for root, dirs, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_spec = spec.parse_spec(loader, file_path)
                if 'base_spec' in file_spec:
                    base_spec = spec.parse_spec(loader, file_spec['base_spec'])
                    file_spec = spec.prune_spec(file_spec, base_spec)

                    with open(file_path, 'w', newline='\n') as f:
                        pajson.dump(file_spec, f, indent=2)


generate_mod(False)
generate_mod(True)
