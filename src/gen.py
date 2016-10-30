#!/usr/bin/env python3
from pa_tools.pa import pafs

# needed for modinfo update
from datetime import datetime
from shutil import copyfile

from pa_tools.pa import pafs
from pa_tools.pa import paths
from pa_tools.pa import pajson


# options, warnings = pajson.loadf('conf.json')
# print ('======= Loading Options =======')
# for w in warnings:
#     print (w)
# print ('debug mode: ', options.get('debug_mode', False))
# print ('pretty printing: ', options.get('pretty_print_effects', True))
# print ('-------------------------------')
# print ('')

print ('PA MEDIA DIR:', paths.PA_MEDIA_DIR)
# create file resolution mappings (handles the mounting of pa_ex1 on pa and fallback etc.)
fs = pafs(paths.PA_MEDIA_DIR)
fs.mount('/pa', '/pa_ex1')
fs.mount('/src', '.')

sources = [
    { "from_file" :   "/src/pa/units/land/ant/ant_patch.json"},
    { "from_file" :   "/src/pa/units/land/inferno/inferno_patch.json"}
]


#     { "from_script" : "/land/commander/commander.py"},

#     { "from_file" :   "/misc/hover_effect_color.pa_patch" },

#     { "from_file" :   "/titans/ares/ares.pa_patch" },

#     { "from_file" :   "/land/drifter/drifter.pa_patch" },

#     { "from_file" :   "/land/leveler/leveler.pa_patch" },
#     { "from_file" :   "/land/sheller/sheller.pa_patch" },

#     { "from_file" :   "/bot/dox/dox2.pa_patch" },
#     { "from_file" :   "/bot/grenadier/grenadier.pa_patch" },
#     { "from_file" :   "/bot/slammer/slammer.pa_patch" },
#     { "from_file" :   "/bot/sniper/sniper.pa_patch" },

#     { "from_file" :   "/air/kestrel/kestrel.pa_patch" },

#     { "from_file" :   "/static/catapult/catapult.pa_patch" },
#     { "from_file" :   "/static/pelter/pelter.pa_patch" },
#     { "from_file" :   "/static/holkins/holkins.pa_patch" },
#     { "from_file" :   "/static/laser/t1.pa_patch" },
#     { "from_file" :   "/static/laser/t2.pa_patch" },
#     { "from_file" :   "/static/laser/t3.pa_patch" },

#     { "from_file" :   "/sea/torpedo/torpedo.pa_patch" },
#     { "from_file" :   "/misc/aa_missile.pa_patch" },
#     { "from_file" :   "/misc/tactical_missile.pa_patch" },

#     { "from_file" :   "/sea/piranha/piranha.pa_patch" },
#     { "from_file" :   "/sea/narwhal/narwhal.pa_patch" },
#     { "from_file" :   "/sea/leviathan/leviathan.pa_patch" },
#     { "from_file" :   "/sea/kraken/kraken.pa_patch" },
#     { "from_file" :   "/sea/kaiju/kaiju.pa_patch" },
#     { "from_file" :   "/sea/orca/orca.pa_patch" }
# ]


def process_changes(changes, loader):
    for change in changes:
        # we have an object, but it is a reference to a file patch to load
        if isinstance(change, dict) and 'from_file' in change:
            from_file = loader.resolveFile(change['from_file'])

            if from_file == None:
                print ("!! ERROR: Not Found '" + change['from_file'] + "'")
                continue

            print('==== loading:', from_file)
            changes, warnings = pajson.loadf(from_file)

            if warnings:
                for warning in warnings: print (warning)

            # make sure our changes are a list
            if isinstance(changes, dict):
                changes = [changes]

            # process new list recursively.
            from os.path import dirname
            loader.mount('/', dirname(from_file))
            process_changes(changes, loader)
            loader.unmount('/')

            continue

        # implicit patch
        if 'patch' not in change:
            change['patch'] = []

        # we have a single target
        if isinstance(change['target'], str):
            target = change['target']
            destination = change.get('destination', target)

            _do_patch(target, change['patch'], destination, loader)

        # list of targets
        if isinstance(change['target'], list):
            for target in change['target']:
                _do_patch(target, change['patch'], target, loader)


def _do_patch(target, patch, destination, loader):
    resolved = loader.resolveFile(target)
    if resolved == None:
        print ("!! ERROR: Not Found '" + target + "'")
        return

    if patch == []:
        print (' copy: ' + resolved)
        return

    print ('patch: ' + resolved)
    obj, warnings = pajson.loadf(resolved)




process_changes(sources, fs)
