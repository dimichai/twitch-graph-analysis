# -*- coding: utf-8 -*-
import scrapy
from twitch import TwitchClient
from twitchTracker.items import TwitchtrackerItem

class StreamsByGame(scrapy.Spider):
    name = 'streamsbygame'
    allowed_domains = ['www.twitchmetrics.net']
    client = TwitchClient('j21z7w7irlu85f779valj22zswacpf')

    def start_requests(self):

        games = ['Variety',
                 'Apex+Legends',
                 'League+of+Legends',
                 'Fortnite',
                 'Counter-Strike%3A+Global+Offensive',
                 'Just+Chatting',
                 'Dota+2',
                 'Overwatch',
                 'PLAYERUNKNOWN%27S+BATTLEGROUNDS',
                 'Hearthstone',
                 'World+of+Warcraft',
                 'Grand+Theft+Auto+V',
                 'Tom+Clancy%27s+Rainbow+Six%3A+Siege',
                 'FIFA+19',
                 'Call+of+Duty%3A+Black+Ops+4',
                 'StarCraft+II',
                 'Old+School+RuneScape',
                 'Minecraft',
                 'Super+Smash+Bros.+Ultimate',
                 'Sea+of+Thieves',
                 'Music+%26+Performing+Arts',
                 'Anthem']

        for game in games:
            req = scrapy.Request("https://www.twitchmetrics.net/channels/follower?game={}".format(game))
            req.meta['game'] = game
            yield req

    def parse(self, response):
        # get the streamer names
        stream_names = response.xpath('//div[@class="d-flex mb-2 flex-wrap"]/a/h5/text()').extract()

        for name in stream_names[0:10]:
            streamer = TwitchtrackerItem()
            streamer['name'] = name
            streamer['streamId'] = StreamsByGame.client.users.translate_usernames_to_ids(name)[0].id
            streamer['game'] = response.meta['game']
            yield streamer
