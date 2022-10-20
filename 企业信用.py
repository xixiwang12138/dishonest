import requests

url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg='

data = {
    # 'draw':'1',
    'start': '0',
    # 'length':'10'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Cookie': '__jsluid=665b7ca3ef2248cc918ef39b209dc7fc; __jsl_clearance=1545702823.489|0|qFApc3mSdSpllfD%2Bo65mwYpq0OY%3D; JSESSIONID=2E2E256DC1FA4D7AEB872730E516D349-n2:1'
}

response = requests.post(url, data=data, headers=headers)
print(response.status_code)
print(response.content.decode())
