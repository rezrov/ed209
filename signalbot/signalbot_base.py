import logging
# from pydbus import SystemBus

class signalbot_base():

    def __init__(self, signal):
        self.signal = signal
        self.function_list = []
        self.admin_function_list = []
        self.root_function_list = []
        self._botFunctions()

    def _botFunctions(self):
        for item in dir(__class__):
            if not item.startswith("_") and not item.endswith('Handler'):
                if item.startswith('admin'):
                    self.admin_function_list.append(item)
                elif item.startswith('root'):
                    self.root_function_list.append(item)
                else:
                    self.function_list.append(item)

    def messageHandler(self, timestamp, sender, groupID, message, attachments):
        # found = False
        logging.debug(f"sender: {sender}, group: {groupID}, message: {message}")
        if len(message) > 0 and message[0] == '/':  # If a message doesn't start with / we don't care and quit
            messagefields = message[1:].split()
            if sender not in self.blacklist:
                if messagefields[0] in self.function_list:
                    getattr(self, messagefields[0])(timestamp, sender, groupID, message, attachments)
                    # found = True
                elif messagefields[0] in self.admin_function_list and (sender in self.admins or sender == self.owner):
                    getattr(self, messagefields[0])(timestamp, sender, groupID, message, attachments)
                elif messagefields[0] in self.root_function_list and sender == self.owner:
                    getattr(self, messagefields[0])(timestamp, sender, groupID, message, attachments)
                else:
                    self._noMatchFound(timestamp, sender, groupID, message, attachments)
            else:
                self._blacklistHandler(timestamp, sender, groupID, message, attachments)
            #     for item in self.function_list:
            #         if message[1:].startswith(item):
            #             getattr(self, item)(timestamp, sender, groupID, message, attachments)
            #             found = True
            #             break
                
            #     # Admin only functions
            #     if sender in self.admins or sender == self.owner:
            #         for item in self.admin_function_list:
            #             if message[1:].startswith(item): 
            #                 getattr(self, item)(timestamp, sender, groupID, message, attachments)
            #                 found = True
            #                 break

            #     # Root only functions
            #     if sender == self.owner:
            #         for item in self.root_function_list:
            #             if message[1:].startswith(item): 
            #                 getattr(self, item)(timestamp, sender, groupID, message, attachments)
            #                 found = True
            #                 break
            # else:
            #     self._blacklistHandler(timestamp, sender, groupID, message, attachments)
            #     found = True

            # We made it all the way to the end and didn't find anything, better do our no match function
            # if not found:
            #     self._noMatchFound(timestamp, sender, groupID, message, attachments)

    def _noMatchFound(self, timestamp, sender, groupID, message, attachments):
        response = "Were you talking to me? I don't understand that command.  Run /help for a list of available commands."
        self._universalReply(timestamp, sender, groupID, response)

    def _blacklistHandler(self, timestamp, sender, groupID, message, attachments):
        # self._universalReply(timestamp, sender, groupID, "", [random.choice(json.loads(self.config['blacklist']['images']))])
        response = "go away"
        self._universalReply(timestamp, sender, groupID, response)

    def _universalReply(self, timestamp, sender, groupID, message, attachments = []):
        self.signal.sendReadReceipt(sender, [timestamp])
        if groupID:
            self.signal.sendGroupMessage(message, attachments, groupID)
        else:
            self.signal.sendMessage(message, attachments, [sender])
