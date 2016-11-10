import json
import sys
import math
import copy

import loader

red = 1
green = 0.5
blue = 0

true = True
false = False


base_trail = loader.loads("""{
  "emitters": [
    {
      "spec": {
        "shader": "particle_add",
        "red": 6,
        "green": 1,
        "blue": 0.2,
        "alpha" : 6,
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 1,
      "emissionBurts": 1,
      "lifetime": 127,
      "maxParticles": 1,
      "killOnDeactivate": true,
      "endDistance": 1400
    },
    {
      "spec": {
        "shader": "particle_add",
        "red": 6,
        "green": 1,
        "blue": 0.2,
        "alpha" : 6,
        "cameraPush": 0.6,
        "baseTexture": "/pa/effects/textures/particles/dot.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 0.6,
      "emissionBurts": 1,
      "lifetime": 127,
      "maxParticles": 1,
      "killOnDeactivate": true,
      "endDistance": 1400
    },
    {
      "spec": {
        "shader": "particle_transparent",
        "shape" : "string",
        "red": 6,
        "green": 0.8,
        "blue": 0.1,
        "size" : [[0, 1], [0.9, 0]],
        "alpha": 1,
        "baseTexture": "/pa/effects/textures/particles/flat.papa",
        "dataChannelFormat": "PositionColorAndAlignVector"
      },
      "sizeX": 0.1,
      "emissionBurts": 1,
      "lifetime": 0.4,
      "emitterLifetime" : 1,
      "killOnDeactivate": true,
      "useWorldSpace": true,
      "endDistance": 2000
    },
    {
      "spec": {
        "shader": "particle_transparent_lit",
        "shape" : "string",
        "red": 6,
        "green": 1,
        "blue": 0.1,
        "size" : [[0, 1], [0.9, 0]],
        "alpha": 0.2,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "dataChannelFormat": "PositionColorAndAlignVector"
      },
      "sizeX": 0.5,
      "emissionBurts": 1,
      "lifetime": 0.4,
      "offsetRangeX": 0.2,
      "offsetRangeZ": 0.2,
      "emitterLifetime" : 1,
      "useWorldSpace": true,
      "endDistance": 2000
    },
    {
      "spec": {
        "shader": "particle_transparent_lit",
        "shape" : "string",
        "red": 6,
        "green": 1,
        "blue": 0.1,
        "size" : [[0, 1], [0.9, 0]],
        "alpha": 0.2,
        "baseTexture": "/pa/effects/textures/particles/flat.papa",
        "dataChannelFormat": "PositionColorAndAlignVector"
      },
      "sizeX": 0.3,
      "lifetime": 0.4,
      "emitterLifetime" : 1,
      "useWorldSpace": true,
      "endDistance": 2000
    }
  ]
}""")


base_trail['emitters'][2]['offsetRangeX'] = 0.4
base_trail['emitters'][2]['offsetRangeZ'] = 0.4

base_trail['emitters'].append(copy.deepcopy(base_trail['emitters'][2]))

# del base_trail['emitters'][2]


base_hit = loader.loads("""{
  "emitters": [
      {
      "spec": {
        "shader": "particle_clip",
        "size": [[0, 0 ], [0.15, 0.5 ], [0.5, 0.75 ], [1, 1.2 ] ],
        "red":   [[0.0, 6.0 ], [1.0, 4.0 ] ],
        "green": [[0.125, 2 ], [0.5, 1 ] ],
        "blue":  [[0.0, 0.25 ], [0.25, 0.25 ] ],
        "alpha": [[0.0, 0.6 ], [1.0, 0.0 ] ],
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/fire_puff.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 14,
      "emissionBursts": 1,
      "rotationRange": 3.15,
      "rotationRateRange": 0.25,
      "lifetime": 0.4,
      "emitterLifetime": 1.0,
      "bLoop": false
    },
    {
      "spec": {
        "shader": "particle_add",
        "size": [[0, 0 ], [0.5, 0.5 ], [1, 0] ],
        "red":   [[0.0, 6.0 ], [1.0, 4.0 ] ],
        "green": [[0.125, 1.8 ], [0.5, 1.0 ] ],
        "blue":  [[0.0, 0.25 ], [0.25, 0.25 ] ],
        "alpha": [[0.0, 0.5 ], [1.0, 0.0 ] ],
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/dot.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 15,
      "emissionBursts": 1,
      "rotationRange": 3.15,
      "rotationRateRange": 0.25,
      "lifetime": 0.4,
      "emitterLifetime": 1.0,
      "bLoop": false
    },
    {
      "spec": {
        "shader": "particle_transparent",
        "facing": "Velocity",
        "size": [[0, 0 ], [0.2, 1 ], [1, 0 ]],
        "red": 2.1,
        "green": 0.5,
        "blue": 0.1,
        "temp_alpha": [[0, 1 ], [1, 0 ] ],
        "baseTexture": "/pa/effects/textures/particles/dot.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionColorAndAlignVector"
      },
      "type": "SHELL",
      "offsetRangeX": 3,
      "offsetRangeY": 3,
      "offsetRangeZ": 3,
      "offsetAllowNegZ": true,
      "velocityZ": 0.0,
      "velocity": 70,
      "velocityRange": 20.0,
      "useRadialVelocityDir": true,
      "sizeX": 0.7,
      "sizeY": 10,
      "sizeRangeY": 1,
      "emissionBursts": 9,
      "lifetime": 0.27,
      "lifetimeRange": 0.05,
      "emitterLifetime": 0.1,
      "bLoop": false,
      "endDistance": 850
    },
    {
      "spec": {
        "shader": "particle_add",
        "facing": "EmitterZ",
        "size": [[0, 0 ], [0.2, 0.667 ], [0.4, 0.889 ], [0.6, 0.963 ], [0.8, 0.98 ], [1, 1 ] ],
        "red": 0.5,
        "green": 0.35,
        "blue": 2.0,
        "alpha": [[0.2, 1 ], [0.3, 0.5 ], [0.6, 0.25 ], [1, 0 ] ],
        "baseTexture": "/pa/effects/textures/particles/simpleExplosionRing.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "offsetZ": 1,
      "sizeX": 30,
      "emissionBursts": 1,
      "rotationRange": 3.1415,
      "lifetime": 0.25,
      "emitterLifetime": 1,
      "bLoop": false
    },
    {
      "spec": {
        "shader": "particle_add",
        "size": [[0, 0.5 ], [0.2, 1 ], [1, 0 ]],
        "red": 1,
        "green": 0.5,
        "blue": 0.1,
        "alpha": [[0, 2 ], [1, 0 ] ],
        "cameraPush": 1,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 8,
      "emissionBursts": 1,
      "lifetime": 0.4,
      "emitterLifetime": 0.1,
      "bLoop": false,
      "endDistance": 850
    },
    {
      "spec": {
        "shape": "pointlight",
        "red": 6,
        "green": 1,
        "blue": 0.1,
        "alpha": [[0, 3 ], [0.25, 1 ], [1, 0 ] ]
      },
      "sizeX": 25,
      "emissionBursts": 1,
      "lifetime": 0.4,
      "emitterLifetime": 0.5,
      "bLoop": false,
      "endDistance": 850
    }
  ]
}""")

def run():
    loader.dump_effect(base_trail, "grenadier_ammo_trail.pfx")
    loader.dump_effect(base_hit, "grenadier_ammo_hit.pfx")


