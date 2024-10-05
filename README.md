# gewechat-python

gewechat python client

## Usage

安装 gewechat client
```sh
pip install gewechat-client
```

使用demo
```python
from gewechat_client import GewechatClient

base_url = "http://127.0.0.1:2531/v2/api"
download_url = "http://127.0.0.1:2532/download"
token = "xxx"
app_id = "xxx"

# 创建 GewechatClient 实例
client = GewechatClient(base_url, download_url, token)

try:
    contacts_list = client.fetch_contacts_list(app_id)
    print("Fetched contacts list successfully!")
    print("Contacts list:", contacts_list)
except Exception as e:
    print("Failed to fetch contacts list:", str(e))
```
