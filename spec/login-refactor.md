# 登录接口重构需求文档

## 需求描述
根据最新登录接口文档（获取二维码/执行登录），当前客户端实现与接口参数和响应形态不一致，需要对登录流程进行兼容性重构与文档同步。

## 需求目标
- 支持新的取码与登录参数（type、regionId、autoSliding 等）。
- 仅面向最新接口格式，不考虑旧版兼容。
- 按最新响应示例处理（qrData、data.url、loginInfo 可能为空）。
- 登录流程可处理人脸/滑块二次验证提示。
- 更新示例与说明，保证使用方知道必填参数与返回结构。
- 仅支持 iPad 登录方式，默认类型为 ipad，传入其他类型需报错。
- 二维码展示仅使用 qrData（不使用 qrImgBase64）。

## 技术方案（可选）
- 扩展 `LoginApi.get_qr`/`check_qr` 方法签名并向上透传到 `GewechatClient`。
- 登录流程先判断 `data.url` 分支，再处理标准 `status/expiredTime/loginInfo` 结构。
- 二维码展示使用 `qrData`，不处理 `qrImgBase64`。
- 登录成功后返回或暴露 `loginInfo` 以便上层保存 `appId ↔ wxid`。
- 强制校验登录类型仅允许 `ipad`，其他类型直接报错。

## 待讨论事项（可选）
- `login()` 的返回结构是否升级为包含 `loginInfo`。
- `autoSliding` 默认值策略（仅 iPad 场景）。
