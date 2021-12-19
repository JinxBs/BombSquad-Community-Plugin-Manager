#squadGame
#by pedram

"""Defines Volley Ball mini-game"""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

from bastd.maps import *
import ba
import _ba
from ba import _map
import random
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory

if TYPE_CHECKING:
    from typing import Any, List, Dict




####### DONT DIE READING THIS #########

### Took me 30mins to port this map ###



a=0.0
class Pointzz:	# Released under the MIT License. See LICENSE for details.
	#
	
	# This file was automatically generated from "big_g.ma"
	# pylint: disable=all
	points = {}
	# noinspection PyDictCreation
	boxes = {}
	boxes['area_of_interest_bounds'] = (0.4011866709, 2.331310176,
	                                    -0.5426286416) + (0.0, 0.0, 0.0) + (
	                                        19.11746262, 10.19675564, 23.50119277)
	boxes['edge_box'] = (-0.103873591, 0.4133341891, 0.4294651013) + (
	    0.0, 0.0, 0.0) + (22.48295719, 1.290242794, 8.990252454)
	points['ffa_spawn1'] = (-10.50,2.95,0)
	points['ffa_spawn2'] = (-10.50,2.95,0)
	points['ffa_spawn3'] = (-10.50,2.95,0)
	points['ffa_spawn4'] = (-10.50,2.95,0)
	points['ffa_spawn5'] = (-10.50,2.95,0)
	points['flag1'] = (7.557928387, 2.889342613, -7.208799596)
	points['flag2'] = (7.696183956, 1.095466627, 6.103380446)
	points['flag3'] = (-8.122819332, 2.844893069, 6.103380446)
	points['flag4'] = (-8.018537918, 2.844893069, -6.202403896)
	points['flag_default'] = (-7.563673017, 2.850652319, 0.08844978098)
	boxes['map_bounds'] = (-0.1916036665, 8.764115729, 0.1971423239) + (
	    0.0, 0.0, 0.0) + (27.41996888, 18.47258973, 22.17335735)
	points['powerup_spawn1'] = (0,100,0)
	points['powerup_spawn2'] = (0,100,0)
	points['powerup_spawn3'] = (0,100,0)
	points['powerup_spawn4'] = (0,100,0)
	points['powerup_spawn5'] = (0,100,0)
	points['race_mine1'] = (-0.06161453294, 1.123140909, 4.966104324)
	points['race_mine10'] = (-6.870248758, 2.851484105, 2.718992803)
	points['race_mine2'] = (-0.06161453294, 1.123140909, 6.99632996)
	points['race_mine3'] = (-0.7319278377, 1.123140909, -2.828583367)
	points['race_mine4'] = (-3.286508423, 1.123140909, 0.8453899305)
	points['race_mine5'] = (5.077545429, 2.850225463, -5.253575631)
	points['race_mine6'] = (6.286453838, 2.850225463, -5.253575631)
	points['race_mine7'] = (0.969120762, 2.851484105, -7.892038145)
	points['race_mine8'] = (-2.976299166, 2.851484105, -6.241064664)
	points['race_mine9'] = (-6.962812986, 2.851484105, -2.120262964)
	points['race_point1'] = (2.280447713, 1.16512015, 6.015278429) + (
	    0.7066894139, 4.672784871, 1.322422256)
	points['race_point10'] = (-4.196540687, 2.877461266, -7.106874334) + (
	    0.1057202515, 5.496127671, 1.028552836)
	points['race_point11'] = (-7.634488499, 2.877461266, -3.61728743) + (
	    1.438144134, 5.157457566, 0.06318119808)
	points['race_point12'] = (-7.541251512, 2.877461266, 3.290439202) + (
	    1.668578284, 5.52484043, 0.06318119808)
	points['race_point2'] = (4.853459878, 1.16512015,
	                         6.035867283) + (0.3920628436, 4.577066678, 1.34568243)
	points['race_point3'] = (6.905234402, 1.16512015, 1.143337503) + (
	    1.611663691, 3.515259775, 0.1135135003)
	points['race_point4'] = (2.681673258, 1.16512015, 0.771967064) + (
	    0.6475414982, 3.602143342, 0.1135135003)
	points['race_point5'] = (-0.3776550727, 1.225615225, 1.920343787) + (
	    0.1057202515, 4.245024435, 0.5914887576)
	points['race_point6'] = (-4.365081958, 1.16512015, -0.3565529313) + (
	    1.627090525, 4.549428479, 0.1135135003)
	points['race_point7'] = (0.4149308672, 1.16512015, -3.394316313) + (
	    0.1057202515, 4.945367833, 1.310190117)
	points['race_point8'] = (4.27031635, 2.19747021, -3.335165617) + (
	    0.1057202515, 4.389664492, 1.20413595)
	points['race_point9'] = (2.552998384, 2.877461266, -7.117366939) + (
	    0.1057202515, 5.512312989, 0.9986814472)
	points['shadow_lower_bottom'] = (-0.2227795102, 0.2903873918, 2.680075641)
	points['shadow_lower_top'] = (-0.2227795102, 0.8824975157, 2.680075641)
	points['shadow_upper_bottom'] = (-0.2227795102, 6.305086402, 2.680075641)
	points['shadow_upper_top'] = (-0.2227795102, 9.470923628, 2.680075641)
	points['spawn1'] = (7.180043217, 2.85596295, -4.407134234) + (0.7629937742,
	                                                              1.0, 1.818908238)
	points['spawn2'] = (5.880548999, 1.142163379, 6.171168951) + (1.817516622, 1.0,
	                                                              0.7724344394)
	points['spawn_by_flag1'] = (7.180043217, 2.85596295,
	                            -4.407134234) + (0.7629937742, 1.0, 1.818908238)
	points['spawn_by_flag2'] = (5.880548999, 1.142163379,
	                            6.171168951) + (1.817516622, 1.0, 0.7724344394)
	points['spawn_by_flag3'] = (-6.66642559, 3.554416948,
	                            5.820238985) + (1.097315815, 1.0, 1.285161684)
	points['spawn_by_flag4'] = (-6.842951255, 3.554416948,
	                            -6.17429905) + (0.8208434737, 1.0, 1.285161684)
	points['tnt1'] = (-3.398312776, 2.067056737, -1.90142919)
	points['tnt2'] = (1.398312776, 2.067056737, -3.90142919)
	points['tnt3'] = (-4.398312776, 2.067056737, 1.90142919)
	points['tnt4'] = (3.398312776, 2.067056737, 3.90142919)
	points['tnt5'] = (-3.398312776, 2.067056737, 4.90142919)
	points['tnt6'] = (-0.398312776, 2.067056737, 0.90142919)
	points['tnt7'] = (6.398312776, 2.067056737, -3.90142919)
	points['tnt8'] = (6.398312776, 2.067056737, -0.90142919)
	points['tnt9'] = (4.398312776, 2.067056737, 0.90142919)
	points['tnt10'] = (-5.398312776, 2.067056737, -3.19)
class squadgame(ba.Map):
    from squadgame_race import Pointzz as defs
    name = "squadgame"

    @classmethod
    def get_play_types(cls) -> List[str]:
        """Return valid play types for this map."""
        return ['melee', 'hockey', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'black'

    @classmethod
    def onPreload(cls):
    	
    
        data: Dict[str, Any] = {
            'model': ba.getmodel('footballStadium'),
            'vr_fill_model': ba.getmodel('footballStadiumVRFill'),
            'collide_model': ba.getcollidemodel('footballStadiumCollide'),
            'tex': ba.gettexture('footballStadium')
        }
        return data
        
    def __init__(self):
        super().__init__()
        shared = SharedObjects.get()

                    
        self.node = ba.newnode('terrain',
                               delegate=self,
                               attrs={
                                   'model':
                                       None,
                                   'collide_model':
                                       ba.getcollidemodel('footballStadiumCollide'),
                                   'color_texture':
                                       None,
                                   'materials': [
                                       shared.footing_material,
                                      
                                   ]
                               })
                    
                    
        ba.newnode('terrain',
                   attrs={
                       'model': ba.getmodel('footballStadiumVRFill'),
                       'vr_only': True,
                       'lighting': False,
                       'background': True,
                       'color_texture': None
                   })
       
        self.floor = ba.newnode('terrain',
                                attrs={
                                    'model': ba.getmodel('hockeyStadiumInner'),
                                    'color':(0.19,0.07,0.03),
                                    'opacity': 0.92,
                                    'opacity_in_low_or_medium_quality': 1.0,
                                    'materials': [shared.footing_material]
                                })
                    
                    
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': ba.getmodel('natureBackground'),
                'lighting': False,
                'background': True,
                'color': (0.10,0.30,0.50)
            })
                    
        
        
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.3, 1.2, 1.0)
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

# ba_meta export plugin
class bypedram(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(squadgame)

