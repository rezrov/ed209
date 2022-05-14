import configparser
import json
from signalbot.signalbot_base import signalbot_base

class signalbot_core(signalbot_base):

    def __init__(self, signal, config):
        signalbot_base.__init__(self, signal)
        self.config = config
        # self.config = configparser.ConfigParser()
        # self.configPath = configPath    # hold onto this so we can save back to the file.
        # self.config.read(configPath)  #'/home/ubuntu/ed209/config.ini'
        self.owner = self.config['admin']['owner']                  # Has access to the root functions
        self.admins = json.loads(self.config['admin']['bot_admins'])    # Has access to the admin level funtions
        self.blacklist = json.loads(self.config['admin']['blacklist'])  # ignore these people
        self._botFunctions()

    def echo(self, timestamp, sender, groupID, message, attachments):
        self._universalReply(timestamp, sender, groupID, message[5:].strip())