#!/usr/bin/env python3
import os
import socket
import ssl
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
ALLOWED_ROLES = set(config['chat'].get('allowed_roles', ['broadcaster', 'moderator']))

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
    def __init__(self, user, token, channel, allowed_roles):
        self.user = user
        self.token = token
        self.ch = channel
        self.allowed_roles = allowed_roles
        self.sock = None

    def connect(self):
        try:
            raw = socket.socket()
            raw.connect(('irc.chat.twitch.tv', 6697))
            ctx = ssl.create_default_context()
            self.sock = ctx.wrap_socket(raw, server_hostname='irc.chat.twitch.tv')
            self.send('CAP REQ :twitch.tv/tags')
            self.send(f'PASS oauth:{self.token}')
            self.send(f'NICK {self.user}')
            self.send(f'JOIN #{self.ch}')
            print('[IRC] Connected (TLS)')
            return True
        except Exception as e:
            print(f'[IRC] Failed: {e}')
            return False

    def send(self, msg):
        try:
            self.sock.send(f'{msg}\r\n'.encode())
        except Exception:
            pass

    def say(self, msg):
        self.send(f'PRIVMSG #{self.ch} :{msg}')

    def is_authorized(self, tags, user):
        if user.lower() == self.ch.lower():
            return True
        badges = tags.get('badges', '')
        roles = {b.split('/')[0] for b in badges.split(',') if b}
        return bool(roles & self.allowed_roles)

    def parse_line(self, line):
        tags = {}
        if line.startswith('@'):
            tag_part, _, line = line.partition(' ')
            for pair in tag_part[1:].split(';'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    tags[k] = v
        return tags, line

    def loop(self, obs):
        buf = ''
        try:
            while True:
                data = self.sock.recv(4096).decode('utf-8', errors='ignore')
                if not data:
                    break
                buf += data
                *lines, buf = buf.split('\r\n')
                for raw_line in lines:
                    tags, line = self.parse_line(raw_line)
                    if line.startswith('PING'):
                        self.send('PONG :tmi.twitch.tv')
                        continue
                    if 'PRIVMSG' in line and '!' in line:
                        try:
                            user = line.split('!')[0][1:]
                            msg = line.split(':', 2)[2].lower().strip()
                            print(f'[CMD] {user}: {msg}')
                            if msg not in ('!rec', '!stoprec'):
                                continue
                            if not self.is_authorized(tags, user):
                                self.say(f'@{user} du darfst diesen Befehl nicht nutzen.')
                                continue
                            if msg == '!rec':
                                obs.start()
                                self.say('Recording started')
                            elif msg == '!stoprec':
                                obs.stop()
                                self.say('Recording stopped')
                        except Exception:
                            pass
        except KeyboardInterrupt:
            print('[BOT] Stopped')

obs = OBS(OBS_HOST, OBS_PORT, OBS_PASS)
irc = IRC(USERNAME, OAUTH, USERNAME, ALLOWED_ROLES)
irc.connect()

print('[BOT] Ready\n')
irc.loop(obs)
