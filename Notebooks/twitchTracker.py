# -*- coding: utf-8 -*-
import scrapy
from twitch import TwitchClient
from twitchTracker.items import TwitchtrackerItem

class TwitchTracker(scrapy.Spider):
    name = 'twitchtracker'
    allowed_domains = ['www.twitchtracker.com']
    client = TwitchClient('j21z7w7irlu85f779valj22zswacpf')

    def start_requests(self):
        for rank_start in range(1, 11):   # go to 201
            yield scrapy.Request("https://twitchtracker.com/channels/most-followers?page={}".format(rank_start))

    def parse(self, response):
        # get the streamer names
        stream_names = response.xpath('//div[@class="ri-name"]/a/text()').extract()
        stream_follows = response.xpath('//div[@class="ri-value"]/div/text()').extract()
        for stream in zip(stream_names, stream_follows):
            streamer = TwitchtrackerItem()
            streamer['name'] = stream[0]
            streamer['streamId'] = TwitchTracker.client.users.translate_usernames_to_ids(stream[0])[0].id
            streamer['follows'] = stream[1]
            yield streamer
