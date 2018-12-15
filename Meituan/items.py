# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'meituan_meishi'
    # 店铺id
    poi_id = scrapy.Field()
    # 城市id
    city_id = scrapy.Field()
    # 城市名称
    city_name = scrapy.Field()
    # 类别
    category = scrapy.Field()
    # 店铺标题
    title = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 关键字
    keyword = scrapy.Field()
    # front_image = scrapy.Field()
    # 是否有广告
    has_ads = scrapy.Field()
    # 店铺名
    name = scrapy.Field()
    # 平均分
    avg_score = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # 营业时间
    open_time = scrapy.Field()
    # 商家服务
    extra_infos = scrapy.Field()
    # 是否有食品安全档案
    has_food_safe_info = scrapy.Field()
    # 坐标
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    # 人均消费
    avg_price = scrapy.Field()
    # 品牌
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    # 是否展示
    show_status = scrapy.Field()
    # 是否美食
    is_meishi = scrapy.Field()
    # 推荐菜
    recommended = scrapy.Field()
    # 团购优惠及代金券
    deal_list = scrapy.Field()
    # 附近商家
    near_pois = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()


class MeituanInfosItem(scrapy.Item):
    collection = 'meituan_meishi_infos'
    poi_id = scrapy.Field()
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    category = scrapy.Field()
    # 食品安全档案信息
    safety_detail = scrapy.Field()
    # 店铺详情
    detail_info = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 评论标签
    comment_tags = scrapy.Field()
    # 店内图片
    photos = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()



