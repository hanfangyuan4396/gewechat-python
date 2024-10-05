from gewechat_client import GeWeChatClient
import os

def main():
    # 配置参数
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:2531/v2/api")
    download_url = os.environ.get("DOWNLOAD_URL", "http://127.0.0.1:2532/download")
    token = os.environ.get("GEWECHAT_TOKE", "xxx")
    app_id = os.environ.get("APP_ID", "xxx")

    # 创建 GeWeChatClient 实例
    client = GeWeChatClient(base_url, download_url, token)

    try:
        contacts_list = client.fetch_contacts_list(app_id)
        print("Fetched contacts list successfully!")
        print("Contacts list:", contacts_list)
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))

if __name__ == "__main__":
    main()
