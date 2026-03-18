# Android 手机收集配置指南（HTTP Shortcuts）

通过 Android 上的开源应用「HTTP Shortcuts」，可以在任意 App 的分享面板中一键将内容发送到 Collector。

## 第一步：安装 HTTP Shortcuts

在以下任一渠道安装：
- Google Play 搜索「HTTP Shortcuts」（开发者：Roland Meyer）
- 国内应用商店搜索「HTTP Shortcuts」或「HTTP 快捷方式」
- GitHub 开源地址：https://github.com/Waboodoo/HTTP-Shortcuts

## 第二步：确认网络环境

- 手机和电脑连接同一个 WiFi
- 查看电脑的局域网 IP（Windows 下在 CMD 中运行 `ipconfig`，找到 IPv4 地址，如 `192.168.1.100`）
- 确认 Collector 服务已启动（默认端口 `8000`）

## 第三步：创建快捷方式

1. 打开 HTTP Shortcuts App
2. 点击右下角 `+` 按钮 → 选择「Regular Shortcut」
3. 按以下内容配置：

### 基本设置（Basic Request Settings）

- **Shortcut Name**：`Save to Collector`
- **Method**：`POST`
- **URL**：`http://192.168.1.100:8000/api/collect`（替换为你电脑的实际 IP）

### 请求体（Request Body）

- **Request Body Type**：选择 `Custom Text`
- **Content Type**：`application/json`
- **Body Content** 填写：

```
{"content": "{content}"}
```

> 注意：这里的 `{content}` 不是占位符文字，而是 HTTP Shortcuts 的内置变量，代表分享传入的文本。如果 App 不支持这个写法，参见下面的「使用变量」方式。

### 使用变量（如果上面的方式不生效）

1. 回到 App 主界面，点击右上角菜单 → 「Variables」
2. 创建一个新变量：
   - **Type**：选择「Share text / Share URL」
   - **Variable Name**：`shared`
3. 回到快捷方式编辑，Request Body 改为：

```
{"content": "{shared}"}
```

### 触发方式（Trigger）

- 点击快捷方式的设置图标
- 找到「Trigger from share menu」或「Accept as share target」
- **开启**此选项

### 响应处理（Response）

- 可以选择「Show toast with response」，这样收集成功后会弹出提示

4. 点击右上角保存

## 使用方法

1. 在任意 App（微信、小红书、知乎、B站等）中点击「分享」
2. 在分享面板中找到「HTTP Shortcuts」或直接找到「Save to Collector」
3. 点击即可完成收集

> 首次使用时，分享面板可能不会直接显示。需要滑到末尾点「更多」，然后在列表中启用 HTTP Shortcuts。小米手机也可以在「设置 → 应用设置 → 应用管理 → HTTP Shortcuts → 应用详情」中确认分享相关权限已开启。

## 故障排查

- **请求超时 / 无法连接**：确认手机和电脑在同一 WiFi，检查 IP 是否正确，确认电脑防火墙放行了 8000 端口
- **Collector 服务没启动**：在电脑上运行 `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **分享面板找不到**：进入 HTTP Shortcuts 的快捷方式设置，确认「share trigger」已开启
- **小米手机权限问题**：在系统设置中给 HTTP Shortcuts 开启「显示在其他应用上层」和「后台弹出界面」权限
