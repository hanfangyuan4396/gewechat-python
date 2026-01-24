# 执行登录(步骤2)

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/login/checkLogin:
    post:
      summary: 执行登录(步骤2)
      deprecated: false
      description: >+
        -
        步骤1若选择ipad登录，新用户首次需要人脸app进行二次处理，若选择mac登录，则支持自动验证/App验证二选一，具体以autoSliding字段进行处理

        -
        [ipad登录人脸识别app下载地址](https://app.qiweapi.com/)(仅支持ios，用苹果自带浏览器打开下载)、[mac登录滑块app下载地址](https://www.pgyer.com/secureandroid)

        - 获取到二维码后可以每间隔**5s**调用本接口来判断是否登录成功（二维码有效期在150s内）

        -
        新设备登录平台，次日凌晨会掉线一次，重新登录时需调用[获取二维码且传appId取码](http://doc.geweapi.com/api-139908278)，登录成功后则可以长期在线

        - 登录成功后请保存appId与wxid的对应关系，后续接口中会用到

        <Accordion title="登录流程图"  defaultOpen={false}>

        <Columns>
            <Column class="bg-gray-100 p-3 rounded">
                <p class="text-lg font-bold text-orange-500">
                    Ipad登录流程图
                </p>
        ![ipad.png](https://api.apifox.com/api/v1/projects/3475559/resources/589600/image-preview)

                
            </Column>
            <Column>
            <p class="text-lg font-bold text-orange-500">
                    Mac登录流程图
                </p>   
              ![mac.png](https://api.apifox.com/api/v1/projects/3475559/resources/589602/image-preview)
            </Column>
        </Columns>

        </Accordion>

        :::highlight green 

        ***温馨提示：***
        登录模块是最麻烦的必须步骤，若觉得过于繁琐，可省略步骤1与步骤2的登录步骤，直接在[后台在线登录](https://manager.geweapi.com/#/tool/wechat)获取appid调用接口。

        :::

      tags:
        - 基础API/登录模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                proxyIp:
                  type: string
                  description: 代理IP 格式：socks5://username:password@123.2.2.2
                  additionalProperties: false
                uuid:
                  type: string
                  description: 取码返回的uuid
                  additionalProperties: false
                captchCode:
                  type: string
                  description: 手机若提示需要输入验证码传输
                autoSliding:
                  type: boolean
                  description: >-
                    新设备自动验证true/false 

                    - ipad登录时：必须传false
                    ，会生成人脸滑块二维码，需[人脸识别app](https://app.qiweapi.com/)扫码进行人脸验证,扫描人脸通过后，再次调用本接口，然后手机点击确认，微信登陆成功。

                    -
                    Mac登录时：当参数传true时，服务会后台进行自动滑块验证，大概10s自动通过，无需下载App【90%通过率】，如果传false则会生成滑块二维码，需[下载滑块app](https://www.pgyer.com/secureandroid)扫码进行手动滑块验证。

                    -
                    当[获取二维码接口](http://doc.geweapi.com/api-139908278)使用网络方式3ttuid取码的时候，此参数必须传false。
              x-apifox-orders:
                - appId
                - uuid
                - autoSliding
                - proxyIp
                - captchCode
              required:
                - appId
                - uuid
            example:
              appId: '{{appid}}'
              proxyIp: ''
              uuid: obpAjgWNiBmumFz5VHmm
              autoSliding: false
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      uuid:
                        type: string
                        description: 二维码的uuid
                      headImgUrl:
                        type: string
                        description: 头像地址
                      nickName:
                        type: string
                        description: 昵称
                      expiredTime:
                        type: integer
                        description: 二维码超时时间
                      status:
                        type: integer
                        description: 状态 0：未扫码 1：已扫码未登录 2：登录成功
                      loginInfo:
                        type: object
                        properties:
                          uin:
                            type: integer
                            description: uin
                          wxid:
                            type: string
                            description: 微信ID，返回此值则是登录成功
                          nickName:
                            type: string
                            description: 昵称
                          mobile:
                            type: string
                            description: 绑定的手机号
                          alias:
                            type: string
                            description: 微信号
                        required:
                          - uin
                          - wxid
                          - nickName
                          - mobile
                          - alias
                        x-apifox-orders:
                          - uin
                          - wxid
                          - nickName
                          - mobile
                          - alias
                        description: 登录成功信息
                    required:
                      - uuid
                      - headImgUrl
                      - nickName
                      - expiredTime
                      - status
                      - loginInfo
                    description: 响应数据
                    x-apifox-orders:
                      - uuid
                      - headImgUrl
                      - nickName
                      - expiredTime
                      - status
                      - loginInfo
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/登录模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908279-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://api.geweapi.com
    description: 测试环境
security: []

```
## 响应示例

### 扫码但未点确认时的响应
```json
{
    "ret": 200,
    "msg": "操作成功",
    "data": {
        "uuid": "AZ0yN8d1wJmiNfQBKFgu",
        "headImgUrl": "http://wx.qlogo.cn/mmhead/ver_1/ZYUmcl1UNzyB2onM08Ij901TaUOLIjHj2UicK3XGDsjEWl4XgQN5IjodunHicBVsZiaZc1iaGCRfluAxkzyibbiau3WBfFj2nprzKp2KryicMjGIvDbWOQGmibwVK648a3o4A8hD/0",
        "nickName": "G",
        "expiredTime": 225,
        "status": 1,
        "loginInfo": null
    }
}
//需人脸/滑块 验证返回
{
    "ret": 200,
    "msg": "操作成功",
    "data": {
        "url": "http://api.asilu.com/qrcode/?t=http://182.40.96.72:8081/s/01KCJGKJ73YTBGQQKAZ4ZH13ZF"
    }
}
```

### 登录成功时的响应
```json
{
    "ret": 200,
    "msg": "操作成功",
    "data": {
        "uuid": "4YHmGvoXvgmS1MqWVtQ2",
        "headImgUrl": "http://wx.qlogo.cn/mmhead/ver_1/ZYUmcl1UNzyB2onM08Ij901TaUOLIjHj2UicK3XGDsjEWl4XgQN5IjodunHicBVsZiaZc1iaGCRfluAxkzyibbiau3WBfFj2nprzKp2KryicMjGIvDbWOQGmibwVK648a3o4A8hD/0",
        "nickName": "G",
        "expiredTime": 230,
        "status": 2,
        "loginInfo": {
            "uin": 4077276085,
            "wxid": "wxid_0xsqb3o0tsvz22",
            "nickName": "G",
            "mobile": "17114312382",
            "alias": null
        }
    }
}
```
