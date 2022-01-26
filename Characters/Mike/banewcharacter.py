from bastd.actor.spazappearance import *

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