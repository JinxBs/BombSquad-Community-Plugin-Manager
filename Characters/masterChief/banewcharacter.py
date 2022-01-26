from bastd.actor.spazappearance import Appearance

# Master Chief #####################################
t         = Appearance('Master Chief')
t.color_texture      = 'mastercColor'
t.color_mask_texture = 'mastercColorMask'
t.icon_texture       = 'mastercIconColor'
t.icon_mask_texture  = 'mastercIconColorMask'
t.head_model         = 'mastercHead'
t.torso_model        = 'mastercTorso'
t.pelvis_model       = 'mastercPelvis'
t.upper_arm_model    = 'mastercUpperArm'
t.forearm_model      = 'mastercForeArm'
t.hand_model         = 'mastercHand'
t.upper_leg_model    = 'mastercUpperLeg'
t.lower_leg_model    = 'mastercLowerLeg'
t.toes_model         = 'mastercToes'
masterc_sounds       = ['masterc1', 'masterc2', 'masterc3',
                        'masterc4', 'masterc5']
masterc_hit          = ['mastercHit1', 'mastercHit2']
t.attack_sounds      = masterc_sounds
t.jump_sounds        = masterc_sounds
t.impact_sounds      = masterc_hit
t.death_sounds       = ['mastercDeath']
t.pickup_sounds      = masterc_sounds
t.fall_sounds        = ['mastercFall']
t.style              = 'agent'