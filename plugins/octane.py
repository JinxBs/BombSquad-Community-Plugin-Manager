# ba_meta require api 6
import ba, _ba

package_name = 'octane'

package_files = {
    "octaneColor.dds": {
        "md5": "512dff4d3cfac320e819072c96e8ede4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneColor.dds",
        "target": "ba_data/textures/octaneColor.dds"
    },
    "octaneHead.bob": {
        "md5": "47da6841cf38e13003731e417935f6e4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneHead.bob",
        "target": "ba_data/models/octaneHead.bob"
    },
    "octaneUpperLeg.bob": {
        "md5": "139a8dd2e5ece77cfec81e85893369e7",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneUpperLeg.bob",
        "target": "ba_data/models/octaneUpperLeg.bob"
    },
    "octaneHand.bob": {
        "md5": "e18d49ac2aee11b1690f54056c8474d4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneHand.bob",
        "target": "ba_data/models/octaneHand.bob"
    },
    "octaneIconColor.dds": {
        "md5": "073dad30161d56729d8058add0c33f1b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneIconColor.dds",
        "target": "ba_data/textures/octaneIconColor.dds"
    },
    "octaneColorMask.dds": {
        "md5": "2a04c16a9ef638f94ea5e59e3c27d478",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneColorMask.dds",
        "target": "ba_data/textures/octaneColorMask.dds"
    },
    "octaneIconColorMask.ktx": {
        "md5": "5f95f902b21a02a75d11e9992fcde9b7",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneIconColorMask.ktx",
        "target": "ba_data/textures/octaneIconColorMask.ktx"
    },
    "octaneUpperArm.bob": {
        "md5": "64beffb9abd6edf0193ff67f94c9232a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneUpperArm.bob",
        "target": "ba_data/models/octaneUpperArm.bob"
    },
    "octaneIconColor.ktx": {
        "md5": "5ea28861d0f0a2a426c105072ddcaa48",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneIconColor.ktx",
        "target": "ba_data/textures/octaneIconColor.ktx"
    },
    "octaneColorMask.ktx": {
        "md5": "e34c4115fe71e42159384a0c2ba6df4a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneColorMask.ktx",
        "target": "ba_data/textures/octaneColorMask.ktx"
    },
    "octaneLowerLeg.bob": {
        "md5": "4853401eff9e582f333f7d327eb5f47c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneLowerLeg.bob",
        "target": "ba_data/models/octaneLowerLeg.bob"
    },
    "octaneTorso.bob": {
        "md5": "95de816f7664d3c9b23992b842abda01",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneTorso.bob",
        "target": "ba_data/models/octaneTorso.bob"
    },
    "octaneIconColorMask.dds": {
        "md5": "2c5e883eb239d4e283996831984656a5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneIconColorMask.dds",
        "target": "ba_data/textures/octaneIconColorMask.dds"
    },
    "octaneColor.ktx": {
        "md5": "636c976ba0a488a08f3deea42f502c50",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneColor.ktx",
        "target": "ba_data/textures/octaneColor.ktx"
    },
    "octaneForeArm.bob": {
        "md5": "c6487e6a90c4be500da09e9b92148d5e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/octaneForeArm.bob",
        "target": "ba_data/models/octaneForeArm.bob"
    },
    "none.bob": {
        "md5": "2aa40a15f2bd71892923f01cc6d35585",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Characters/octane/none.bob",
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
        
        # Octane #####################################
        t         = Appearance('Octane')
        t.color_texture      = 'octaneColor'
        t.color_mask_texture = 'octaneIconColorMask'
        t.icon_texture       = 'octaneIconColor'
        t.icon_mask_texture  = 'octaneIconColorMask'
        t.head_model         = 'octaneHead'
        t.torso_model        = 'octaneTorso'
        t.pelvis_model       = 'none'
        t.upper_arm_model    = 'octaneUpperArm'
        t.forearm_model      = 'octaneForeArm'
        t.hand_model         = 'octaneHand'
        t.upper_leg_model    = 'octaneUpperLeg'
        t.lower_leg_model    = 'octaneLowerLeg'
        t.toes_model         = 'none'
        agent_sounds         = ['agent1', 'agent2', 'agent3', 'agent4']
        agent_hit_sounds     = ['agentHit1', 'agentHit2']
        t.attack_sounds      = agent_sounds
        t.jump_sounds        = agent_sounds
        t.impact_sounds      = agent_hit_sounds
        t.death_sounds       = ['agentDeath']
        t.pickup_sounds      = agent_sounds
        t.fall_sounds        = ['agentFall']
        t.style              = 'agent'
