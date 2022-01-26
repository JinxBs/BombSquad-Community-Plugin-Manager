# ba_meta require api 6
import ba, _ba

package_name = 'henryStickmin'

package_files = {
    "henryStickminUpperArm.bob": {
        "md5": "6354669b2458de1eb4841e104523ae15",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminUpperArm.bob",
        "target": "ba_data/models/henryStickminUpperArm.bob"
    },
    "henryStickminLowerLeg.bob": {
        "md5": "a60241e2cf26077de9882bda34fec3a4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminLowerLeg.bob",
        "target": "ba_data/models/henryStickminLowerLeg.bob"
    },
    "henryStickminColorMask.ktx": {
        "md5": "7df4c68fb0ed3fc1c317d2f62312987a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminColorMask.ktx",
        "target": "ba_data/textures/henryStickminColorMask.ktx"
    },
    "henryStickminToes.bob": {
        "md5": "641b14277beb6a099b2cbce112943f02",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminToes.bob",
        "target": "ba_data/models/henryStickminToes.bob"
    },
    "henryStickminHand.bob": {
        "md5": "01bcee44bd927e4c289b6061d7b80837",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminHand.bob",
        "target": "ba_data/models/henryStickminHand.bob"
    },
    "henryStickminIconColor.ktx": {
        "md5": "deb0e2a821dca2730a793736caf8bebe",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminIconColor.ktx",
        "target": "ba_data/textures/henryStickminIconColor.ktx"
    },
    "henryStickminColorMask.dds": {
        "md5": "b03207af4065d7ccdc927e93b2602ef8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminColorMask.dds",
        "target": "ba_data/textures/henryStickminColorMask.dds"
    },
    "henryStickminIconColor.dds": {
        "md5": "6999a707e328757ce9c3a9bc6a0c5420",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminIconColor.dds",
        "target": "ba_data/textures/henryStickminIconColor.dds"
    },
    "henryStickminUpperLeg.bob": {
        "md5": "d710a079a453b7595422e84b9eb073c3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminUpperLeg.bob",
        "target": "ba_data/models/henryStickminUpperLeg.bob"
    },
    "henryStickminHead.bob": {
        "md5": "d04fd08005620824c551e5be16740e41",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminHead.bob",
        "target": "ba_data/models/henryStickminHead.bob"
    },
    "henryStickminColor.dds": {
        "md5": "7554ade12a891b1a2e85abf830ed42e4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminColor.dds",
        "target": "ba_data/textures/henryStickminColor.dds"
    },
    "henryStickminTorso.bob": {
        "md5": "b52626d23827b3c39b91ccff2d23f83d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminTorso.bob",
        "target": "ba_data/models/henryStickminTorso.bob"
    },
    "henryStickminColor.ktx": {
        "md5": "c55f34b3851674a7c4f54b3e4b3c9d5a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminColor.ktx",
        "target": "ba_data/textures/henryStickminColor.ktx"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/none.bob",
        "target": "ba_data/models/none.bob"
    },
    "henryStickminForeArm.bob": {
        "md5": "d1902e05c0614f4a218e57092e9cfbf7",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/henryStickmin/henryStickminForeArm.bob",
        "target": "ba_data/models/henryStickminForeArm.bob"
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
        # Henry Stickmin #####################################
        t = Appearance('Henry Stickmin')
        t.color_texture = 'henryStickminColor'
        t.color_mask_texture = 'henryStickminColorMask'
        t.default_color = (0.4, 0.5, 0.4)
        t.default_highlight = (1, 0.5, 0.3)
        t.icon_texture = 'henryStickminIconColor'
        t.icon_mask_texture = 'black'
        t.head_model = 'henryStickminHead'
        t.torso_model = 'henryStickminTorso'
        t.pelvis_model = 'none'
        t.upper_arm_model = 'henryStickminUpperArm'
        t.forearm_model = 'henryStickminForeArm'
        t.hand_model = 'henryStickminHand'
        t.upper_leg_model = 'henryStickminUpperLeg'
        t.lower_leg_model = 'henryStickminLowerLeg'
        t.toes_model = 'henryStickminToes'
        sound = ["blank"]
        t.jump_sounds = sound
        t.attack_sounds = sound
        t.impact_sounds = sound
        t.death_sounds = sound
        t.pickup_sounds = sound
        t.fall_sounds = sound
        t.style = 'bones'

