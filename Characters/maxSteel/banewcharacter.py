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