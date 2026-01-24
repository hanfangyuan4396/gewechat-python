from ..util.terminal_printer import make_and_print_qr, print_green, print_yellow, print_red
from ..util.http_util import post_json
import time


class LoginApi:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def _validate_login_type(self, login_type):
        if login_type != "ipad":
            raise ValueError("仅支持ipad登录")

    def _validate_auto_sliding(self, auto_sliding):
        if auto_sliding is True:
            raise ValueError("ipad登录不支持autoSliding=true")

    def get_token(self):
        """获取tokenId"""
        return post_json(self.base_url, "/tools/getTokenId", self.token, {})

    def set_callback(self, token, callback_url):
        """设置微信消息的回调地址"""
        param = {
            "token": token,
            "callbackUrl": callback_url
        }
        return post_json(self.base_url, "/tools/setCallback", self.token, param)

    def get_qr(self, app_id, region_id, login_type="ipad", proxy_ip="", ttuid="", aid=""):
        """获取登录二维码"""
        if not region_id:
            raise ValueError("regionId不能为空")
        self._validate_login_type(login_type)
        param = {
            "appId": app_id,
            "type": login_type,
            "regionId": region_id,
        }
        if proxy_ip:
            param["proxyIp"] = proxy_ip
        if ttuid:
            param["ttuid"] = ttuid
        if aid:
            param["aid"] = aid
        return post_json(self.base_url, "/login/getLoginQrCode", self.token, param)

    def check_qr(self, app_id, uuid, auto_sliding=False, proxy_ip="", captch_code=""):
        """确认登陆"""
        self._validate_auto_sliding(auto_sliding)
        param = {
            "appId": app_id,
            "uuid": uuid,
            "autoSliding": auto_sliding,
        }
        if proxy_ip:
            param["proxyIp"] = proxy_ip
        if captch_code:
            param["captchCode"] = captch_code
        return post_json(self.base_url, "/login/checkLogin", self.token, param)

    def log_out(self, app_id):
        """退出微信"""
        param = {
            "appId": app_id
        }
        return post_json(self.base_url, "/login/logout", self.token, param)

    def dialog_login(self, app_id):
        """弹框登录"""
        param = {
            "appId": app_id
        }
        return post_json(self.base_url, "/login/dialogLogin", self.token, param)

    def check_online(self, app_id):
        """检查是否在线"""
        param = {
            "appId": app_id
        }
        return post_json(self.base_url, "/login/checkOnline", self.token, param)

    def logout(self, app_id):
        """退出"""
        param = {
            "appId": app_id
        }
        return post_json(self.base_url, "/login/logout", self.token, param)

    def _get_and_validate_qr(self, app_id, region_id, login_type, proxy_ip, ttuid, aid):
        """获取并验证二维码数据

        Args:
            app_id: 应用ID

        Returns:
            tuple: (app_id, uuid, qr_data) 或在失败时返回 (None, None, None)
        """

        qr_response = self.get_qr(app_id, region_id, login_type, proxy_ip, ttuid, aid)
        if qr_response.get('ret') != 200:
            print_yellow(f"获取二维码失败:", qr_response)
            return None, None, None

        qr_data = qr_response.get('data', {})
        app_id = qr_data.get('appId')
        uuid = qr_data.get('uuid')
        qr_data_value = qr_data.get('qrData')
        if not app_id or not uuid or not qr_data_value:
            print_yellow(f"app_id: {app_id}, uuid: {uuid}, qr_data: {qr_data_value}, 获取app_id或uuid或qrData失败")
            return None, None, None

        return app_id, uuid, qr_data_value

    def login(self, app_id, region_id, login_type="ipad", proxy_ip="", ttuid="", aid="", auto_sliding=False):
        """执行完整的登录流程
        
        Args:
            app_id: 可选的应用ID，为空时会自动创建新的app_id
            region_id: 登录地区ID
            login_type: 设备类型，仅支持 ipad
            proxy_ip: 代理IP
            ttuid: 代理id
            aid: 本地代理aid
            auto_sliding: 自动滑块，仅支持 false

        Returns:
            tuple: (app_id: str, error_msg: str, login_info: dict|None)
                   成功时 error_msg 为空字符串，login_info 为登录信息
                   失败时 app_id 可能为空字符串，error_msg 包含错误信息
        """
        if not region_id:
            raise ValueError("regionId不能为空")
        self._validate_login_type(login_type)
        self._validate_auto_sliding(auto_sliding)
        # 1. 检查是否已经登录
        input_app_id = app_id
        if input_app_id:
            check_online_response = self.check_online(input_app_id)
            if check_online_response.get('ret') == 200 and check_online_response.get('data'):
                print_green(f"AppID: {input_app_id} 已在线，无需登录")
                return input_app_id, "", None
            else:
                print_yellow(f"AppID: {input_app_id} 未在线，执行登录流程")

        # 2. 获取初始二维码
        app_id, uuid, qr_data = self._get_and_validate_qr(app_id, region_id, login_type, proxy_ip, ttuid, aid)
        if not app_id or not uuid or not qr_data:
            return "", "获取二维码失败", None

        if not input_app_id:
            print_green(f"AppID: {app_id}, 请保存此app_id，下次登录时继续使用!")
            print_yellow("\n新设备登录平台，次日凌晨会掉线一次，重新登录时需使用原来的app_id取码，否则新app_id仍然会掉线，登录成功后则可以长期在线")

        make_and_print_qr(qr_data)

        # 3. 轮询检查登录状态
        retry_count = 0
        max_retries = 100  # 最大重试100次
        
        while retry_count < max_retries:
            login_status = self.check_qr(app_id, uuid, auto_sliding, proxy_ip, "")
            if login_status.get('ret') != 200:
                print_red(f"检查登录状态失败: {login_status}")
                return app_id, f"检查登录状态失败: {login_status}", None

            login_data = login_status.get('data')
            if login_data is None:
                print_yellow("登录响应缺少data，继续等待...")
                time.sleep(5)
                continue

            # 需要人脸/滑块验证的分支（仅返回url）
            verify_url = login_data.get('url')
            if verify_url:
                print_yellow("需要人脸验证，请访问下方链接获取二维码，并使用安盾扫码助手扫码完成验证：")
                print_green(verify_url)
                time.sleep(5)
                continue

            status = login_data.get('status')
            expired_time = login_data.get('expiredTime', 0)
            
            # 检查二维码是否过期，提前5秒重新获取
            if expired_time <= 5:
                print_yellow("二维码即将过期，正在重新获取...")
                _, uuid, qr_data = self._get_and_validate_qr(app_id, region_id, login_type, proxy_ip, ttuid, aid)
                if not uuid or not qr_data:
                    return app_id, "重新获取二维码失败", None

                make_and_print_qr(qr_data)
                continue

            if status == 2:  # 登录成功
                nick_name = login_data.get('nickName', '未知用户')
                print_green(f"\n登录成功！用户昵称: {nick_name}")
                return app_id, "", login_data.get("loginInfo")
            else:
                retry_count += 1
                if retry_count >= max_retries:
                    print_yellow("登录超时，请重新尝试")
                    return app_id, "登录超时，请重新尝试", None
                time.sleep(5)
