# ba_meta require api 6
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
 from typing import Dict,Callable
from ba import _activity,Plugin
import _ba
import random
def i_was_imported()->bool:
 result=getattr(_ba.app,'_snowfall_enabled',False)
 setattr(_ba.app,'_snowfall_enabled',True)
 return result
def redefine(methods:Dict[str,Callable])->None:
 for n,func in methods.items():
  if hasattr(_activity.Activity,n):
   setattr(_activity.Activity,n+'_snowfall',getattr(_activity.Activity,n))
  setattr(_activity.Activity,n,func)
def snowfall(self)->None:
 if hasattr(self,'_snowfall'):
  delattr(self,'_snowfall')
 if getattr(self,'map',None):
  bounds=self.map.get_def_bound_box('map_bounds')
  def emits()->None:
   for i in range(int(bounds[3]*bounds[5])):
    def _emit()->None:
     _ba.emitfx(position=(random.uniform(bounds[0],bounds[3]),random.uniform(bounds[4]*1.15,bounds[4]*1.45),random.uniform(bounds[2],bounds[5])),velocity=(0,0,0),scale=random.uniform(1.5,2),count=random.randint(7,18),spread=random.uniform(0.05,0.1),chunk_type='spark')
    _ba.timer(random.uniform(0.02,0.05)*(i+1),_emit)
  setattr(self,'_snowfall',_ba.timer(0.5,emits,repeat=True))
def on_begin(self)->None:
 self.snowfall()
 return self.on_begin_snowfall()
def main()->None:
 if i_was_imported():
  return
 redefine({'snowfall':snowfall,'on_begin':on_begin})
# ba_meta export plugin
class SnowFall(Plugin):
 def on_app_launch(self)->None:
  main()