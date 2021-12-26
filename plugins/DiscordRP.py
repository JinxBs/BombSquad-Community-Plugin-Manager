# ba_meta require api 6

'''
Bombsquad Discord Rich Presence  by Mr.Smoothy
v1.0   13 june 2021

Watch : https://www.youtube.com/watch?v=RB0jzZ95gY4
Checkout : https://www.youtube.com/c/heysmoothy    for more interesting mods
Bombsquad 1.6 Server : https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server
Stay upto date join : https://discord.gg/ucyaesh

Just install and enable this plugin and you go .
only compatible with discord desktop app (Windows/Linux)  (not discord in browser).

Inspired by JRMP ,  mod requested by Firefighter1077

Join Discord 
BCS      : https://discord.gg/ucyaesh
Bombspot : https://discord.gg/2RKd9QQdQY
JRMP     : https://discord.gg/Zz4XsrTUpT
SahilP   : https://discord.gg/B9mJaQAuKv

Released under MIT Licence   

'''


from __future__ import annotations

from typing import TYPE_CHECKING

import ba

import threading

from ba._error import print_exception, print_error, NotFoundError
from ba._gameutils import animate, animate_array
from ba._language import Lstr
from ba._enums import SpecialChar, InputType
from ba._profile import get_player_profile_colors
if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional
import weakref
import os,json

import time
from time import mktime
from ba._enums import TimeType

from abc import ABCMeta, abstractmethod

import logging

import socket
import sys
import struct
import uuid

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4

logger = logging.getLogger(__name__)


class DiscordIpcError(Exception):
    pass


class DiscordIpcClient(metaclass=ABCMeta):

    """Work with an open Discord instance via its JSON IPC for its rich presence API.

    In a blocking way.
    Classmethod `for_platform`
    will resolve to one of WinDiscordIpcClient or UnixDiscordIpcClient,
    depending on the current platform.
    Supports context handler protocol.
    """

    def __init__(self, client_id):
        self.client_id = client_id
        self._connect()
        self._do_handshake()
        logger.info("connected via ID %s", client_id)

    @classmethod
    def for_platform(cls, client_id, platform=sys.platform):
        if platform == 'win32':
            return WinDiscordIpcClient(client_id)
        else:
            return UnixDiscordIpcClient(client_id)

    @abstractmethod
    def _connect(self):
        pass

    def _do_handshake(self):
        ret_op, ret_data = self.send_recv({'v': 1, 'client_id': self.client_id}, op=OP_HANDSHAKE)
        # {'cmd': 'DISPATCH', 'data': {'v': 1, 'config': {...}}, 'evt': 'READY', 'nonce': None}
        if ret_op == OP_FRAME and ret_data['cmd'] == 'DISPATCH' and ret_data['evt'] == 'READY':
            return
        else:
            if ret_op == OP_CLOSE:
                self.close()
            raise RuntimeError(ret_data)

    @abstractmethod
    def _write(self, date: bytes):
        pass

    @abstractmethod
    def _recv(self, size: int) -> bytes:
        pass

    def _recv_header(self) -> (int, int):
        header = self._recv_exactly(8)
        return struct.unpack("<II", header)

    def _recv_exactly(self, size) -> bytes:
        buf = b""
        size_remaining = size
        while size_remaining:
            chunk = self._recv(size_remaining)
            buf += chunk
            size_remaining -= len(chunk)
        return buf

    def close(self):
        logger.warning("closing connection")
        try:
            self.send({}, op=OP_CLOSE)
        finally:
            self._close()

    @abstractmethod
    def _close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def send_recv(self, data, op=OP_FRAME):
        self.send(data, op)
        return self.recv()

    def send(self, data, op=OP_FRAME):
        logger.debug("sending %s", data)
        data_str = json.dumps(data, separators=(',', ':'))
        data_bytes = data_str.encode('utf-8')
        header = struct.pack("<II", op, len(data_bytes))
        self._write(header)
        self._write(data_bytes)

    def recv(self) -> (int, "JSON"):
        """Receives a packet from discord.

        Returns op code and payload.
        """
        op, length = self._recv_header()
        payload = self._recv_exactly(length)
        data = json.loads(payload.decode('utf-8'))
        logger.debug("received %s", data)
        return op, data

    def set_activity(self, act):
        
        # act
        data = {
            'cmd': 'SET_ACTIVITY',
            'args': {'pid': os.getpid(),
                     'activity': act},
            'nonce': str(uuid.uuid4())
        }
        self.send(data)


class WinDiscordIpcClient(DiscordIpcClient):

    _pipe_pattern = R'\\?\pipe\discord-ipc-{}'

    def _connect(self):
        for i in range(10):
            path = self._pipe_pattern.format(i)
            try:
                self._f = open(path, "w+b")
            except OSError as e:
                pass
                
                #logger.error("Discord not running ")
                #logger.error("failed to open {!r}: {}".format(path, e))
            else:
                break
        else:
            return DiscordIpcError("Failed to connect to Discord pipe")

        self.path = path

    def _write(self, data: bytes):
        try:
            self._f.write(data)
            self._f.flush()
        except:
            pass

    def _recv(self, size: int) -> bytes:
        try:
            return self._f.read(size)
        except:
            return b"0"
        

    def _close(self):
        self._f.close()


class UnixDiscordIpcClient(DiscordIpcClient):

    def _connect(self):
        self._sock = socket.socket(socket.AF_UNIX)
        pipe_pattern = self._get_pipe_pattern()

        for i in range(10):
            path = pipe_pattern.format(i)
            if not os.path.exists(path):
                continue
            try:
                self._sock.connect(path)
            except OSError as e:
                pass
                #logger.error("failed to open {!r}: {}".format(path, e))
            else:
                break
        else:
            return DiscordIpcError("Failed to connect to Discord pipe")

    @staticmethod
    def _get_pipe_pattern():
        env_keys = ('XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP')
        for env_key in env_keys:
            dir_path = os.environ.get(env_key)
            if dir_path:
                break
        else:
            dir_path = '/tmp'
        return os.path.join(dir_path, 'discord-ipc-{}')

    def _write(self, data: bytes):
        self._sock.sendall(data)

    def _recv(self, size: int) -> bytes:
        return self._sock.recv(size)

    def _close(self):
        self._sock.close()



# ba_meta export plugin
class HeySmoothy(ba.Plugin):
    def on_app_launch(self):

        
        
        if self.discordrunning():
            self.rpc_obj = DiscordIpcClient.for_platform(self.client_id)
            self.dcLastState=True
        
        self.timerr=ba.Timer(9.0,self.main,repeat=True,timetype=TimeType.REAL)

    
        

    def __init__(self):
        self.details="Just started"
        self.state="Just Started"
        self.laststatus="offline"
        self.starttime=mktime(time.localtime())
        self.dcLastState=False
        self.client_id = '806052133761450024'
        print("Discord RP Plugin by Mr.Smoothy \n Search \"HeySmoothy\" on Youtube for more.")
        
        self._pipe_pattern = R'\\?\pipe\discord-ipc-{}'
        self.x=0
  
    def discordrunning(self):
        for i in range(10):
            path = self._pipe_pattern.format(i)
            try:
                self._f = open(path, "w+b")
            except:
                self.x +=1
            else:
                
                self._f.close()
                return True
        if self.x==9:
            
            return False

        
    def main(self):
        
        if self.discordrunning():
            if not self.dcLastState:
                self.rpc_obj = DiscordIpcClient.for_platform(self.client_id)
                self.dcLastState=True
                
        else:
            self.dcLastState=False
      
        self.getstatus()
        start_time = mktime(time.localtime())
         
        _pipe_pattern = R'\\?\pipe\discord-ipc-{}'
        
        activity = {
                    "state": self.state,  
                    "details": self.details,  
                    "timestamps": {
                        "start": self.starttime
                    },

                    "assets": {
                        "small_text": "bslogo",  
                        "small_image": "bslogo",  
                        "large_text": "large",  
                        "large_image": "large"  
                    }
                }
        if self.dcLastState:
            self.rpc_obj.set_activity(activity)
            
    def getstatus(self):
        import _ba
        if _ba.get_connection_to_host_info()=={}:
            act=_ba.get_foreground_host_activity()
            self.state=act.__class__.__name__.replace("Activity","")
            
            if len(_ba.get_game_roster())==0:
                self.details="Local"
            else:
                self.details="Local ("+str(len(_ba.get_game_roster()))+" Players)"

            if self.laststatus=="online":
                self.starttime=mktime(time.localtime())
            self.laststatus="offline"
        else:
            self.state=_ba.get_connection_to_host_info()["name"]
            if len(_ba.get_game_roster())<=2:
                self.details="Online Alone !!"
            else:
                self.details="Online ("+str(len(_ba.get_game_roster()))+" Players)"

            if self.laststatus=="offline":
                self.starttime=mktime(time.localtime())
            self.laststatus="online"






        
        
    
