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