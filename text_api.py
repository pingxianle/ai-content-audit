# 测试模拟前端网页去访问本机服务器

import requests


# r = requests.post('http://127.0.0.1:8000/audit', json={'text':'你好,我是大肥鱼'})
# print(r.text)

r = requests.post('http://127.0.0.1:8000/audit', json={'text':''})
print(r.text)




# fastapi dev server.py  启动代码