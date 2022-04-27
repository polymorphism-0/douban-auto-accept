old_group_id = '' # 填写旧组的id
new_group_id = '' # 填写新组的id

# 账号信息，每次重新登录后，需要修改下面两个参数
douban_cookie = ''
security_token = ''

member_search = "https://www.douban.com/group/" + old_group_id + "/member_search?q={id}&cat=1005"

requests_base_url = "https://www.douban.com/group/" + new_group_id + "/requests/?start="
reject_url = "https://www.douban.com/j/group/" + new_group_id + "/requests/reject"
accept_url = "https://www.douban.com/j/group/" + new_group_id + "/requests/accept"

form_data = "ck=" + security_token + "&req_item={req_items}"
form_data_accept = "ck=" + security_token + "&req_item={req_items}&accept_btn=True"

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.5,en-US;q=0.3',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.5,en-US;q=0.3',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded'
}

log_path = "log/"
