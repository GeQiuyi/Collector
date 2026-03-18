# Collector 部署准备清单

部署到 ai-builders.space 前的自检清单。按顺序完成每一项。

---

## 一、GitHub 仓库准备

- [ ] **1.1** 项目已推送到 GitHub，且为**公开仓库**（私有仓库无法部署）
- [ ] **1.2** 所有待部署的代码已 `git add`、`git commit`、`git push`
- [ ] **1.3** 未将敏感信息提交到仓库（`.env`、API Key、密码等）
- [ ] **1.4** `.gitignore` 已包含：`collector.db`、`.env`、`deploy-config.json`

---

## 二、Dockerfile 检查

- [ ] **2.1** 项目根目录存在 `Dockerfile`
- [ ] **2.2** Dockerfile 使用 `python:3.11-slim` 或兼容的 base 镜像
- [ ] **2.3** `CMD` 使用 shell 形式：`CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"`
- [ ] **2.4** 未硬编码端口（必须使用 `${PORT:-8000}`）
- [ ] **2.5** （可选）本地测试构建：`docker build -t collector .` 能成功

---

## 三、应用配置检查

- [ ] **3.1** 应用从单进程、单端口对外提供服务（API + 静态文件均由 uvicorn 提供）
- [ ] **3.2** 无后台 worker、无多进程、无额外 Web 服务
- [ ] **3.3** SQLite 数据库路径可写（默认 `./collector.db` 在容器内可用）
- [ ] **3.4** 依赖已全部写入 `requirements.txt`，无本地未记录依赖

---

## 四、部署配置

- [ ] **4.1** 复制 `deploy-config.example.json` 为 `deploy-config.json`（不要提交到 Git）
- [ ] **4.2** 填写 `repo_url`：你的 GitHub 仓库地址，如 `https://github.com/username/collector`
- [ ] **4.3** 填写 `service_name`：唯一服务名，将作为子域名，如 `collector` → `https://collector.ai-builders.space`
- [ ] **4.4** 填写 `branch`：要部署的分支，如 `main` 或 `master`
- [ ] **4.5** （可选）如需环境变量，在 `env_vars` 中配置，最多 20 个，键名需大写

---

## 五、MCP 与认证

- [ ] **5.1** `mcp.json` 中已配置 `AI_BUILDER_TOKEN`（替换 `sk_live_your_token_here`）
- [ ] **5.2** Token 有效且未过期

---

## 六、执行部署

部署由 AI 助手调用 Space API 完成，需要你提供：

| 信息       | 示例                     |
|------------|--------------------------|
| 仓库 URL   | `https://github.com/xxx/collector` |
| 服务名     | `collector`              |
| 分支       | `main`                   |

准备好后，对 AI 说：**「请帮我部署 Collector」**，并按要求提供上述信息。

---

## 七、部署后

- [ ] **7.1** 等待 5–10 分钟完成首次部署
- [ ] **7.2** 访问 `https://{service_name}.ai-builders.space` 验证
- [ ] **7.3** 后续修改代码：先 `git push`，再重新触发部署（调用 `POST /v1/deployments`）

---

## 常见问题

**Q: 部署失败怎么办？**  
A: 使用 `GET /v1/deployments/{service_name}/logs` 查看构建和运行日志，排查错误。

**Q: 数据会丢失吗？**  
A: 使用 SQLite 时，容器重启可能导致数据丢失。如需持久化，可考虑后续接入云数据库。

**Q: 免费时长多久？**  
A: 首次成功部署后约 12 个月免费托管。
