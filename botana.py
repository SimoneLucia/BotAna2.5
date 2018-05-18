import sys
import requests
import configparser
import os
import irc.bot

class Botana(irc.bot.SingleServerIRCBot):
    def __init__(self):
        #To read from config file 'config.ini'
        config = configparser.ConfigParser()

        #The username of the chatbot
        self.BOT_NAME = self.from_config('config\config.ini', config, 'bot_name')
        #The registered application Client ID
        self.CLIENT_ID = self.from_config('config\config.ini', config, 'client_id')
        #The bot OAuth
        self.TOKEN = self.from_config('config\config.ini', config, 'token')
        #The channel's name
        self.USERNAME = self.from_config('config\config.ini', config, 'channel')
        self.CHANNEL = '#' + self.USERNAME

        #Channel ID for API calls
        URL = 'https://api.twitch.tv/kraken/users?login=' + self.USERNAME
        headers = {
            'Client-ID' : self.CLIENT_ID,
            'Accept' : 'application/vnd.twitchtv.v5+json'
        }
        r = requests.get(URL, headers=headers).json()
        self.CHANNEL_ID = r['users'][0]['_id']

        #IRC connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connessione a ' + server + ' nella porta ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+self.TOKEN)], self.USERNAME, self.USERNAME)

    def on_welcome(self, c, e):
        print('Connesso a ' + self.USERNAME + '.')

        #IRC capabilities
        c.cap('REQ', 'twitch.tv/tags')
        c.cap('REQ', 'twitch.tv/commands')
        c.cap('REQ', 'twitch.tv/membership')
        c.join(self.USERNAME)

    def on_pubmsg(self, c, e):
        #It's a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection
        c.privmsg(self.USERNAME, 'Comando: ' + cmd)

    def from_config(self, path, config, name):
        if os.path.exists(path):
            try:
                config.read(path)
                return config['DEFAULT'][name]
            except:
                file = open('LogError.txt', 'a+')
                print('Errore nella lettura di <' + name +'>.\nControlla il file LogError per maggiori dettagli.')
                file.write(time.strftime('[%d/%m/%Y - %H:%M:%S] ') + traceback.format_exc() + "\n")
                traceback.print_exc()
                file.close()
        else:
            print('Errore. Il file config.ini non esiste.')

def main():
    bot = Botana()
    bot.start()

if __name__ == '__main__':
    main()
