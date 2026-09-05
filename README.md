# PodLens

中文 · [English](./README.en.md)

PodLens 是一个基于原始文本做解读、编辑与发布的本地工作空间，处理播客、视频和论文。

**线上站点：** [lens.lumihelia.com](https://lens.lumihelia.com) ·  
**RSS：** [English](https://lens.lumihelia.com/feed.xml) / [中文](https://lens.lumihelia.com/zh/feed.xml) ·  
**JSON Feed：** [episodes.json](https://lens.lumihelia.com/episodes.json)

PodLens 有一条贯穿整个流程的硬规则：

> 先忠实还原，再用大白话讲清楚，最后进入个人映射。每条洞察都要能够回到来源。

仓库同时包含命令行解读 pipeline 和本地 editorial workbench。Workbench 是当前主要的发布入口：完整报告先留在本地审阅，公开层可以继续编辑，跨内容关联也会在发布前进入人工检查，确认之后再生成中英文静态页面。

## 解读模型

PodLens 将解读分成三个有来源约束的阶段：

1. **忠实还原**：整理主题、核心问题、时间顺序、可回查的论点与论点类型。
2. **大白话重述**：把因果关系讲清楚，寻找有帮助的比喻，也标出值得重新回看的时刻。
3. **证据锚定洞察与个人映射**：给洞察标注置信度，并与本地 `profile.md` 中的个人背景建立连接。

公开网站只接收前两层。个人映射层与完整报告保留在本地，其中完整报告存放于被 Git 忽略的 `reports/` 目录。

目前支持的输入包括：

- YouTube 链接，通过字幕轨获取文本，不下载视频本体
- `.srt`、`.vtt`、`.txt`、`.md` 字幕或文本
- `.pdf`、`.txt`、`.md` 论文
- 通过标准输入 pipe 进入 CLI 的文本

## 本地 Workbench

Workbench 承担从解读到发布之间的编辑交接：

- 在播客 / 视频与论文解读之间切换
- 上传源文件，或提供 YouTube / 来源链接
- 分开审阅完整私有报告与拟公开内容
- 发布前编辑标题、标签、来源链接与公开 Markdown
- 检查与既有播客、视频和论文之间的证据关联
- 删除不合适的关联建议
- 管理已经发布的内容，并加入署名为 `From Helia` 的编辑备注
- 编辑个人映射阶段使用的本地背景
- 生成配对的英文与中文发布树
- 将生成的公开文件提交并推送到 GitHub Pages

macOS 上可以直接双击 `start_ui.command`，也可以从 Terminal 启动：

```bash
./start_ui.command
```

启动脚本会安装当前依赖，在 `http://127.0.0.1:8765` 启动本地服务并打开浏览器。Workbench 运行期间需要保留对应的 Terminal 窗口，`Ctrl-C` 用于停止服务。

Workbench 中的发布会执行真实 Git 操作。确认发布后，流程会：

1. 将公开静态内容写入 `docs/`。
2. 更新 `.podlens/` 中可继续编辑的发布源文件。
3. 只提交这两个路径，并排除 `.DS_Store`。
4. 将 commit 直接 push 到 `origin/main`。

其他已经 staged 的路径不会被带入这次发布 commit。当前工作流面向单一维护者仓库，`main` 中的 `docs/` 通过 GitHub Pages 部署。

## 安装

```bash
bash setup.sh
```

脚本会创建 `.venv`、安装依赖，并在本地还不存在对应文件时，根据 example 创建 `.env` 与 `profile.md`。

在 `.env` 中选择一个 provider：

```env
# gemini or deepseek
PODLENS_PROVIDER=gemini

GEMINI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here

# 可选。留空时使用所选 provider 的默认模型。
PODLENS_MODEL=
```

当前默认模型：

- Gemini：`gemini-2.5-pro`
- DeepSeek：`deepseek-chat`

实际只会读取当前 provider 对应的 API key。`profile.md`、`.env`、完整报告、字幕与源论文都被 Git 忽略。

## CLI

先进入虚拟环境：

```bash
source .venv/bin/activate
```

常用命令：

```bash
# 解读 YouTube 视频
python -m podlens "https://youtu.be/VIDEO_ID"

# 解读本地 transcript
python -m podlens examples/sample_transcript.txt

# 保存完整报告
python -m podlens my_transcript.srt -o report.md

# 从剪贴板 pipe 文本
pbpaste | python -m podlens -

# 跳过个人映射
python -m podlens my_transcript.txt --no-profile

# 指定英文解读输出
python -m podlens my_transcript.txt --lang en

# 不调用 API，只检查完整 prompt pipeline
python -m podlens examples/sample_transcript.txt --dry-run
```

字幕文件目前是更稳定的播客 / 视频输入，因为时间戳可以保留，也能绕开部分 YouTube bot check。字幕抓取被阻挡时，`yt-dlp` 可以复用现有浏览器 session：

```env
PODLENS_COOKIES_FROM_BROWSER=chrome
PODLENS_SUB_LANGS=zh.*,en.*,.*
```

## Provider 与长文本

Gemini 与 DeepSeek 通过 `podlens/interpreter.py` 中同一层 provider boundary 接入解读流程。

面对较长的播客 transcript，DeepSeek 会通过 `podlens/chunking.py` 按 transcript 行边界拆分第一、二阶段，分别解读后再合并结果。第三阶段与论文解读使用已经压缩过的中间结果，目前不做 chunking。Gemini 保持 single-call 路径。

Chunking 会增加调用次数，也可能损失一部分跨 segment 的关联。DeepSeek 生成的姓名、机构、翻译与跨内容连接尤其适合在发布前完整读一遍。

## 双语发布

公开网站当前以英文为主：

- English：`/`、`/episodes/`、`/papers/`、`/feed.xml`
- 中文：`/zh/`、`/zh/episodes/`、`/zh/papers/`、`/zh/feed.xml`

两种语言通过页面内的语言切换与 `hreflang` 连接。历史 `/en/...` HTML 页面会跳转到英文根路径；部分已经改名或合并的旧 episode URL 也保留兼容跳转，避免既有链接直接失效。

CLI 发布命令：

```bash
# 解读并发布
python -m podlens "Episode.srt" --title "My Episode" --publish

# 使用已有报告发布，不再重新调用解读 API
python -m podlens --publish-existing report.md --title "My Episode"

# 根据 manifest 重建 index、feed 与 sitemap
python -m podlens --rebuild-site
```

`PODLENS_PRIVATE_CUTOFF` 定义报告从哪个标题开始进入私有层。静态文件写入前，该标题及其后内容都会被移除。

## GitHub Pages 部署

仓库使用 `main` 分支中的 `/docs` 部署 GitHub Pages，`docs/CNAME` 当前指向 `lens.lumihelia.com`。

```text
在本地 workbench 审阅
    -> 生成 docs/ 与 .podlens/
    -> scoped Git commit
    -> push origin/main
    -> GitHub Pages build
    -> lens.lumihelia.com
```

Workbench 会分别报告 Git commit 与 push 失败。Push 成功表示内容已经进入远端仓库，Pages build 仍需要继续完成，公开页面与 feed 之后还需要做一次部署验证。

## 验证

离线验证命令：

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q podlens webui
python3 -m podlens examples/sample_transcript.txt --dry-run
git diff --check
```

当前测试覆盖 provider 默认值、transcript chunking、发布 commit 范围、XML 解析、双语路由、来源 URL、历史跳转与公开层隐私标题。真实模型调用、翻译、Git push 与 Pages 部署仍然需要单独做 live verification。

## 当前边界

- 还没有音频文件转录能力，也没有 podcast RSS ingestion。
- YouTube 字幕抓取会受到 bot check 与 rate limit 影响。
- PDF 文字抽取效果取决于论文排版；复杂 PDF 可以先转换为 `.txt` 或 `.md`。
- DeepSeek chunking 可以降低上下文压力，发布前的编辑审阅仍然必要。
- Workbench 是本地单用户工具，目前不是 hosted multi-user CMS。

## 仓库结构

- `podlens/`：解读、provider、发布与来源处理逻辑
- `webui/`：本地 editorial workbench
- `.podlens/episodes/`：可继续编辑的双语发布源文件
- `docs/`：生成后的 GitHub Pages 静态站
- `scripts/`：一次性发布与维护脚本
- `tests/`：离线 regression tests

## License

[MIT](LICENSE)
