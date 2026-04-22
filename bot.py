#!/usr/bin/env python3
import os
import socket
import json
from dotenv import load_dotenv
from obsws_python import ReqClient

load_dotenv()

with open('config.json') as f:
    config = json.load(f)

USERNAME = config['chat']['username']
OAUTH = os.getenv('TWITCH_BOT_OAUTH')
OBS_HOST = config['software']['host']
OBS_PORT = config['software']['port']
OBS_PASS = config['software']['password']

print('=' * 50)
print('OBS RECORDING BOT')
print('=' * 50)
print(f'Twitch: {USERNAME}')
print(f'OBS: {OBS_HOST}:{OBS_PORT}')
print('=' * 50)
print()

class OBS:
    def __init__(self, host, port, pwd):
        self.client = None
        self.ok = False
        try:
            self.client = ReqClient(host=host, port=port, password=pwd)
            self.ok = True
            print('[OBS] Connected')
        except Exception as e:
            print(f'[OBS] Failed: {e}')
    
    def start(self):
        if not self.ok:
            return False
        try:
            self.client.start_record()
            print('[REC] START')
            return True
        except Exception as e:
            print(f'[REC] Error: {e}')
            return False
    
    def stop(self):
        if not self.ok:
            return False
        try:
            self.client.stop_record()
            print('[REC] STOP')
            return True
        except Exception as e:
            print(f'[REC] Error: {e}')
            return False

class IRC:
    def __init__(self, user, token, channel):
        self.user = user
        self.token = token
        self.ch = channel
        self.sock = None
    
    def connect(self):
        try:
            self.sock = socket.socket()
            self.sock.connect(('irc.chat.twitch.tv', 6667))
            self.send(f'PASS oauth:{self.token}')
            self.send(f'NICK {self.user}')
            self.send(f'JOIN #{self.ch}')
            print('[IRC] Connected')
            return True
        except:
            print('[IRC] Failed')
            return False
    
    def send(self, msg):
        try:
            self.sock.send(f'{msg}\r\n'.encode())
        except:
            pass
    
    def say(self, msg):
        self.send(f'PRIVMSG #{self.ch} :{msg}')
    
    def is_mod_or_broadcaster(self, tags_string, username):
        """Prüft ob User Mod oder Broadcaster ist"""
        # Broadcaster check
        if username == self.ch:
            return True
        
        # Mod check - suche nach "mod=1" in den Tags
        if 'mod=1' in tags_string:
            return True
        
        return False
    
    def loop(self, obs):
        try:
            while True:
                data = self.sock.recv(1024).decode('utf-8', errors='ignore')
                for line in data.split('\r\n'):
                    if 'PING' in line:
                        self.send('PONG :tmi.twitch.tv')
                    if 'PRIVMSG' in line and '!' in line:
                        try:
                            # Parse tags und user
                            parts = line.split(' ')
                            tags = parts[0] if parts[0].startswith('@') else ''
                            user = line.split('!')[0][1:] if '@' in line else line.split('!')[0][1:]
                            
                            # Entferne @ von user falls vorhanden
                            if user.startswith('@'):
                                user = user[1:]
                            
                            msg = line.split(':', 2)[2].lower().strip()
                            
                            print(f'[CMD] {user}: {msg}')
                            
                            # Permission check
                            if not self.is_mod_or_broadcaster(tags, user):
                                self.say(f'@{user} Nur Mods und Broadcaster dürfen das')
                                continue
                            
                            if msg == '!rec':
                                obs.start()
                                self.say(f'@{user} Recording started')
                            elif msg == '!stoprec':
                                obs.stop()
                                self.say(f'@{user} Recording stopped')
                        except:
                            pass
        except KeyboardInterrupt:
            print('[BOT] Stopped')

obs = OBS(OBS_HOST, OBS_PORT, OBS_PASS)
irc = IRC(USERNAME, OAUTH, USERNAME)
irc.connect()

print('[BOT] Ready\n')
irc.loop(obs)
