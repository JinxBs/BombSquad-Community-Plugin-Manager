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