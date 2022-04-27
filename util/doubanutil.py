from lxml import etree
from config import douban_cookie

cookie = {}


def get_cookie():
    # 获取豆瓣登录Cookie信息
    if cookie:
        return cookie
    for line in douban_cookie.split("; "):
        key, value = line.split("=", 1)
        cookie[key] = value
    return cookie


def get_requests_list(text):
    # 获取这个页面上的的入组申请列表
    return etree.HTML(text).xpath('//ul[@class="group-request-list"]//p[@class="fright"]')


def parse_request(request):
    # 解析用户的uid和申请的uid
    profile_url = request[0].get('href')
    user_uid = profile_url.split('/')[-1]
    request_uid = request[2].get('data-uid')
    return user_uid, request_uid


def parse_search_result(text):
    # 判断搜索页面是否找到uid相同的用户
    if bool(etree.HTML(text).xpath('//*[@name="usp_form"]')):
        return bool(etree.HTML(text).xpath('//*[@class="member-item"]'))
    else:
        # 如果页面没有usp_form元素，是因为遇到验证码了
        raise ValueError("Cannot access search page")
