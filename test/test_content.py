import wechatsogou
from wechatsogou.identify_image import identify_image_callback_by_feifei, unlock_sogou_callback_example, \
    unlock_weixin_callback_example
from wechatsogou.pipline import  MongoUtil

if __name__ == "__main__":
    wx_api = wechatsogou.WechatSogouAPI()
    wx_list = wx_api.get_gzh_article_by_history(keyword="xinlang-xinwen",
                                            unlock_callback_weixin=unlock_weixin_callback_example,
                                            unlock_callback_sogou=unlock_sogou_callback_example,
                                            identify_image_callback_weixin=identify_image_callback_by_feifei,
                                            identify_image_callback_sogou=identify_image_callback_by_feifei)
    mongo = MongoUtil()
    mongo.insertContent(content=wx_list)