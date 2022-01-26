from bastd.actor.spazappearance import Appearance

# Samus Aran #####################################
t         = Appearance('Samus Aran')
t.color_texture      = 'samusAranColor'
t.color_mask_texture = 'samusAranColorMask'
t.default_color      = (0.4, 0.5, 0.4)
t.default_highlight  = (1, 0.5, 0.3)
t.icon_texture       = 'samusAranIconColor'
t.icon_mask_texture  = 'samusAranIconColorMask'
t.head_model         = 'samusAranHead'
t.torso_model        = 'samusAranTorso'
t.pelvis_model       = 'none'
t.upper_arm_model    = 'samusAranUpperArm'
t.forearm_model      = 'samusAranForeArm'
t.hand_model         = 'samusAranHand'
t.upper_leg_model    = 'samusAranUpperLeg'
t.lower_leg_model    = 'samusAranLowerLeg'
t.toes_model         = 'samusAranToes'
sounds               = ['samusAran', 'samusAran2',
                        'samusAran3', 'samusAran4']
t.attack_sounds      = sounds
t.jump_sounds        = ["samusAranJump"]
#t.impact_sounds      = soundsHit
t.death_sounds       = ["samusAranDeath"]
t.pickup_sounds      = sounds
t.fall_sounds        = sounds
t.style              = 'agent'
