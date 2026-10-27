# 全局 CLI（imgbed）

`tools/imgbed` 把图床能力带出仓库目录 —— 在**任何项目**里上传图片，直接拿到链接。

## 安装（一次性）

```bash
git clone https://github.com/webkubor/free-imgbed.git
cd free-imgbed
tools/imgbed install        # 软链到 ~/.local/bin
imgbed init <你的fork仓库地址>   # 登记仓库（默认克隆本模板仓）
```

## 日常使用

```bash
imgbed push banner.png my-project/   # 压缩 → 提交 → 推送 → 打印直链
imgbed push banner.png my-project/ --no-push   # 只提交到本地，稍后手动推
imgbed link my-project/banner.webp   # 查已有文件的直链
```

`push` 完整流程：调用图床仓的 `tools/add.sh`（缩放/压缩/红线检查）→ 只暂存目标文件与 INDEX.md → commit → push → 打印 `🔗 https://...`。

## 多仓切换

```bash
FREE_IMGBED_REPO=/path/to/another-imgbed imgbed push x.png dir/
# 或改写 ~/.config/free-imgbed/repo.conf 的 REPO= 行
```
