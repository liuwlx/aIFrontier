# -*- coding: utf-8 -*-
import json
import os
import re
from html.parser import HTMLParser
from html import unescape

OUTPUT_DIR = r'E:\workerspace\daily\frontier-data-hub\data\agent-readings\2026\06'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, '2026-06-04.article-reader-agent.jsonl')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_text_from_html(html_content):
    """Extract readable text from HTML."""
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text_parts = []
            self.skip_tags = {'script', 'style', 'noscript', 'nav', 'footer', 'header', 'aside', 'svg', 'path'}
            self.in_skip = 0

        def handle_starttag(self, tag, attrs):
            tag_lower = tag.lower()
            if tag_lower in self.skip_tags:
                self.in_skip += 1

        def handle_endtag(self, tag):
            tag_lower = tag.lower()
            if tag_lower in self.skip_tags:
                self.in_skip -= 1
            if tag_lower in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br', 'tr', 'blockquote'):
                if not self.in_skip:
                    self.text_parts.append('\n')

        def handle_data(self, data):
            if not self.in_skip:
                text = data.strip()
                if text:
                    self.text_parts.append(text + ' ')

    extractor = TextExtractor()
    try:
        extractor.feed(html_content)
    except Exception:
        pass
    result = ''.join(extractor.text_parts)
    result = re.sub(r' \n ', '\n', result)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = unescape(result).strip()
    lines = [line.strip() for line in result.split('\n')]
    lines = [line for line in lines if line and len(line) > 2]
    return '\n'.join(lines)


# ============================================================
# Define article results
# ============================================================

articles = []

# ---- Article 1: Anthropic Research landing page (blocked) ----
articles.append({
    "source_url": "https://www.anthropic.com/research",
    "title": "Research",
    "reader_status": "blocked",
    "reader_agent": "Article Reader Agent",
    "article_summary": "",
    "why_it_matters": "",
    "action_hint": "",
    "key_points": [],
    "evidence_quotes": [],
    "reading_quality": "low",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 2: Economic Futures landing page (blocked) ----
articles.append({
    "source_url": "https://www.anthropic.com/economic-futures",
    "title": "Economic Futures",
    "reader_status": "blocked",
    "reader_agent": "Article Reader Agent",
    "article_summary": "",
    "why_it_matters": "",
    "action_hint": "",
    "key_points": [],
    "evidence_quotes": [],
    "reading_quality": "low",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 3: Introducing the Services Track and Partner Hub ----
articles.append({
    "source_url": "https://www.anthropic.com/news/services-track-partner-hub",
    "title": "Introducing the Services Track and Partner Hub of the Claude Partner Network",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic于2026年6月3日宣布推出Claude合作网络的两项新组件：服务轨( Services Track)和合作伙伴中心(Partner Hub)。服务轨采用三级分层结构（Select、Preferred、Global Premier），根据认证人员数量、生产部署客户数和公开客户案例来衡量合作伙伴的Claude实践深度。自3月启动以来，已有超过40,000家企业申请加入，超过10,000名顾问获得Claude认证。Accenture、Cognizant、Deloitte、KPMG、Infosys和PwC等顶级咨询公司正在大规模构建Claude实践。合作伙伴中心是一个门户网站，合作伙伴可实时查看自身评级，客户也可查找最合适的合作伙伴。该项目得到1亿美元投资支持，用于培训、技术支持和联合营销。评级每年1月1日和7月1日更新两次。",
    "why_it_matters": "这表明Anthropic正在构建一个围绕Claude的企业级生态系统，通过标准化合作伙伴评级体系降低企业采用AI的门槛，加速Claude在企业中的生产部署。",
    "action_hint": "关注此生态系统发展，评估你的组织是否应加入Claude合作网络。对于计划部署Claude的企业，可通过合作伙伴中心的公开目录筛选合适的实施伙伴。",
    "key_points": [
        "Claude合作网络自3月启动以来已有超过40,000家企业申请加入",
        "服务轨分为Select、Preferred、Global Premier三个等级，反映合作伙伴的Claude实践深度",
        "超过10,000名顾问已获得Claude认证",
        "Accenture培训30,000名专业人员，Cognizant向约350,000名员工推广Claude",
        "Global Premier等级要求至少1,000名活跃认证人员、100个生产部署客户和15个公开案例",
        "认证归属于个人而非企业，通过Anthropic Partner Academy考试获得",
        "合作伙伴中心提供每日更新的实时评级看板和公开目录",
        "合作伙伴还可通过MCP连接器将Partner Hub接入Claude进行对话式查询",
        "服务轨评级每年1月1日和7月1日更新，降级需提前90天通知",
        "未来将推出面向特定行业和用例的专业化认证"
    ],
    "evidence_quotes": [
        "The real work—and the real opportunity—is in the integration, the evaluation, and the way people's work evolves.",
        "Every firm is measured against the same requirements, whether it's a ten-person AI-native shop or a global consultancy.",
        "$100 million we committed in March funds partner training, dedicated technical support, and shared marketing."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 4: AI-enabled cyber threats MITRE ATT&CK ----
articles.append({
    "source_url": "https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack",
    "title": "What we learned mapping a year's worth of AI-enabled cyber threats",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic前沿红队发布了一份关于AI赋能网络威胁的分析报告，研究了2025年3月至2026年3月期间因恶意网络活动被封禁的832个账户，并将其映射到MITRE ATT&CK框架。研究得出三个主要结论：第一，恶意行为者正在利用AI使其更具危险性，特别是在攻击生命周期后期阶段；第二，网络攻击正变得更加自主化，AI能够将攻击的多个环节串联起来；第三，MITRE ATT&CK框架未能完全捕捉AI赋能攻击者的工具和活动。研究发现67.3%的被封账户使用AI编写恶意软件，6.5%使用AI辅助横向移动。在分析的前六个月，33%的参与者被归类为中等或更高风险；后六个月这一比例跃升至56%。研究还发现，使用AI进行账户发现增长了8.9%，而AI辅助钓鱼下降了8.6%，表明攻击者正将AI应用于攻击生命周期的更深阶段。",
    "why_it_matters": "这是首个对真实AI赋能网络攻击进行系统性分析的大规模研究，揭示了现有安全框架的不足，为AI时代的安全防御策略提供了关键证据。",
    "action_hint": "安全团队应重新评估基于传统指标（技术数量、工具类型）的风险评估方法，关注攻击者在攻击生命周期中应用AI的位置和方式。",
    "key_points": [
        "分析了2025年3月至2026年3月间832个因恶意网络活动被封禁的账户",
        "67.3%的账户使用AI编写恶意软件，6.5%使用AI辅助横向移动",
        "高风险行为者比例从33%跃升至56%，增长了约1.7倍",
        "AI辅助钓鱼下降8.6%，而AI辅助账户发现增长8.9%，显示攻击者深入攻击生命周期",
        "传统基于技术数量和工具类型的风险评估方法已不再有效",
        "低技能行为者平均使用约16种技术，高技能约20种，差距显著缩小",
        "MITRE ATT&CK框架缺少AI自主编排攻击链的战术ID",
        "高风险行为者的关键区别在于围绕模型构建的\"脚手架\"架构，使AI能以最小人工干预串联攻击步骤",
        "Anthropic已开发和部署了网络防护措施来检测和阻止发现的部分活动",
        "正在与MITRE讨论如何扩展ATT&CK框架以包含AI赋能行为"
    ],
    "evidence_quotes": [
        "Malicious actors are using AI in ways that make them more dangerous... threat actors are using AI in the later, more complex stages of their cyber operations.",
        "The MITRE ATT&CK framework does not fully capture the tools and activities that make AI-enabled attackers so dangerous.",
        "There is no ATT&CK ID for this type of agentic orchestration—yet these are precisely the behaviors we expect to see much more of as AI agents become more capable."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 5: Expanding Project Glasswing ----
articles.append({
    "source_url": "https://www.anthropic.com/news/expanding-project-glasswing",
    "title": "Expanding Project Glasswing",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic于2026年6月2日宣布扩展Project Glasswing，将合作伙伴从最初的约50家扩大到约150家新组织，分布在超过15个国家。新合作伙伴涵盖电力、水务、医疗、通信和硬件等关键基础设施领域，许多是维护全球众多组织依赖的代码库的供应商。每个合作伙伴的共同点是其代码库一旦被成功攻击可能造成灾难性后果，估计影响超过1亿人。文章阐述了Project Glasswing的长期目标：让AI使所有软件更安全，帮助行业适应AI如何改变网络安全的核心假设。Anthropic预计6至12个月内其他AI公司将拥有Mythos级模型并可能无安全防护地发布。为此，Anthropic推出了Claude Security产品，并在开发更强大的安全防护措施以确保安全释放Mythos级能力。",
    "why_it_matters": "Project Glasswing是AI时代网络安全防御的前沿实践，展示了前沿AI模型如何从漏洞发现者转变为安全守护者，对全球关键基础设施保护具有深远意义。",
    "action_hint": "如果你的组织涉及关键基础设施或维护重要开源软件，应关注Project Glasswing的后续扩展计划，考虑申请加入或学习其安全实践。",
    "key_points": [
        "Project Glasswing扩展至约150家新组织，来自超过15个国家",
        "新合作伙伴涵盖电力、水务、医疗、通信和硬件等关键基础设施领域",
        "估计每个合作伙伴的代码库被成功攻击可能影响超过1亿人",
        "Anthropic预计6至12个月内其他公司也将拥有Mythos级模型",
        "已推出Claude Security产品用于代码库扫描和补丁建议",
        "Mythos Preview已被合作伙伴用于编写补丁和预发布检查",
        "当前瓶颈在于验证、披露和修补漏洞而非发现漏洞",
        "长期目标是实现Mythos级能力的安全普遍可用",
        "计划进一步扩展Project Glasswing并扩大Cyber Verification Program",
        "Anthropic认为未来前沿模型发布将面临越来越高的安全风险"
    ],
    "evidence_quotes": [
        "The organizations in this new group are based in more than 15 countries, and most provide critical infrastructure to many more.",
        "Within 6 to 12 months, we expect that many other AI companies will have Mythos-class models, and they could release them without safeguards that prevent misuse.",
        "The bottleneck in cybersecurity is now verifying, disclosing, and patching the large numbers of vulnerabilities that Mythos-class models can surface."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 6: Project Glasswing (comprehensive launch article) ----
articles.append({
    "source_url": "https://www.anthropic.com/glasswing",
    "title": "Project Glasswing: Securing critical software for the AI era",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic宣布启动Project Glasswing，这是一个汇集AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorganChase、Linux基金会、Microsoft、NVIDIA和Palo Alto Networks等巨头的网络安全合作计划。该计划的核心是Claude Mythos Preview——一款未公开发布的前沿模型，在代码能力上已超越除最顶尖人类外的所有安全专家。Mythos Preview已发现数千个零日漏洞，包括每个主要操作系统和Web浏览器中的高危漏洞。例如，它发现了一个存在27年的OpenBSD漏洞、一个被自动化测试工具测试了500万次都未发现的FFmpeg 16年漏洞，以及Linux内核中多个漏洞的串联利用。在CyberGym评估中，Mythos Preview得分83.1%，而Claude Opus 4.6为66.6%。Anthropic承诺投入最高1亿美元的模型使用积分和400万美元的开源安全组织捐款。",
    "why_it_matters": "这标志着AI在网络安全领域的一个重要转折点——AI模型在漏洞发现方面已接近甚至超越人类顶级专家。Project Glasswing代表了行业巨头联合应对AI安全挑战的前所未有的合作模式。",
    "action_hint": "安全决策者应密切关注Project Glasswing的成果和最佳实践。如果你的组织管理关键软件基础设施，考虑评估如何将AI驱动的安全扫描整合到开发流程中。",
    "key_points": [
        "Project Glasswing汇集了AWS、Apple、Cisco、Google、Microsoft、NVIDIA等12家行业巨头",
        "Claude Mythos Preview在SWE-bench Verified上得分93.9%，Opus 4.6为80.8%",
        "发现了一个存在27年的OpenBSD漏洞(远程崩溃)和16年的FFmpeg漏洞",
        "Mythos Preview在CyberGym评估中以83.1%大幅领先Opus 4.6的66.6%",
        "在Humanity's Last Exam中Mythos Preview达56.8%(无工具)和64.7%(有工具)",
        "能够自主发现并串联利用Linux内核中的多个漏洞实现提权",
        "Anthropic承诺最高1亿美元模型使用积分和400万美元开源安全捐款",
        "模型使用定价为每百万输入/输出token $25/$125",
        "不计划公开提供Mythos Preview，将逐步通过安全防护释放能力",
        "计划在90天内发布公开报告并制定AI时代安全实践建议"
    ],
    "evidence_quotes": [
        "AI models have reached a level of coding capability where they can surpass all but the most skilled humans at finding and exploiting software vulnerabilities.",
        "Mythos Preview found a 27-year-old vulnerability in OpenBSD... the model autonomously found and chained together several vulnerabilities in the Linux kernel.",
        "Ten years after the first DARPA Cyber Grand Challenge, frontier AI models are now becoming competitive with the best humans at finding and exploiting vulnerabilities."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 7: Engineering at Anthropic (blocked - listing page) ----
articles.append({
    "source_url": "https://www.anthropic.com/engineering",
    "title": "Engineering at Anthropic",
    "reader_status": "blocked",
    "reader_agent": "Article Reader Agent",
    "article_summary": "",
    "why_it_matters": "",
    "action_hint": "",
    "key_points": [],
    "evidence_quotes": [],
    "reading_quality": "low",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 8: Claude Code product page ----
articles.append({
    "source_url": "https://www.anthropic.com/product/claude-code",
    "title": "Claude Code | Anthropic's agentic coding system",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "本文详细介绍了Anthropic的智能编码系统Claude Code。Claude Code是一个能够读取整个代码库、跨文件进行更改、运行测试并交付已提交代码的智能体编码系统。在Anthropic内部，大多数代码已由Claude Code编写，工程师专注于架构、产品思维和持续编排。文章列举了多个企业案例：Stripe向1,370名工程师部署Claude Code，一个团队在四天内完成了估计需要十人周工作的10,000行Scala到Java迁移；Ramp将事故调查时间减少了80%；Wiz在约20小时内将50,000行Python库迁移到Go，估计原本需要两到三个月；Rakuten将新功能平均交付时间从24个工作日缩短到5个。Claude Code支持代码库导航、全代码库开发、工具链执行、测试和CI管理，并让无工程背景的人也能构建软件。",
    "why_it_matters": "Claude Code代表了AI辅助编程从\"自动补全\"到\"智能体\"的范式转变，正在深刻改变软件工程的生产力格局，并使得编程向更广泛人群民主化。",
    "action_hint": "工程团队应评估Claude Code能否融入现有开发流程。对于缺乏工程背景但需要构建工具的人员，Claude Code提供了一条低门槛路径。可参考Stripe、Ramp等企业的部署经验。",
    "key_points": [
        "Claude Code是项目级别的智能体编码系统，不同于行级别的代码补全工具",
        "Anthropic内部大多数代码已由Claude Code编写",
        "Stripe向1,370名工程师部署，团队4天完成10,000行代码迁移",
        "Ramp将事故调查时间减少80%，非工程团队用自然语言查询数据仓库",
        "Wiz将50,000行Python库迁移到Go从2-3个月缩短到约20小时",
        "Rakuten将新功能交付时间从24个工作日缩短到5个",
        "支持代码库导航、全代码库开发、工具链执行、测试和CI管理",
        "采用谨慎的安全设计：默认在修改文件或运行命令前征求许可",
        "让创始人、产品经理、设计师等非工程人员也能构建软件原型",
        "支持多种自主程度，从审批每个操作到内置分类器自动区分安全与风险操作"
    ],
    "evidence_quotes": [
        "The tools engineers use to build software are now capable of building software themselves. That changes what it means to be an engineer.",
        "At Anthropic, the majority of code is now written by Claude Code.",
        "If you can describe it, you can build it."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 9: Google DeepMind Models (blocked - catalog page) ----
articles.append({
    "source_url": "https://deepmind.google/models/",
    "title": "Explore models",
    "reader_status": "blocked",
    "reader_agent": "Article Reader Agent",
    "article_summary": "",
    "why_it_matters": "",
    "action_hint": "",
    "key_points": [],
    "evidence_quotes": [],
    "reading_quality": "low",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 10: Gemini 3.5 product page ----
articles.append({
    "source_url": "https://deepmind.google/models/gemini/",
    "title": "Gemini 3.5: Frontier intelligence with action",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Google DeepMind推出了Gemini 3.5系列模型，主打\"前沿智能与行动能力\"的结合。Gemini 3.5 Flash在多项基准测试中展现出领先性能：Terminal-Bench 2.1得分76.2%（智能体终端编码），SWE-Bench Pro得分55.1%，MCP Atlas（多步骤工作流）得分83.6%，OSWorld-Verified得分78.4%。在推理方面，Humanity's Last Exam达40.2%，ARC-AGI-2达72.1%。文章展示了多个企业应用案例：Shopify使用Gemini 3.5 Flash运行并行子智能体进行复杂数据分析；Macquarie Bank用于加速客户入职流程（处理100页以上复杂文档）；Salesforce将其集成到Agentforce中自动化企业任务；Ramp用于智能OCR识别；Xero用于自动化管理多周工作流；Databricks用于监控和诊断大规模数据集。该系列包括3.5 Flash（已可用）、3.1 Pro和即将推出的3.5 Pro。",
    "why_it_matters": "Gemini 3.5代表了Google在智能体AI领域的最强竞争力，在多个编码和智能体基准测试上与Claude和GPT系列直接竞争，其企业生态案例展示了AI智能体的实际商业价值。",
    "action_hint": "在评估AI编码和智能体模型时，应将Gemini 3.5 Flash纳入对比名单。特别关注其在MCP Atlas（83.6%）和OSWorld-Verified（78.4%）等智能体任务上的表现。",
    "key_points": [
        "Gemini 3.5 Flash在Terminal-Bench 2.1得分76.2%，在智能体编码任务上具有竞争力",
        "MCP Atlas多步骤工作流得分83.6%，领先于多个竞品",
        "OSWorld-Verified得分为78.4%，在计算机使用任务上表现强劲",
        "ARC-AGI-2抽象推理得分72.1%，在视觉推理任务上表现突出",
        "Shopify使用Gemini 3.5 Flash运行并行子智能体进行长时域数据分析",
        "Salesforce集成到Agentforce中实现复杂多轮工具调用",
        "Ramp用于多模态理解复杂发票并结合历史模式推理",
        "Macquarie Bank用于处理100页以上复杂文档加速客户入职",
        "Gemini 3.5 Pro即将推出，3.1 Pro和3.5 Flash已可用",
        "Gemini 3.5 Flash在多模态理解（MMMU-Pro 83.6%）上也有出色表现"
    ],
    "evidence_quotes": [
        "Gemini 3.5 is leading across a wide range of benchmarks.",
        "Gemini's newest flash model advances the frontier for intelligence per dollar. It performs 42% better than Flash 3 on our long range, multi-turn cyber benchmark.",
        "We're seeing promising gains in how quickly and confidently developers can move from idea to code."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 11: Gemini Omni product page ----
articles.append({
    "source_url": "https://deepmind.google/models/gemini-omni/",
    "title": "Gemini Omni: Create anything from anything",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Google DeepMind发布了Gemini Omni，这是一款以视频为核心的多模态生成模型。Gemini Omni将Gemini的推理能力与创造能力相结合，实现了从任何输入（图像、文本、视频、音频）创建任何输出的能力。其核心功能包括：通过自然对话逐步编辑视频，维持一致连贯的场景；应用真实世界知识（物理、历史、科学、文化）进行有意义的叙事；引用参考图像、视频等素材进行创作；支持多轮编辑保持一致性；通过自然语言替换角色和物体；将草稿图转化为逼真视频；理解并同步文本与画面内容。Gemini Omni在Gemini应用、Google Flow和YouTube Shorts中可用。所有通过Omni创作的内容均包含SynthID数字水印和C2PA内容凭证，以支持内容溯源和透明度。",
    "why_it_matters": "Gemini Omni代表了AI视频生成从\"生成\"到\"编辑/创作\"的重大跨越，将推理能力与多模态创造深度融合，预示着内容创作方式的根本变革。",
    "action_hint": "内容创作者和视频制作团队应试用Gemini Omni，评估其在视频编辑、特效和内容创作中的应用潜力。特别是其通过自然对话进行多轮编辑的能力，可能改变传统视频工作流。",
    "key_points": [
        "Gemini Omni支持从任何输入（图像、文本、视频、音频）创建内容",
        "核心能力是通过自然语言对话逐步编辑视频，维持一致性",
        "融合了Gemini的世界知识（物理、历史、科学、文化）进行叙事",
        "支持多轮编辑，可在后续对话中更改细节、环境、镜头角度等",
        "可通过参考图像替换角色和物体，保持场景一致",
        "能够将草稿图转化为逼真视频，将草图作为运动指导",
        "支持引用多个输入源并将它们融合为单一叙事",
        "支持运动和风格迁移，可应用参考视频的动作和风格",
        "所有输出包含SynthID数字水印和C2PA内容凭证",
        "在Gemini应用、Google Flow和YouTube Shorts中可用"
    ],
    "evidence_quotes": [
        "Gemini Omni is where Gemini's ability to reason meets the ability to create. It delivers a leap in world understanding, multimodality, and editing.",
        "Think of Gemini Omni like Nano Banana, but for video. Every edit you make builds on the one before – maintaining a consistent, coherent scene.",
        "Omni has an intuitive understanding of forces like gravity, kinetic energy, and fluid dynamics for more realistic movement."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 12: Nano Banana (blocked - short landing page) ----
articles.append({
    "source_url": "https://deepmind.google/models/gemini-image/",
    "title": "Nano Banana: Create and edit detailed images",
    "reader_status": "blocked",
    "reader_agent": "Article Reader Agent",
    "article_summary": "",
    "why_it_matters": "",
    "action_hint": "",
    "key_points": [],
    "evidence_quotes": [],
    "reading_quality": "low",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# ---- Article 13: Gemini Audio product page ----
articles.append({
    "source_url": "https://deepmind.google/models/gemini-audio/",
    "title": "Gemini Audio: Talk, create and control audio",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Google DeepMind推出了Gemini Audio系列音频模型，包括两个核心产品：Gemini 3.1 Flash Live和Gemini 3.1 Flash TTS。Flash Live专注于低延迟、流畅自然的实时对话，可识别音高和语速等语音细微差别，同时能够调用函数管理多步骤复杂任务。Flash TTS专注于语音合成，通过直观的音频标签提供对风格、语速和语调的精确控制。两大模型均支持多语言。在安全方面，所有音频输出均带有SynthID水印技术，可用于检测语音是否由AI创建或编辑。模型可通过Google AI Studio、Gemini API和Gemini Live API访问，也可通过Gemini Enterprise Agent Platform和Gemini Enterprise for Customer Experience部署到企业级应用中。",
    "why_it_matters": "Gemini Audio展示了AI语音技术正在从简单的文本转语音向具备高表现力、实时交互和深度理解能力的成熟平台演进，为语音优先应用和企业级语音交互开辟了新可能。",
    "action_hint": "开发语音应用或需要AI语音交互能力的产品团队，应评估Gemini Audio在实时对话（Flash Live）和高度可控语音合成（Flash TTS）两个方向的能力。",
    "key_points": [
        "Gemini 3.1 Flash Live面向低延迟流畅的实时对话，识别音高和语速等语音细微差别",
        "Gemini 3.1 Flash TTS通过音频标签提供对风格、语速和语调的精确控制",
        "Flash Live支持在实时对话中调用函数管理多步骤复杂任务",
        "所有音频输出均带有SynthID水印，可检测AI生成或编辑的语音",
        "支持多语言语音交互和翻译能力",
        "可通过Google AI Studio、Gemini API和Gemini Live API访问",
        "支持语音理解——不仅转录，还能识别说话者和理解意图",
        "可用于企业级客户体验、视频创作等场景",
        "经过了全面的安全评估和红队测试以确保负责任部署"
    ],
    "evidence_quotes": [
        "Fluid and natural live dialogue and translation capabilities, for powerful voice-first applications.",
        "Craft anything from short snippets to long-form narratives, with granular control over style, pace, delivery and performance.",
        "Go beyond simple transcription, with models that identify who's talking and understand the intent behind the words."
    ],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})


# ============================================================
# Write to JSONL
# ============================================================
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for article in articles:
        f.write(json.dumps(article, ensure_ascii=False) + '\n')

print(f"Written {len(articles)} entries to {OUTPUT_FILE}")

# Also print summary
statuses = {}
for a in articles:
    s = a['reader_status']
    statuses[s] = statuses.get(s, 0) + 1
    print(f"  [{s.upper():7s}] {a.get('title', '')[:60]}")

print(f"\nSummary: {statuses}")
