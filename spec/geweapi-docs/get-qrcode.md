# 获取登录二维码(步骤1)

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/login/getLoginQrCode:
    post:
      summary: 获取登录二维码(步骤1)
      deprecated: false
      description: >-
        -
        appId参数为设备ID，首次登录传空，会自动触发创建设备，掉线后重新登录则必须传接口返回的appId，注意**同一个号避免重复创建设备**，以免触发官方风控

        - 响应结果中的qrImgBase64为微信二维码图片的base64，前端需要将二维码图片展示给用户并进行手机扫码操作（PS:
        **扫码后调用[执行登录接口](https://doc.geweapi.com/api-139908279)**，手机上才**显示登录**）。

        - ***如果使用手机微信扫码显示 “在新设备完成验证以继续登录”
        则需要进行二次处理，具体可以看[执行登录接口](https://doc.geweapi.com/api-139908279)***

        - 取码时传的appId需要与上次登录扫码的微信一致，否则会导致登录失败

        :::highlight green 

        ***温馨提示：***
        登录模块是最麻烦的必须步骤，若觉得过于繁琐，可省略步骤1与步骤2的登录步骤，直接在[后台在线登录](https://manager.geweapi.com/#/tool/wechat)获取appid调用接口。

        :::
      tags:
        - 基础API/登录模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: PS：进入后台系统-点击Token中心-生成Token
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
                  description: 设备ID，首次登录传空，之后传接口返回的appId
                  additionalProperties: false
                proxyIp:
                  type: string
                  description: '- 网络方式2：自定义代理IP 格式：socks5://username:password@123.2.2.2:8932'
                  additionalProperties: false
                regionId:
                  type: string
                  description: >-
                    -
                    网络方式1：平台内置登陆地区ID，登录时请选择最近的地区，若目前支持的regionId中没有您所在的地区，可以自行采购socks5协议代理IP，填写到proxyIp参数中。

                    - 地区id对照表

                    110000：北京市 | 120000：天津市 | 130000：河北省 | 140000：山西省 |
                    210000：辽宁省 |

                    220000：吉林省 | 230000：黑龙江省 |310000：上海市 | 320000 ：江苏省 |
                    330000：浙江省 | 

                    340000：安徽省 | 350000：福建省 | 360000：江西省 | 370000：山东省 |
                    410000：河南省 |

                    420000：湖北省 | 430000：湖南省 | 440000：广东省 | 450000：广西省 |
                    460000：海南省 |

                    500000：重庆市 | 510000：四川省 | 520000：贵州省 |  530000：云南省 | 
                    540000：西藏 | 

                    610000：陕西省 | 620000：甘肃省 | 630000：青海省 | 640000：宁夏 |
                    150000：内蒙古 |
                     650000：新疆 |
                  additionalProperties: false
                type:
                  type: string
                  description: 设备类型：ipad（推荐），mac
                ttuid:
                  type: string
                  title: 代理id
                  description: >-
                    -
                    [代理id下载地址](https://cos.geweapi.com/ttuid/%E4%BB%A3%E7%90%86id-%E6%96%B0.zip)，需配合
                    regionId/proxyIp 联合使用，不能单独使用。使用后可以临时借用用户的本地网络进行取码，网络环境比方式1纯净
                aid:
                  type: string
                  title: aid
                  description: >-
                    -
                    网络方式3：[aid下载地址](https://download-1308498490.cos.ap-guangzhou.myqcloud.com/%E6%9C%AC%E5%9C%B0%E4%BB%A3%E7%90%86%E5%AE%A2%E6%88%B7%E7%AB%AF-%E6%96%B0.zip)，aid指的本地电脑代理,需要客户在本地电脑上运行aid程序,微信登录期间，Aid工具必须保证正常在线运行，网络环境最纯净的方式
              x-apifox-orders:
                - appId
                - type
                - regionId
                - proxyIp
                - ttuid
                - aid
              required:
                - appId
                - type
                - regionId
            example:
              appId: ''
              proxyIp: ''
              regionId: '320000'
              type: mac
              aid: ''
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
                      qrData:
                        type: string
                        description: 二维码内包含的信息（可用二维码生成工具结合值生成可扫描的微信二维码）
                      qrImgBase64:
                        type: string
                        description: 二维码图片base64
                      uuid:
                        type: string
                        description: 二维码的uuid
                      appId:
                        type: string
                        description: 登录设备ID
                    required:
                      - qrData
                      - qrImgBase64
                      - uuid
                      - appId
                    description: 响应数据
                    x-apifox-orders:
                      - qrData
                      - appId
                      - qrImgBase64
                      - uuid
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
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908278-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://api.geweapi.com
    description: 测试环境
security: []

```
## 响应示例

```json
{
    "ret": 200,
    "msg": "操作成功",
    "data": {
        "appId": "wx_wR_U4zPj2M_OTS3BCyoE4",
        "qrData": "http://weixin.qq.com/x/4dmHZZMtoLbHoLZwd1wE",
        "qrImgBase64": "data:image/jpg;base64,/9j/...",
        "uuid": "4dmHZZMtoLbHoLZwd1wE"
    }
}
```
