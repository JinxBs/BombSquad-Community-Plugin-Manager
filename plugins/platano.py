# ba_meta require api 6
import ba, _ba

package_name = 'platano'

package_files = {
    "platanoLowerLeg.bob": {
        "md5": "fb858538c6428d820707881039b3c0e1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoLowerLeg.bob",
        "target": "ba_data/models/platanoLowerLeg.bob"
    },
    "platanoIconColor.ktx": {
        "md5": "367a23849ac0cda43546ec33b516d46a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoIconColor.ktx",
        "target": "ba_data/textures/platanoIconColor.ktx"
    },
    "platanoToes.bob": {
        "md5": "9e2247ed0209ace7d2c73774e18aa13c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoToes.bob",
        "target": "ba_data/models/platanoToes.bob"
    },
    "platanoHand.bob": {
        "md5": "5cabdf4b45648b2513ccb96fd608bbb6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoHand.bob",
        "target": "ba_data/models/platanoHand.bob"
    },
    "platanoIconColorMask.ktx": {
        "md5": "7dd3e708df4a6d9e2a428e81f8eeacf8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoIconColorMask.ktx",
        "target": "ba_data/textures/platanoIconColorMask.ktx"
    },
    "platanoTorso.bob": {
        "md5": "e332b298645f759f6764bc3d2e3146b5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoTorso.bob",
        "target": "ba_data/models/platanoTorso.bob"
    },
    "platanoColor.ktx": {
        "md5": "58a096015a88be3c6d0f90694788c946",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoColor.ktx",
        "target": "ba_data/textures/platanoColor.ktx"
    },
    "platanoColor.dds": {
        "md5": "fd4a7e23399537a2fb935ba11b278977",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoColor.dds",
        "target": "ba_data/textures/platanoColor.dds"
    },
    "platanoIconColor.dds": {
        "md5": "7e0ae6909ba49c3f7ba25ccf62a6cd7b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoIconColor.dds",
        "target": "ba_data/textures/platanoIconColor.dds"
    },
    "platanoUpperArm.bob": {
        "md5": "24bbb5e0e31d97af692d73264cd5a4b5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoUpperArm.bob",
        "target": "ba_data/models/platanoUpperArm.bob"
    },
    "platanoForeArm.bob": {
        "md5": "b0e46523ec73681e85ceb539a3b77a01",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoForeArm.bob",
        "target": "ba_data/models/platanoForeArm.bob"
    },
    "platanoUpperLeg.bob": {
        "md5": "f0845c13d067202fd034dc0f438a0adf",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoUpperLeg.bob",
        "target": "ba_data/models/platanoUpperLeg.bob"
    },
    "platanoIconColorMask.dds": {
        "md5": "ee151a14fd23dd1c7a09a6840676dcfc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/platanoIconColorMask.dds",
        "target": "ba_data/textures/platanoIconColorMask.dds"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/platano/none.bob",
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
        # Platano #####################################
        t         = Appearance('Platano')
        t.color_texture      = 'platanoColor'
        t.color_mask_texture = 'platanoIconColorMask'
        t.default_color      = (0.4, 0.5, 0.4)
        t.default_highlight  = (1, 0.5, 0.3)
        t.icon_texture       = 'platanoIconColor'
        t.icon_mask_texture  = 'platanoIconColorMask'
        t.head_model         = 'none'
        t.torso_model        = 'platanoTorso'
        t.pelvis_model       = 'none'
        t.upper_arm_model    = 'platanoUpperArm'
        t.forearm_model      = 'platanoForeArm'
        t.hand_model         = 'platanoHand'
        t.upper_leg_model    = 'platanoUpperLeg'
        t.lower_leg_model    = 'platanoLowerLeg'
        t.toes_model         = 'platanoToes'
        mel_sounds = [
            'mel01', 'mel02', 'mel03', 'mel04', 'mel05', 'mel06', 'mel07', 'mel08',
            'mel09', 'mel10'
        ]
        t.attack_sounds = mel_sounds
        t.jump_sounds = mel_sounds
        t.impact_sounds = mel_sounds
        t.death_sounds = ['melDeath01']
        t.pickup_sounds = mel_sounds
        t.fall_sounds = ['melFall01']
        t.style              = 'agent'
