# -*- coding: utf-8 -*-
import scrapy
from twitch import TwitchClient
from twitchTracker.items import TwitchtrackerItem

class TwitchTrackerGreek(scrapy.Spider):
    name = 'twitchtrackergreek'
    # allowed_domains = ['www.twitchtracker.com']
    client = TwitchClient('j21z7w7irlu85f779valj22zswacpf')
    #start_urls = ["https://twitchtracker.com/channels/live/greek?page=1"]

    def start_requests(self):
        types = ['live', 'rating', 'viewership', 'hours-watched', 'followers-growth', 'peak-viewers', 'most-followers', 'most-views']
        for t in types:  # greek streams
            yield scrapy.Request("https://twitchtracker.com/channels/{}/greek?page=1".format(t))

    def parse(self, response):
        # get the streamer names
        stream_names = response.xpath('//div[@class="ri-name"]/a/text()').extract()
        for stream in stream_names:
            streamer = TwitchtrackerItem()
            streamer['name'] = stream
            streamer['streamId'] = TwitchTrackerGreek.client.users.translate_usernames_to_ids(stream)[0].id
            yield streamer

        # Pagination
        next_page = response.xpath('//ul[@class="pagination"]/li/a[@rel="next"]/@href')
        if next_page is not None:
            for href in next_page:
                yield response.follow(href, self.parse)
