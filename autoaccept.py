import random
import time
import requests
import sys
import urllib3
from sys import argv

from util import logmodule
from util import doubanutil
from config import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logmodule.LogModule()


class DECISION:
    REJECT = 0
    ACCEPT = 1
    HOLD = 2


def process_requests(requests_url):
    """
    处理这一页的所有入组申请
    """
    try:
        parsed_requests = get_requests_list(requests_url)
        accept_list, reject_list = check_users(parsed_requests)
        if accept_list:
            post_decision(accept_list, True)
        if reject_list:
            post_decision(reject_list, False)
    except Exception as e:
        logger.error("Exception: " + str(e))


def get_requests_list(requests_url):
    """
    获取这一页的申请列表
    """
    r = requests.get(requests_url, headers=default_headers,
                     cookies=doubanutil.get_cookie(), verify=False, timeout=(5, 10))
    requests_list = list(doubanutil.get_requests_list(r.text))
    parsed_requests = []
    for request in requests_list:
        parsed_requests.append(doubanutil.parse_request(request))

    if len(parsed_requests) == 0:
        # 如果这一页没有入组申请，是因为豆瓣反爬虫的机制导致页面加载不出来（一般来说是遇到验证码）
        # 所以直接退出程序，等人工解决以后再重新运行
        print(r.text)
        logger.error("豆瓣反爬虫的机制导致页面加载不出来，退出程序，等人工解决以后再重新运行")
        sys.exit()
    return parsed_requests


def check_users(parsed_requests):
    """
    返回哪些用户应该通过，哪些应该拒绝
    """
    accept_list = []
    reject_list = []
    for parsed_request in parsed_requests:
        decision, request_uid = check_user(parsed_request)
        if decision == DECISION.ACCEPT:
            accept_list.append(request_uid)
        elif decision == DECISION.REJECT:
            reject_list.append(request_uid)
    return accept_list, reject_list


def check_user(parsed_request):
    """
    检查用户是否加了旧组
    """
    user_uid, request_uid = parsed_request
    try:
        r = requests.get(member_search.format(id=user_uid), headers=default_headers,
                         cookies=doubanutil.get_cookie(), verify=False, timeout=(5, 10))
        is_member = doubanutil.parse_search_result(r.text)
        if is_member:
            logger.info("accept: " + user_uid)
            return DECISION.ACCEPT, request_uid
        else:
            logger.info("reject: " + user_uid)
            return DECISION.REJECT, request_uid
    except ValueError:
        # 遇到ValueError的话是因为豆瓣检测到操作频繁，无法看到搜索结果，需要输入验证码才能继续
        logger.error("操作频繁，遇到验证码")
        input("请用浏览器打开任意一个豆瓣页面并且输入验证码后，在terminal输入回车继续审核")
        return check_user(parsed_request)
    except Exception as e:
        # 一般是网络问题，所以先跳过这个申请，并且让程序暂停一段时间
        logger.error("Exception: " + str(e) + ' ' + user_uid)
        time.sleep(random.randint(10, 20))
        return DECISION.HOLD, request_uid


def post_decision(requests_list, is_accept):
    if is_accept:
        url = accept_url
        log_desc = "accepted"
    else:
        url = reject_url
        log_desc = "rejected"

    req_items = '&req_item='.join(requests_list)
    r = requests.post(url, data=form_data.format(req_items=req_items),
                      headers=post_headers, cookies=doubanutil.get_cookie())

    while r.status_code != 200:
        # post失败的话同样是因为遇到验证码了，需要打开浏览器，手动输入验证码才能继续
        logger.error("操作频繁，遇到验证码")
        input("请用浏览器打开任意一个豆瓣页面并且输入验证码后，在terminal输入回车继续审核")
        r = requests.post(reject_url, data=form_data.format(req_items=req_items),
                          headers=post_headers, cookies=doubanutil.get_cookie())

    count = len(requests_list)
    logger.info("Number of " + log_desc + " requests in this page: " + str(count))


if __name__ == "__main__":
    requests_number = int(argv[1])

    while requests_number >= 0:
        requests_url = requests_base_url + str(requests_number)
        logger.info("Process page: " + requests_url)
        process_requests(requests_url)
        requests_number -= 50  # 翻页到前一页，每一页有50个申请
        time.sleep(random.randint(5, 8))
