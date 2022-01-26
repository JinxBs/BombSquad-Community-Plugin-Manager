# ba_meta require api 6
import ba, _ba

package_name = 'boris'

package_files = {
    "borisColor.ktx": {
        "md5": "ebbcb6e44cf22d873389eff30991deee",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisColor.ktx",
        "target": "ba_data/textures/borisColor.ktx"
    },
    "borisIconColor.ktx": {
        "md5": "e35b32339b5af1d38472b0ebad2e8b71",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisIconColor.ktx",
        "target": "ba_data/textures/borisIconColor.ktx"
    },
    "borisLowerLeg.bob": {
        "md5": "436dd9de4272d53ad5b24148611b8bcc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisLowerLeg.bob",
        "target": "ba_data/models/borisLowerLeg.bob"
    },
    "borisUpperLeg.bob": {
        "md5": "13c28c5b13df9864430900e3a924ff49",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisUpperLeg.bob",
        "target": "ba_data/models/borisUpperLeg.bob"
    },
    "borisTorso.bob": {
        "md5": "06a04cf185f2158ebed041e0effcc38e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisTorso.bob",
        "target": "ba_data/models/borisTorso.bob"
    },
    "borisColor.dds": {
        "md5": "898c63e35565c4e2d8c33e05fe11efc7",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisColor.dds",
        "target": "ba_data/textures/borisColor.dds"
    },
    "borisToes.bob": {
        "md5": "01b490f99755996e96bcae2a61f6e638",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisToes.bob",
        "target": "ba_data/models/borisToes.bob"
    },
    "borisIconColor.dds": {
        "md5": "0c91affbfaad181c142f2b111d6cea78",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisIconColor.dds",
        "target": "ba_data/textures/borisIconColor.dds"
    },
    "borisHand.bob": {
        "md5": "96f0d43c31a48a619b50bc5dab36f2cc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisHand.bob",
        "target": "ba_data/models/borisHand.bob"
    },
    "borisForeArm.bob": {
        "md5": "3fad2bae8f8d6f7a874054558f6f4b25",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisForeArm.bob",
        "target": "ba_data/models/borisForeArm.bob"
    },
    "borisHead.bob": {
        "md5": "e65f2bac13baec7ba5786b499780855d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisHead.bob",
        "target": "ba_data/models/borisHead.bob"
    },
    "borisUpperArm.bob": {
        "md5": "dba285affa767a41e5275879e02863d6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/borisUpperArm.bob",
        "target": "ba_data/models/borisUpperArm.bob"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/boris/none.bob",
        "target": "ba_data/models/none.bob"
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
        # Boris #####################################
        t = Appearance('Boris')
        t.color_texture = 'borisColor'
        t.color_mask_texture = 'black'
        t.default_color = (0.4, 0.5, 0.4)
        t.default_highlight = (1, 0.5, 0.3)
        t.icon_texture = 'borisIconColor'
        t.icon_mask_texture = 'black'
        t.head_model = 'borisHead'
        t.torso_model = 'borisTorso'
        t.pelvis_model = 'none'
        t.upper_arm_model = 'borisUpperArm'
        t.forearm_model = 'borisForeArm'
        t.hand_model = 'borisHand'
        t.upper_leg_model = 'borisUpperLeg'
        t.lower_leg_model = 'borisLowerLeg'
        t.toes_model = 'borisToes'
        agent_sounds = ['agent1', 'agent2', 'agent3', 'agent4']
        agent_hit_sounds = ['agentHit1', 'agentHit2']
        t.attack_sounds = agent_sounds
        t.jump_sounds = agent_sounds
        t.impact_sounds = agent_hit_sounds
        t.death_sounds = ['agentDeath']
        t.pickup_sounds = agent_sounds
        t.fall_sounds = ['agentFall']
        t.style = 'agent'
