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