# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.feifei import FateadmApi
from wechatsogou.five import readimg, input
from wechatsogou.filecache import WechatCache
from wechatsogou.exceptions import WechatSogouVcodeOcrException

ws_cache = WechatCache()


def identify_image_callback_by_hand(img):
    """识别二维码

    Parameters
    ----------
    img : bytes
        验证码图片二进制数据

    Returns
    -------
    str
        验证码文字
    """
    im = readimg(img)
    im.show()
    return input("please input code: ")

def identify_image_callback_by_feifei(img):
    pd_id = "105040"  # 用户信息页可以查询到pd信息
    pd_key = "7FHyfRlVN94qrLzQyAavEFgykFFkG0Jx"
    app_id = "305040" # 开发者分成用的账号，在开发者中心可以查询到
    app_key = " 2aWqzFyD23aSUhMfAZ2/KAP9LO5Jk3aR"
    # 识别类型，
    # 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
    pred_type = "30600"
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    api.QueryBalc()
    # 如果不是通过文件识别，则调用Predict接口
    rsp = api.Predict(pred_type, img)
    if rsp.ret_code == 0.0:
        return rsp.pred_rsp.value


def unlock_sogou_callback_example(url, req, resp, img, identify_image_callback):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        验证码页面 之前的 url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    resp : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据
    identify_image_callback : callable
        处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

    Returns
    -------
    dict
        {
            'code': '',
            'msg': '',
        }
    """
    # no use resp
    url_quote = url.split('weixin.sogou.com/')[-1]
    unlock_url = 'http://weixin.sogou.com/antispider/thank.php'
    data = {
        'c': identify_image_callback(img),
        'r': '%2F' + url_quote,
        'v': 5
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + url_quote
    }
    r_unlock = req.post(unlock_url, data, headers=headers)
    if not r_unlock.ok:
        raise WechatSogouVcodeOcrException(
            'unlock[{}] failed: {}'.format(unlock_url, r_unlock.text, r_unlock.status_code))

    return r_unlock.json()


def unlock_weixin_callback_example(url, req, resp, img, identify_image_callback):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        验证码页面 之前的 url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    resp : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据
    identify_image_callback : callable
        处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

    Returns
    -------
    dict
        {
            'ret': '',
            'errmsg': '',
            'cookie_count': '',
        }
    """
    # no use resp

    unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
    data = {
        'cert': time.time() * 1000,
        'input': identify_image_callback(img)
    }
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': url
    }
    r_unlock = req.post(unlock_url, data, headers=headers)
    if not r_unlock.ok:
        raise WechatSogouVcodeOcrException(
            'unlock[{}] failed: {}[{}]'.format(unlock_url, r_unlock.text, r_unlock.status_code))

    return r_unlock.json()
