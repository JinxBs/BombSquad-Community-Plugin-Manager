# ba_meta require api 6
import ba, _ba

package_name = 'Mike'

package_files = {
    "mikeForeArm.bob": {
        "md5": "e5dabd98868edbf22089e128e62d9fdf",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeForeArm.bob",
        "target": "ba_data/models/mikeForeArm.bob"
    },
    "mikeTorso.bob": {
        "md5": "0be35e2c0e7ae583a9b1690f72fe7166",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeTorso.bob",
        "target": "ba_data/models/mikeTorso.bob"
    },
    "mikeColor.dds": {
        "md5": "846fc8bad9a6b84a43d5d94a064752a6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeColor.dds",
        "target": "ba_data/textures/mikeColor.dds"
    },
    "mikeLowerLeg.bob": {
        "md5": "582563dc1d4f34aedf840428c4302d8f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeLowerLeg.bob",
        "target": "ba_data/models/mikeLowerLeg.bob"
    },
    "mikeUpperLeg.bob": {
        "md5": "5ca2b9900732649bae9ea8008ac08b3a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeUpperLeg.bob",
        "target": "ba_data/models/mikeUpperLeg.bob"
    },
    "mikeHand.bob": {
        "md5": "3d6f461ec07349e29e568048f6f74244",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeHand.bob",
        "target": "ba_data/models/mikeHand.bob"
    },
    "empty.bob": {
        "md5": "e5c115a85ca2415c5ddbb27b543d6bf8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/empty.bob",
        "target": "ba_data/models/empty.bob"
    },
    "mikeIconColor.dds": {
        "md5": "02b5f90ad2a01e7a47d452639c859ebb",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeIconColor.dds",
        "target": "ba_data/textures/mikeIconColor.dds"
    },
    "mikeIconColor.ktx": {
        "md5": "19098795905943427921acf4edc30f31",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeIconColor.ktx",
        "target": "ba_data/textures/mikeIconColor.ktx"
    },
    "mikeUpperArm.bob": {
        "md5": "7529ab90b0839d6f17ff485c2f8748b6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeUpperArm.bob",
        "target": "ba_data/models/mikeUpperArm.bob"
    },
    "mikeColor.ktx": {
        "md5": "d49ebdfb507803bd470e26a326979da6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/Mike/mikeColor.ktx",
        "target": "ba_data/textures/mikeColor.ktx"
    }
}


files_needed = {}
headless_mode = _ba.env()['headless_mode']
for file, value in package_files.items():
    if headless_mode:
        if not file.endswith('.cob'):
            continue
    else:
        if file.endswith('.dds'):
            if  _ba.app.platform == 'android':
                continue
        elif file.endswith('.ktx'):
            if _ba.app.platform != 'android':
                continue
    files_needed[file] = value

from PackInstaller import PackInstaller
PackInstaller(package_name, files_needed)

# ba_meta export plugin
class Character(ba.Plugin):
    def on_app_launch(self):
        from bastd.actor.spazappearance import Appearance
        
        # Meme #####################################
        t         = Appearance('Mike')
        t.color_texture      = 'mikeColor'
        t.color_mask_texture = 'black'
        t.default_color      = (0.4, 0.5, 0.4)
        t.default_highlight  = (1, 0.5, 0.3)
        t.icon_texture       = 'mikeIconColor'
        t.icon_mask_texture  = 'black'
        t.head_model         = 'empty'
        t.torso_model        = 'mikeTorso'
        t.pelvis_model       = 'empty'
        t.upper_arm_model    = 'mikeUpperArm'
        t.forearm_model      = 'mikeForeArm'
        t.hand_model         = 'mikeHand'
        t.upper_leg_model    = 'mikeUpperLeg'
        t.lower_leg_model    = 'mikeLowerLeg'
        t.toes_model         = 'empty'
        sounds               = ['','']
        soundsHit            = ['','']
        t.attack_sounds      = sounds
        t.jump_sounds        = sounds
        t.impact_sounds      = soundsHit
        t.death_sounds       = [""]
        t.pickup_sounds      = sounds
        t.fall_sounds        = [""]
        t.style              = 'agent'
