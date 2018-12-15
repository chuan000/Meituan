# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
import json
import re
from Meituan.items import MeituanItem, MeituanInfosItem
from Meituan.settings import *
from random import random, randint
import time


class MeituanMeishiSpider(Spider):
    name = 'meituan_meishi'
    # allowed_domains = ['meituan.com']
    # start_urls = ['https://bj.meituan.com/meishi/']
    category_urls = ['https://bj.meituan.com/meishi/']
    regex_p = re.compile(r'window._appState = ({.*});')

    detail_url = 'https://www.meituan.com/meishi/{}/'
    list_page_url = 'https://bj.meituan.com/meishi/pn{}/'
    food_safety_detail_url = 'https://www.meituan.com/meishi/api/poi/getFoodSafetyDetail'
    comment_url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment'
    near_url = 'https://www.meituan.com/meishi/api/poi/getNearPoiList?offset=0&limit=10&cityId=1&lat={:.6f}&lng={:.6f}'
    cookie_args = 2

    def start_requests(self):
        for url in self.category_urls:
            list_page_headers = LIST_PAGE_HEADERS
            list_page_headers['Cookie'] = LIST_PAGE_COOKIES.format(39+random(), 116+random(), randint(6, 100))
            time.sleep(randint(0, 2))
            yield Request(url, headers=list_page_headers, callback=self.parse_list_page, meta={'page': 1})

    def parse_list_page(self, response):
        try:
            page_infos = self.regex_p.search(response.text).group(1)
            infos_dict = json.loads(page_infos)
            page = response.meta['page']
            if infos_dict.get('poiLists').get('poiInfos'):
                if not infos_dict['poiLists']['poiInfos']:
                    return
                poi_infos = infos_dict['poiLists']['poiInfos']
                for poi_info in poi_infos:
                    poi_id = poi_info['poiId']
                    # front_img = poi_info['frontImg']
                    has_ads = poi_info.get('hasAds')
                    detail_page_headers = DETAIL_PAGE_HEADERS
                    detail_page_headers['Cookie'] = DETAIL_PAGE_COOKIES.format(
                        39+random(), 116+random(), randint(6, 100))
                    time.sleep(randint(0, 2))
                    yield Request(url=self.detail_url.format(poi_id),
                                  headers=detail_page_headers,
                                  meta={'has_ads': has_ads, 'poi_id': poi_id},
                                  callback=self.parse_detail_page
                                  )
                if page < 42:
                    next_page = page + 1
                    list_page_headers = LIST_PAGE_HEADERS
                    list_page_headers['Cookie'] = LIST_PAGE_COOKIES.format(39 + random(), 116 + random(), randint(6, 100))
                    time.sleep(randint(0, 2))
                    yield Request(url=self.list_page_url.format(next_page), meta={
                        'page': next_page}, headers=list_page_headers, callback=self.parse_list_page)
        except Exception as e:
            with open('list_page.html', 'w') as f:
                f.write(response.text)
            raise Exception(e.args, response.url)

    def parse_detail_page(self, response):
        page_infos = self.regex_p.search(response.text).group(1)
        infos_dict = json.loads(page_infos)

        meituan_item = MeituanItem()
        infos_item = MeituanInfosItem()
        meituan_item['city_id'] = infos_dict.get('$meta').get('cityId')
        meituan_item['city_name'] = infos_dict.get('$meta').get('cityName')
        meituan_item['category'] = CATEGORY
        meituan_item['title'] = infos_dict.get('title')
        meituan_item['description'] = infos_dict.get('description')
        meituan_item['keyword'] = infos_dict.get('keyword')
        # meituan_item['front_image'] = response.meta['front_img']
        meituan_item['has_ads'] = response.meta['has_ads']
        detail_info = infos_dict.get('detailInfo')
        if detail_info:
            meituan_item['poi_id'] = detail_info.get('poiId')
            meituan_item['name'] = detail_info.get('name')
            meituan_item['avg_score'] = detail_info.get('avgScore')
            meituan_item['address'] = detail_info.get('address')
            meituan_item['phone'] = detail_info.get('phone')
            meituan_item['open_time'] = detail_info.get('openTime')
            meituan_item['extra_infos'] = detail_info.get('extraInfos')
            meituan_item['has_food_safe_info'] = detail_info.get('hasFoodSafeInfo')
            meituan_item['longitude'] = detail_info.get('longitude')
            meituan_item['latitude'] = detail_info.get('latitude')
            meituan_item['avg_price'] = detail_info.get('avgPrice')
            meituan_item['brand_id'] = detail_info.get('brandId')
            meituan_item['brand_name'] = detail_info.get('brandName')
            meituan_item['show_status'] = detail_info.get('showStatus')
            meituan_item['is_meishi'] = detail_info.get('isMeishi')
        meituan_item['recommended'] = infos_dict.get('recommended')
        meituan_item['deal_list'] = infos_dict.get('dealList')
        yield meituan_item

        infos_item['city_id'] = meituan_item['city_id']
        infos_item['city_name'] = meituan_item['city_name']
        infos_item['category'] = CATEGORY
        infos_item['poi_id'] = detail_info.get('poiId')
        infos_item['detail_info'] = infos_dict.get('detailInfo')
        infos_item['photos'] = infos_dict.get('photos')
        yield infos_item

        food_safety_detail_headers = FOOD_SAFETY_DETAIL_HEADERS
        food_safety_detail_headers['Cookie'] = FOOD_SAFETY_DETAIL_COOKIES.format(
            36+random(), 116+random(), randint(1, 50))
        food_safety_detail_headers['Referer'] = self.detail_url.format(detail_info.get('poiId'))
        pay_load = {'poiId': str(detail_info.get('poiId'))}
        if meituan_item['has_food_safe_info']:
            time.sleep(randint(0, 2))
            yield FormRequest(url=self.food_safety_detail_url,
                              method='POST',
                              encoding='utf-8',
                              headers=food_safety_detail_headers,
                              body=json.dumps(pay_load),
                              callback=self.parse_food_safety,
                              meta={'poi_id': meituan_item['poi_id']}
                              )

        comment_args = {
            'uuid': 'e62cdad445af4a12ae73.1544164130.3.0.0',
            'platform': '1',
            'partner': '126',
            'originUrl': response.url,
            'riskLevel': '1',
            'optimusCode': '1',
            'id': str(meituan_item['poi_id']),
            'offset': '0',
            'pageSize': '10',
            'sortType': '1'
        }
        comment_headers = COMMENT_HEADERS
        comment_headers['Referer'] = response.url

        comment_headers['Cookie'] = COMMENT_COOKIES.format(randint(6, 50), 39+random(), 116+random())
        comment_url = self.comment_url + '?'
        count = 0
        for k, v in comment_args.items():
            if count == 0:
                comment_url += '='.join([k, v])
            else:
                comment_url = comment_url + '&' + '='.join([k, v])
            count += 1
        time.sleep(randint(0, 2))
        yield Request(
            url=comment_url, headers=comment_headers,
            callback=self.parse_comment,
            meta={'poi_id': detail_info.get('poiId')}
        )

        near_url = self.near_url.format(39+random(), 116+random())
        near_headers = NEAR_POIS_HEADERS
        near_cookie = NEAR_POI_COOKIES.format(randint(6, 100), 39+random(), 116+random())
        near_headers['Cookie'] = near_cookie
        near_headers['Referer'] = self.detail_url.format(detail_info.get('poiId'))
        yield Request(
            url=near_url, headers=near_headers, callback=self.parse_near_poi,
            meta={'poi_id': detail_info.get('poiId')}
        )

    def parse_near_poi(self, response):
        infos = response.text
        infos = json.loads(infos)
        if infos['status'] == 0 and infos.get('data'):
            meituan_item = MeituanItem()
            meituan_item['near_pois'] = infos.get('data')
            meituan_item['poi_id'] = response.meta['poi_id']
            yield meituan_item

    def parse_food_safety(self, response):
        try:
            safety_detail = response.text
            poi_id = response.meta['poi_id']

            infos_item = MeituanInfosItem()
            infos_item['poi_id'] = poi_id
            infos_item['safety_detail'] = safety_detail
            yield infos_item
        except Exception as e:
            print('parse food safety page error', e.args, response.meta['poi_id'])
            with open('food_safety_page' + response.meta['poi_id'] + '.html', 'w') as f:
                f.write(response.text)

    def parse_comment(self, response):
        try:
            infos = response.text
            infos = json.loads(infos)
            if infos['status'] == 0 and infos.get('data'):
                infos_item = MeituanInfosItem()
                infos_item['comment_tags'] = infos.get('data').get('tags')
                infos_item['comment_count'] = infos.get('data').get('total')
                infos_item['poi_id'] = response.meta['poi_id']
                yield infos_item
        except Exception as e:
            print('parse comment page error', e.args, response.url)
            with open('comment_page' + response.meta['poi_id'] + '.html', 'w') as f:
                f.write(response.text)
