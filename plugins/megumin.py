# ba_meta require api 6
import ba, _ba

package_name = 'megumin'

package_files = {
    "meguminForeArm.bob": {
        "md5": "8fc56eb3ba0829d0ba571b8dcf9219a3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminForeArm.bob",
        "target": "ba_data/models/meguminForeArm.bob"
    },
    "meguminHead.bob": {
        "md5": "2df37135cd902fae16923789c4473150",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminHead.bob",
        "target": "ba_data/models/meguminHead.bob"
    },
    "meguminUpperLeg.bob": {
        "md5": "6d2521bfa0bfb4140c07bc8342202a5a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminUpperLeg.bob",
        "target": "ba_data/models/meguminUpperLeg.bob"
    },
    "meguminUpperArm.bob": {
        "md5": "4e675cce6c175cfcadfd6502b8c5ff43",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminUpperArm.bob",
        "target": "ba_data/models/meguminUpperArm.bob"
    },
    "meguminColor.dds": {
        "md5": "b7766ec7a313001001830eab7ccf950a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminColor.dds",
        "target": "ba_data/textures/meguminColor.dds"
    },
    "meguminIconColor.ktx": {
        "md5": "da06baba5bbc1655386efdaa9d21d805",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminIconColor.ktx",
        "target": "ba_data/textures/meguminIconColor.ktx"
    },
    "meguminTorso.bob": {
        "md5": "c4690c75eceeedee339cd81d8dd44c7e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminTorso.bob",
        "target": "ba_data/models/meguminTorso.bob"
    },
    "meguminColorMask.dds": {
        "md5": "af08d4f9635de0288bc24caffb11a072",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminColorMask.dds",
        "target": "ba_data/textures/meguminColorMask.dds"
    },
    "meguminIconColor.dds": {
        "md5": "3f971d76eee1b5eba1e2e0084d1f8a8f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminIconColor.dds",
        "target": "ba_data/textures/meguminIconColor.dds"
    },
    "meguminColor.ktx": {
        "md5": "e2ac0f537feb40650707425e452b1de8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminColor.ktx",
        "target": "ba_data/textures/meguminColor.ktx"
    },
    "meguminIconColorMask.ktx": {
        "md5": "375a6c76a2f2181d1fb6e8673e6c12ba",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminIconColorMask.ktx",
        "target": "ba_data/textures/meguminIconColorMask.ktx"
    },
    "meguminColorMask.ktx": {
        "md5": "eae9e0d64c953c6c043bec8b764df97f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminColorMask.ktx",
        "target": "ba_data/textures/meguminColorMask.ktx"
    },
    "meguminLowerLeg.bob": {
        "md5": "379fefae3c52f937004d01844ade7ed2",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminLowerLeg.bob",
        "target": "ba_data/models/meguminLowerLeg.bob"
    },
    "meguminHand.bob": {
        "md5": "bc408cb97bc2c57f9159b074e41385c5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminHand.bob",
        "target": "ba_data/models/meguminHand.bob"
    },
    "meguminIconColorMask.dds": {
        "md5": "4df36a931dbc38a98d8e047482c17282",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminIconColorMask.dds",
        "target": "ba_data/textures/meguminIconColorMask.dds"
    },
    "meguminToes.bob": {
        "md5": "a0fd8eb96b3b57a64083fa80275a7249",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/meguminToes.bob",
        "target": "ba_data/models/meguminToes.bob"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/megumin/none.bob",
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
        
        # Megumin #####################################
        t         = Appearance('Megumin')
        t.color_texture      = 'meguminColor'
        t.color_mask_texture = 'meguminColorMask'
        t.default_color      = (0.4, 0.5, 0.4)
        t.default_highlight  = (1, 0.5, 0.3)
        t.icon_texture       = 'meguminIconColor'
        t.icon_mask_texture  = 'meguminIconColorMask'
        t.head_model         = 'meguminHead'
        t.torso_model        = 'meguminTorso'
        t.pelvis_model       = 'none'
        t.upper_arm_model    = 'meguminUpperArm'
        t.forearm_model      = 'meguminForeArm'
        t.hand_model         = 'meguminHand'
        t.upper_leg_model    = 'meguminUpperLeg'
        t.lower_leg_model    = 'meguminLowerLeg'
        t.toes_model         = 'meguminToes'
        sounds               = ['pixie1', 'pixie2', 'pixie3', 'pixie4']
        soundsHit            = ['pixieHit1', 'pixieHit2']
        t.attack_sounds      = sounds
        t.jump_sounds        = sounds
        t.impact_sounds      = soundsHit
        t.death_sounds       = ["pixieDeath"]
        t.pickup_sounds      = sounds
        t.fall_sounds        = ["pixieFall"]
        t.style              = 'agent'
