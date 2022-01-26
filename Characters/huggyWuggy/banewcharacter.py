from bastd.actor.spazappearance import Appearance

# Huggy Wuggy #####################################
t         = Appearance('Huggy Wuggy')
t.color_texture      = 'huggyWuggyColor'
t.color_mask_texture = 'huggyWuggyColorMask'
t.icon_texture       = 'huggyWuggyIcon'
t.icon_mask_texture  = 'huggyWuggyIconMask'
t.head_model         = 'huggyWuggyHead'
t.torso_model        = 'huggyWuggyTorso'
t.pelvis_model       = 'none'
t.upper_arm_model    = 'huggyWuggyUpperArm'
t.forearm_model      = 'huggyWuggyForeArm'
t.hand_model         = 'huggyWuggyHand'
t.upper_leg_model    = 'huggyWuggyUpperLeg'
t.lower_leg_model    = 'huggyWuggyLowerLeg'
t.toes_model         = 'huggyWuggyToes'
sounds               = ['huggyWuggy', 'huggyWuggy2',
                        'huggyWuggy3', 'huggyWuggy4']
t.attack_sounds      = sounds
t.jump_sounds        = sounds
t.impact_sounds      = sounds
t.death_sounds       = ['huggyWuggyDeath']
t.pickup_sounds      = sounds
t.fall_sounds        = ['huggyWuggyFall']
t.style              = 'bones'