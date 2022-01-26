# ba_meta require api 6
import ba, _ba

package_name = 'godzilla'

package_files = {
    "godzillaForeArm.bob": {
        "md5": "f7ac9b52bb8eac6f65aa5ede7b396458",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaForeArm.bob",
        "target": "ba_data/models/godzillaForeArm.bob"
    },
    "godzillaHead.bob": {
        "md5": "bf7e11e588b6f2808f53c2079ff46fa7",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaHead.bob",
        "target": "ba_data/models/godzillaHead.bob"
    },
    "godzillaColorMask.dds": {
        "md5": "6ba0cc3e67e91bcf7fc84ac51e552115",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaColorMask.dds",
        "target": "ba_data/textures/godzillaColorMask.dds"
    },
    "godzillaUpperArm.bob": {
        "md5": "8bf420d8ee0b8e2f46600e5b9dcd2fda",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaUpperArm.bob",
        "target": "ba_data/models/godzillaUpperArm.bob"
    },
    "godzillaUpperLeg.bob": {
        "md5": "b1b2f08ff4621998777eefa70a67a0e3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaUpperLeg.bob",
        "target": "ba_data/models/godzillaUpperLeg.bob"
    },
    "godzillaToes.bob": {
        "md5": "84971b258f9bbd9d2415b136e3ede530",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaToes.bob",
        "target": "ba_data/models/godzillaToes.bob"
    },
    "godzillaColor.dds": {
        "md5": "153de938707d7e8ba6569541b903128e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaColor.dds",
        "target": "ba_data/textures/godzillaColor.dds"
    },
    "godzillaColor.ktx": {
        "md5": "1b535588d4382dcc32ceda69d583275d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaColor.ktx",
        "target": "ba_data/textures/godzillaColor.ktx"
    },
    "godzillaTorso.bob": {
        "md5": "cc07ddf9a61fa047c0e51643e3c972d5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaTorso.bob",
        "target": "ba_data/models/godzillaTorso.bob"
    },
    "godzillaColorMask.ktx": {
        "md5": "ef830579c110b1dad8aefe1e3eda8a6f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaColorMask.ktx",
        "target": "ba_data/textures/godzillaColorMask.ktx"
    },
    "godzillaIconColorMask.dds": {
        "md5": "5fca21dc5abf6997212da5efb940d283",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaIconColorMask.dds",
        "target": "ba_data/textures/godzillaIconColorMask.dds"
    },
    "godzillaLowerLeg.bob": {
        "md5": "c1b90a29abc7397b09b25be608c1aa43",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaLowerLeg.bob",
        "target": "ba_data/models/godzillaLowerLeg.bob"
    },
    "godzillaHand.bob": {
        "md5": "cdb84e3a0af3137776133c23410bb397",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaHand.bob",
        "target": "ba_data/models/godzillaHand.bob"
    },
    "godzillaIconColorMask.ktx": {
        "md5": "350b2a5d633cb052df8d0099cf5b0653",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaIconColorMask.ktx",
        "target": "ba_data/textures/godzillaIconColorMask.ktx"
    },
    "godzillaIconColor.dds": {
        "md5": "bc7e4e221d03c950efb30a6323df8caf",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaIconColor.dds",
        "target": "ba_data/textures/godzillaIconColor.dds"
    },
    "godzillaIconColor.ktx": {
        "md5": "a4f1921fc8f2d02808830d19e69e3cb1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/godzillaIconColor.ktx",
        "target": "ba_data/textures/godzillaIconColor.ktx"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/godzilla/none.bob",
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
        
        # Godzilla #####################################
        t         = Appearance('Godzilla')
        t.color_texture      = 'godzillaColor'
        t.color_mask_texture = 'godzillaIconColorMask'
        t.icon_texture       = 'godzillaIconColor'
        t.icon_mask_texture  = 'godzillaIconColorMask'
        t.head_model         = 'godzillaHead'
        t.torso_model        = 'godzillaTorso'
        t.pelvis_model       = 'none'
        t.upper_arm_model    = 'godzillaUpperArm'
        t.forearm_model      = 'godzillaForeArm'
        t.hand_model         = 'godzillaHand'
        t.upper_leg_model    = 'godzillaUpperLeg'
        t.lower_leg_model    = 'godzillaLowerLeg'
        t.toes_model         = 'godzillaToes'
        bear_sounds          = ['bear1', 'bear2', 'bear3', 'bear4']
        bear_hit_sounds      = ['bearHit1', 'bearHit2']
        t.attack_sounds      = bear_sounds
        t.jump_sounds        = bear_sounds
        t.impact_sounds      = bear_hit_sounds
        t.death_sounds       = ['bearDeath']
        t.pickup_sounds      = bear_sounds
        t.fall_sounds        = ['bearFall']
        t.style              = 'bones'
