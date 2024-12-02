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
import os

def main():
    # 配置参数
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:2531/v2/api")
    token = os.environ.get("GEWECHAT_TOKE", "xxx")
    app_id = os.environ.get("APP_ID", "xxx")
    send_msg_nickname = "张伟" # 要发送消息的好友昵称

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)

    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return
    try:

        # 获取好友列表
        fetch_contacts_list_result = client.fetch_contacts_list(app_id)
        if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
            print("获取通讯录列表失败:", fetch_contacts_list_result)
            return
        # {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['weixin', 'fmessage', 'medianote', 'floatbottle', 'wxid_abcxx'], 'chatrooms': ['1234xx@chatroom'], 'ghs': ['gh_xx']}}
        friends = fetch_contacts_list_result['data'].get('friends', [])
        if not friends:
            print("获取到的好友列表为空")
            return
        print("获取到的好友列表:", friends)

        # 获取好友的简要信息
        friends_info = client.get_brief_info(app_id, friends)
        if friends_info.get('ret') != 200 or not friends_info.get('data'):
            print("获取好友简要信息失败:", friends_info)
            return
        # {
        #     "ret": 200,
        #     "msg": "获取联系人信息成功",
        #     "data": [
        #         {
        #             "userName": "weixin",
        #             "nickName": "微信团队",
        #             "pyInitial": "WXTD",
        #             "quanPin": "weixintuandui",
        #             "sex": 0,
        #             "remark": "",
        #             "remarkPyInitial": "",
        #             "remarkQuanPin": "",
        #             "signature": null,
        #             "alias": "",
        #             "snsBgImg": null,
        #             "country": "",
        #             "bigHeadImgUrl": "https: //wx.qlogo.cn/mmhead/Q3auHgzwzM6H8bJKHKyGY2mk0ljLfodkWnrRbXLn3P11f68cg0ePxA/0",
        #             "smallHeadImgUrl": "https://wx.qlogo.cn/mmhead/Q3auHgzwzM6H8bJKHKyGY2mk0ljLfodkWnrRbXLn3P11f68cg0ePxA/132",
        #             "description": null,
        #             "cardImgUrl": null,
        #             "labelList": null,
        #             "province": "",
        #             "city": "",
        #             "phoneNumList": null
        #         }
        #     ]
        # }
        
        # 找对目标好友的wxid
        friends_info_list = friends_info['data']
        if not friends_info_list:
            print("获取到的好友简要信息列表为空")
            return
        wxid = None
        for friend_info in friends_info_list:
            if friend_info.get('nickName') == send_msg_nickname:
                print("找到好友:", friend_info)
                wxid = friend_info.get('userName')
                break
        if not wxid:
            print(f"没有找到好友: {send_msg_nickname} 的wxid")
            return
        print("找到好友:", wxid)

        # 发送消息
        send_msg_result = client.post_text(app_id, wxid, "你好啊")
        if send_msg_result.get('ret') != 200:
            print("发送消息失败:", send_msg_result)
            return
        print("发送消息成功:", send_msg_result)
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))

if __name__ == "__main__":
    main()

```
