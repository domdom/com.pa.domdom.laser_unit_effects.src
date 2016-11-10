import json
import collections
import copy

base_arty_effect_file = 'arty_ammo_hit.pfx'



with open(base_arty_effect_file, 'r', encoding='utf-8') as base_file:
    base_arty_effect = json.load(base_file, object_pairs_hook=collections.OrderedDict)

to_scale = ['sizeX', 'sizeY', 'sizeRangeX', 'sizeRangeY', 'velocity', 'velocityRange', 'offsetX', 'offsetY', 'offsetZ', 'offsetRangeX', 'offsetRangeY', 'offsetRangeZ', 'accelX', 'accelY', 'accelZ', 'gravity', 'snapToSurfaceOffset', ]

for scale in [0.15, 0.2, 0.4, 0.8, 1.6]:
    arty_effect = copy.deepcopy(base_arty_effect)
    for i, emitter in enumerate(arty_effect['emitters']):
        for key in to_scale:
            if key in emitter:
                try:
                    if isinstance(emitter[key], (float, int)):
                        arty_effect['emitters'][i][key] *= scale
                    elif isinstance(emitter[key], list):
                        for j, value in enumerate(emitter[key]):
                            arty_effect['emitters'][i][key][j][1] *= scale
                    elif isinstance(emitter[key], dict):
                        for j, value in enumerate(emitter[key]['keys']):
                            arty_effect['emitters'][i][key]['keys'][j][1] *= scale
                    else:
                        print(key, emitter[key])
                except:
                    print(key, arty_effect['emitters'][i][key])
                    raise
    # print(json.dumps(arty_effect))
    with open('arty_ammo_hit_scale_' + str(scale) + '.pfx', 'w') as out:
        json.dump(arty_effect, out, indent=2)

