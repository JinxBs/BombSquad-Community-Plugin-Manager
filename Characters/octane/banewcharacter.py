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