"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from ba import internal

if TYPE_CHECKING:
    from typing import Type, List, Dict, Tuple, Optional, Any
    import ba

# ba_meta export plugin
class FullStore(ba.Plugin):

    def new_get_store_layout() -> Dict[str, List[Dict[str, Any]]]:
        """Return what's available in the store at a given time.

            Categorized by tab and by section."""
        if _ba.app.store_layout is None:
            _ba.app.store_layout = {
                'characters': [{
                    'items': []
                }],
                'extras': [{
                    'items': ['pro']
                }],
                'maps': [{
                    'items': ['maps.lake_frigid']
                }],
                'minigames': [],
                'icons': [{
                    'items': [
                        'icons.mushroom',
                        'icons.heart',
                        'icons.eyeball',
                        'icons.yinyang',
                        'icons.hal',
                        'icons.flag_us',
                        'icons.flag_mexico',
                        'icons.flag_germany',
                        'icons.flag_brazil',
                        'icons.flag_russia',
                        'icons.flag_china',
                        'icons.flag_uk',
                        'icons.flag_canada',
                        'icons.flag_india',
                        'icons.flag_japan',
                        'icons.flag_france',
                        'icons.flag_indonesia',
                        'icons.flag_italy',
                        'icons.flag_south_korea',
                        'icons.flag_netherlands',
                        'icons.flag_uae',
                        'icons.flag_qatar',
                        'icons.flag_egypt',
                        'icons.flag_kuwait',
                        'icons.flag_algeria',
                        'icons.flag_saudi_arabia',
                        'icons.flag_malaysia',
                        'icons.flag_czech_republic',
                        'icons.flag_australia',
                        'icons.flag_singapore',
                        'icons.flag_iran',
                        'icons.flag_poland',
                        'icons.flag_argentina',
                        'icons.flag_philippines',
                        'icons.flag_chile',
                        'icons.moon',
                        'icons.fedora',
                        'icons.spider',
                        'icons.ninja_star',
                        'icons.skull',
                        'icons.dragon',
                        'icons.viking_helmet',
                        'icons.fireball',
                        'icons.helmet',
                        'icons.crown',
                    ]
                }]
            }
        store_layout = _ba.app.store_layout
        assert store_layout is not None
        store_layout['characters'] = [{
            'items': [
                'characters.kronk', 'characters.zoe', 'characters.jackmorgan',
                'characters.mel', 'characters.snakeshadow', 'characters.bones',
                'characters.bernard', 'characters.agent', 'characters.frosty',
                'characters.pascal', 'characters.pixie'
            ]
        }]
        store_layout['minigames'] = [{
            'items': [
                'games.ninja_fight', 'games.meteor_shower', 'games.target_practice'
            ]
        }]
        store_layout['characters'][0]['items'].append('characters.wizard')
        store_layout['characters'][0]['items'].append('characters.cyborg')
        store_layout['characters'].append({
            'title': 'store.holidaySpecialText',
            'items': ['characters.bunny', 'characters.santa',
                      'characters.taobaomascot']
        })
        store_layout['minigames'].append({
            'title': 'store.holidaySpecialText',
            'items': ['games.easter_egg_hunt']
        })
        return store_layout
    internal.get_store_layout = new_get_store_layout
