# ba_meta require api 6
import ba, _ba

package_name = 'maxSteel'

package_files = {
    "maxSteelIconColorMask.dds": {
        "md5": "003dab654ecc4317b7250c44e24c15b8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelIconColorMask.dds",
        "target": "ba_data/textures/maxSteelIconColorMask.dds"
    },
    "maxSteelColor.ktx": {
        "md5": "314473698ada4d5aec6d161f0639ac24",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelColor.ktx",
        "target": "ba_data/textures/maxSteelColor.ktx"
    },
    "maxSteelColorMask.ktx": {
        "md5": "536ae1289761566bca2fc88d9e8a6f57",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelColorMask.ktx",
        "target": "ba_data/textures/maxSteelColorMask.ktx"
    },
    "maxSteelColorMask.dds": {
        "md5": "431cbcab08c4eb9f8a89252eab91007d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelColorMask.dds",
        "target": "ba_data/textures/maxSteelColorMask.dds"
    },
    "maxSteelIconColorMask.ktx": {
        "md5": "19162dc83d6468e28a44f81153a00451",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelIconColorMask.ktx",
        "target": "ba_data/textures/maxSteelIconColorMask.ktx"
    },
    "maxSteelIconColor.dds": {
        "md5": "869ab19e0c8d2973ca31587958bdd467",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelIconColor.dds",
        "target": "ba_data/textures/maxSteelIconColor.dds"
    },
    "maxSteelUpperArm.bob": {
        "md5": "42df27fa2d42188aec12d7becdb548ca",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelUpperArm.bob",
        "target": "ba_data/models/maxSteelUpperArm.bob"
    },
    "maxSteelHand.bob": {
        "md5": "53d14e1db151e35d2b5466eae056e16c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelHand.bob",
        "target": "ba_data/models/maxSteelHand.bob"
    },
    "maxSteelIconColor.ktx": {
        "md5": "b10a532091e125b69e25149e91b5b79e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelIconColor.ktx",
        "target": "ba_data/textures/maxSteelIconColor.ktx"
    },
    "maxSteelUpperLeg.bob": {
        "md5": "99149cd010d62beb81d50785beca5460",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelUpperLeg.bob",
        "target": "ba_data/models/maxSteelUpperLeg.bob"
    },
    "maxSteelForeArm.bob": {
        "md5": "cd87107ae60bca15997c1b94fe654498",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelForeArm.bob",
        "target": "ba_data/models/maxSteelForeArm.bob"
    },
    "maxSteelColor.dds": {
        "md5": "6e443cecedb22503c5f6b15adc9c75a5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelColor.dds",
        "target": "ba_data/textures/maxSteelColor.dds"
    },
    "maxSteelHead.bob": {
        "md5": "d9e42290e20416446e4001b98fb216f8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelHead.bob",
        "target": "ba_data/models/maxSteelHead.bob"
    },
    "maxSteelLowerLeg.bob": {
        "md5": "a8dfb0120cfc04d896c2604c530ef50d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelLowerLeg.bob",
        "target": "ba_data/models/maxSteelLowerLeg.bob"
    },
    "maxSteelTorso.bob": {
        "md5": "924d64372c3027fc5c66f75a46c57279",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelTorso.bob",
        "target": "ba_data/models/maxSteelTorso.bob"
    },
    "maxSteelToes.bob": {
        "md5": "039ef6f74a0d125b0a500dd4a666d7b3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/maxSteelToes.bob",
        "target": "ba_data/models/maxSteelToes.bob"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/maxSteel/none.bob",
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
        
        # Max Steel #####################################
        t         = Appearance('Max Steel')
        t.color_texture      = 'maxSteelColor'
        t.color_mask_texture = 'maxSteelColorMask'
        t.icon_texture       = 'maxSteelIconColor'
        t.icon_mask_texture  = 'maxSteelIconColorMask'
        t.head_model         = 'maxSteelHead'
        t.torso_model        = 'maxSteelTorso'
        t.pelvis_model       = 'none'
        t.upper_arm_model    = 'maxSteelUpperArm'
        t.forearm_model      = 'maxSteelForeArm'
        t.hand_model         = 'maxSteelHand'
        t.upper_leg_model    = 'maxSteelUpperLeg'
        t.lower_leg_model    = 'maxSteelLowerLeg'
        t.toes_model         = 'maxSteelToes'
        cyborg_sounds        = ['cyborg1', 'cyborg2', 'cyborg3', 'cyborg4']
        cyborg_hit_sounds    = ['cyborgHit1', 'cyborgHit2']
        t.attack_sounds      = cyborg_sounds
        t.jump_sounds        = cyborg_sounds
        t.impact_sounds      = cyborg_hit_sounds
        t.death_sounds       = ['cyborgDeath']
        t.pickup_sounds      = cyborg_sounds
        t.fall_sounds        = ['cyborgFall']
        t.style              = 'bones'
