# 自定义域名绑定

把文档站 / 图床入口绑到自己的域名（例：`imgbed.webkubor.online`）。整条链路 = **GitHub Pages（托管）+ Cloudflare DNS（解析）**。

## 1. GitHub 侧（本仓已配好）

- 仓库 Settings → Pages → Build and deployment → Source 选 **GitHub Actions**（本仓 workflow `deploy-docs` 自动构建 `docs/`）
- Custom domain 填 `imgbed.webkubor.online`，等 DNS 校验通过后勾选 **Enforce HTTPS**

API 方式（等价）：

```bash
gh api repos/<你>/<仓>/pages -X POST -f build_type=workflow
gh api repos/<你>/<仓>/pages -X PUT -f cname=imgbed.你的域名.com -F https_enforced=true
```

## 2. Cloudflare 侧（需要你的账号权限）

在域名所在 Zone 添加一条记录：

| 类型 | 名称 | 内容 | 代理状态 |
|---|---|---|---|
| CNAME | `imgbed` | `webkubor.github.io`（或 `<你的GitHub用户名>.github.io`） | 仅 DNS（先灰云，HTTPS 证书签发后再开橙云） |

::: warning 顺序很重要
先灰云让 GitHub 签发证书（几分钟），Enforce HTTPS 成功后再开橙云代理，否则容易 526/重定向循环。
:::

## 3. 验证

```bash
curl -sI https://imgbed.webkubor.online/
curl -sI https://imgbed.webkubor.online/free-imgbed/logo.svg
```

本仓域名目前由 Cloudflare 代理，HTTPS 图片请求已实测可用；文档首页偶发超时，稳定性仍需观察。GitHub Pages 的 `https_enforced` 仍为 `false`，因此 HTTP 链接不会自动跳转；对外请直接引用 `https://`，关键 README 图片优先用 jsDelivr HTTPS。

## 自动化（Agent/Skill）

有 `CLOUDFLARE_API_TOKEN`（Zone:DNS:Edit 权限）时，以上 DNS 可一条 API 搞定：

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"imgbed","content":"webkubor.github.io","proxied":false}'
```

本机已沉淀为技能「CF 自定义域名绑定」，直接对 agent 说「给 xx 绑定域名 yy」即可。
