"""Prototype: interpret a research paper with paper-tuned prompts.

Validation run for the papers feature. Reuses the existing three-stage engine
(podlens.interpreter._generate) but swaps in paper-shaped prompts. Output is
Chinese so the (non-academic, ESL) reader can judge fidelity and plainness;
every anchor quotes the EXACT ENGLISH source so it is findable in the PDF.

This is a one-off under scripts/ on purpose: the prompt design must be validated
before it is folded into podlens/prompts.py and the publish path. Nothing here
publishes or pushes; the full report (incl. the private personal-mapping layer)
is written to reports/ (gitignored, local only).

Usage:
    .venv/bin/python scripts/paper_interpret.py "论文/The Era of Experience Paper.pdf"
"""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import _generate, _make_client, _parse_json_obj
from podlens.papers import load_paper, quote_is_present
from podlens.profile import load_profile

_T_RECON, _T_PLAIN, _T_MAP, _T_META = 0.2, 0.5, 0.6, 0.2

# Anchor rule shared by every stage: quotes must be the EXACT English source so
# the reader can search them in the PDF (this is PodLens's "traceable to source"
# promise applied to papers, replacing the podcast timestamp).
_ANCHOR_RULE = (
    "锚点规则(关键):每一处证据锚点都要给出「章节名 · \"英文原文短引用\"」。"
    "引用必须是论文里一字不差的英文原文(5-12 个单词),即使你的解读是中文,"
    "引用也保持英文原文不翻译——这样读者能直接在 PDF 里检索到那句话。"
    "若要标一整段,用「该段开头三个词 … 该段结尾三个词」的形式。不要编造或改写引用。"
)

_FIDELITY = (
    "忠实规则:只依据下面给出的论文原文,不臆造事实、数据、结论或文中没有的说法。"
    "把论文实际说的,与你自己的推断,清楚分开。人名、机构名、专有名词一律保留英文原形,"
    "不要音译成中文。不堆砌口号和励志填充。除了要求的 Markdown 章节,不要写任何开场白或结语。"
    "用简体中文输出;正文不要夹杂未翻译的普通英文词(专有名词和上述英文引用除外)。"
)


def stage1_reconstruction(paper: str) -> str:
    return (
        "你是一位严谨的研究者,正在为一篇学术论文做忠实还原。这是「保真层」:"
        "低解读、高忠实。先不要用大白话解释,也先不要做个人联系。\n\n"
        + _FIDELITY + "\n\n" + _ANCHOR_RULE + "\n\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变:\n\n"
        "## 这篇论文讲了什么\n"
        "几句话忠实概述:论文的主题、作者、它要回答的核心问题、它的中心主张、"
        "以及整体论证脉络。像高质量的读书笔记,不带个人解读。\n\n"
        "## 论文骨架\n"
        "拆出这篇论文的结构,逐条说明(每条尽量带锚点):它在解决什么问题;"
        "核心主张是什么;用什么方式来论证(实验/推理/案例/类比等,position paper 就说明它的论证链);"
        "拿出了哪些证据或例子;它自己承认的边界或局限在哪。\n\n"
        "## 核心论点清单\n"
        "编号列出这篇论文最关键的论点(把紧密相关的合并成一条,别把一个意思拆成多条;"
        "一般 6-10 条)。每一条给出:\n"
        "- 论点本身(忠实陈述)\n"
        "- 锚点(章节 · 英文原文短引用)\n"
        "- 类型,取其一:事实 / 主张 / 例子 / 预测 / 定义 / 反驳\n"
        "- 若有,作者表达的不确定或保留(一行)\n\n"
        "论文原文:\n\"\"\"\n" + paper + "\n\"\"\"\n"
    )


def stage2_plain(paper: str, reconstruction: str) -> str:
    return (
        "你现在有了一篇论文的忠实还原(见下),以及论文原文。你的任务是「大白话层」:"
        "像一个聪明而诚实的朋友坐在读者旁边,把门槛降下来,但不简化掉内容、也不偏离原文。"
        "读者几乎没读过论文、且英文吃力,所以你要特别照顾零基础的人。\n\n"
        + _FIDELITY + "\n\n" + _ANCHOR_RULE + "\n\n"
        "这一层的额外要求:\n"
        "- 把术语翻成日常语言,必要时用贴切的比喻(但不能歪曲)。\n"
        "- 把复杂推理压成清晰的因果链。\n"
        "- 遇到反直觉的地方,直说它为什么反直觉。\n"
        "- 保留原文的论证顺序,不要重排逻辑。\n"
        "- 不要寒暄,不要对读者打招呼,直接进入内容。\n\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变:\n\n"
        "## 大白话重讲\n"
        "先用一两句点出「这篇在跟什么较劲、为什么值得在意」,再顺着论文把它讲清楚。"
        "是流动的重述,不是要点罗列,可以有声音和节奏,但每一步都贴着论文的真实内容。\n\n"
        "## 术语小词典\n"
        "挑出 5-10 个理解这篇论文绕不开的关键术语,每个用一句人话解释清楚,并带上锚点"
        "(它在论文哪里被用到)。这是给零基础读者的脚手架。\n\n"
        "## 这篇之前与之后\n"
        "帮没有领域背景的读者把这篇放回它所在的脉络:在这篇之前,这个领域大体默认/相信什么;"
        "这篇主张改变或挑战了什么。两段话即可,带锚点。\n\n"
        "## 最值得读原文的几段\n"
        "指出 3-5 处最值得读者亲自去读英文原文的地方:给出锚点,并说明为什么值得"
        "(信息密度高、是论证的关键转折、或措辞本身重要)。\n\n"
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n\n"
        "论文原文(用于核对与引用):\n\"\"\"\n" + paper + "\n\"\"\"\n"
    )


def stage3_mapping(reconstruction: str, plain: str, profile: str | None) -> str:
    if profile:
        profile_block = (
            "读者提供了个人档案,描述他长期的兴趣、当前的项目、写作方向和已有的看法。"
            "只用它来写「个人映射」一节。不要奉承;若这篇论文和档案里的东西没有真实关联,"
            "就不要硬扯。\n\n读者档案:\n\"\"\"\n" + profile + "\n\"\"\"\n"
        )
        mapping_section = (
            "## 个人映射\n"
            "把这篇论文连接到这位具体的读者(依据他的档案)。可涵盖:它和他长期兴趣的关系;"
            "和他当前项目的关系;可能如何进入他的写作或产品思考;哪些想法可作为可复用的概念工具;"
            "哪些想法挑战或更新了他已有的看法;哪里印证了他已经相信的东西。\n"
            "关键:每一条映射都必须回指论文证据,带上锚点(章节 · 英文原文引用)。"
            "锚不住的洞察就删掉,不要悬空。\n\n"
        )
    else:
        profile_block = "读者没有提供个人档案。跳过「个人映射」一节,只产出证据锚定洞察、值得收藏的概念、待追踪的问题。\n"
        mapping_section = ""

    body = (
        "你现在有了一篇论文的忠实还原和大白话重讲(见下)。这是最后一层,只在前面已核验的层之上运行。"
        "你的任务:提炼有证据支撑的洞察;若有档案,则把论文映射到这位具体读者。\n\n"
        + _FIDELITY + "\n\n" + _ANCHOR_RULE + "\n\n" + profile_block + "\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变"
        + ("(包含「个人映射」):" if profile else "(无档案,跳过「个人映射」):") + "\n\n"
        "## 证据锚定洞察\n"
        "列出这篇论文最重要的几条洞察。每条给出:洞察本身;一行大白话解释;支撑的锚点"
        "(章节 · 英文原文引用);置信度 高/中/低;以及它是 明确陈述 / 推断 / 猜测。\n\n"
        + mapping_section +
        "## 值得收藏的概念\n"
        "几个值得收进个人知识体系的概念、框架或心智模型,每个一行描述加锚点。\n\n"
        "## 待追踪的问题\n"
        "论文提出但未解决、或值得后续跟进的开放问题与线索。\n\n"
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n\n"
        "大白话重讲:\n\"\"\"\n" + plain + "\n\"\"\"\n"
    )
    return body


def stage_meta(reconstruction: str) -> str:
    return (
        "从下面的忠实还原中,产出一个标题和 3-6 个具体的主题标签。\n"
        "标题格式:一个精炼的主题短语,然后 \" · \",然后第一作者的英文原名"
        "(例:\"经验时代:超越人类数据的强化学习 · David Silver\")。人名保留英文原形,不要音译。\n"
        "标签:3-6 个论文真正讨论的具体概念/术语(中文),每个 2-6 字,不要标点,不要写宽泛学科名。\n"
        "只返回一个 JSON 对象,例如:"
        '{"title": "主题短语 · David Silver", "tags": ["经验流", "奖励接地", "世界模型"]}\n\n'
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n"
    )


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else "论文/The Era of Experience Paper.pdf"
    config = load_config()
    if not config.has_api_key:
        print("未配置 GEMINI_API_KEY。"); return 1

    print(f"[1/5] 读取并清洗论文: {src}")
    paper = load_paper(src)
    print(f"      抽取 {len(paper)} 字")

    profile = load_profile(config.profile_path)
    print(f"      个人档案: {'已加载,会做个人映射' if profile else '无,跳过个人映射'}")

    client = _make_client(config)  # noqa: F841 (kept for parity / future per-stage)

    print(f"[2/5] 忠实还原  (model={config.model})")
    recon = _generate(client, config.model, stage1_reconstruction(paper), _T_RECON)

    print("[3/5] 大白话重讲 + 术语词典 + 前后脉络")
    plain = _generate(client, config.model, stage2_plain(paper, recon), _T_PLAIN)

    print("[4/5] 证据锚定洞察 + 个人映射")
    mapping = _generate(client, config.model, stage3_mapping(recon, plain, profile), _T_MAP)

    print("[5/5] 标题与标签")
    meta = _parse_json_obj(_generate(client, config.model, stage_meta(recon), _T_META))
    title = str(meta.get("title", "")).strip() or "论文解读"
    tags = [str(t).strip() for t in meta.get("tags", []) if str(t).strip()][:6]

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = (
        f"# {title}\n\n> PodLens 论文解读原型 · 模型 {config.model} · {stamp}\n"
        f"> 标签:{', '.join(tags)}\n\n"
        f"{recon.strip()}\n\n{plain.strip()}\n\n{mapping.strip()}\n"
    )

    # Save the FULL report (incl. private mapping) locally; reports/ is gitignored.
    out = ROOT / "reports" / "PROTOTYPE-era-of-experience.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report, encoding="utf-8")

    # Traceability safety net: how many quoted anchors actually occur in the PDF?
    import re
    quotes = re.findall(r'"([^"]{8,})"', report) + re.findall(r'“([^”]{8,})”', report)
    eng = [q for q in quotes if re.search(r"[A-Za-z]", q)]
    ok = sum(1 for q in eng if quote_is_present(q, paper))
    print("\n================ 结果 ================")
    print(f"标题: {title}")
    print(f"标签: {', '.join(tags)}")
    print(f"完整报告已保存(含私人层,本地不上线): {out}")
    if eng:
        print(f"锚点可追溯性: {ok}/{len(eng)} 条英文引用能在 PDF 原文中检索到 "
              f"({100*ok//max(len(eng),1)}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
