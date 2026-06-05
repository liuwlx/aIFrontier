import json

entries = []

# 1. Anthropic Research page
entries.append({
    "source_url": "https://www.anthropic.com/research",
    "title": "Research",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面是Anthropic研究团队的入口页面，介绍了其五大研究方向：可解释性、对齐、社会影响、前沿红队和经济学研究。页面列举了近期重要研究成果，包括自然语言自编码器（将Claude思维转化为文本）、降低代理失调的教学方法、Project Deal（AI市场实验）、以及8.1万人AI需求调查等。同时展示了Anthropic研究团队的最新论文列表，涵盖政策、经济、公告等多个类别。",
    "why_it_matters": "Anthropic的研究组合代表了AI安全与对齐领域的前沿探索，其多个研究方向直接影响行业标准和政策制定。",
    "action_hint": "关注Anthropic研究动态，特别是可解释性和对齐方面的新方法，可用于评估自身AI系统的安全性。",
    "key_points": ["Anthropic设有可解释性、对齐、社会影响、前沿红队、经济研究五大研究团队", "2026年5月发布自然语言自编码器研究，将Claude的内部思维转化为可读文本", "发布降低代理失调的新方法，提升AI系统可靠性", "Project Deal实验展示了AI在经济市场中的行为模式", "8.1万人参与的AI需求调查是迄今最大规模的多语言定性研究", "2026年6月发布AI网络威胁研究报告，映射MITRE ATT&CK框架"],
    "evidence_quotes": ["Our research teams investigate the safety, inner workings, and societal impacts of AI models", "The mission of the Interpretability team is to discover and understand how large language models work internally", "Nearly 81,000 people participated—the largest and most multilingual qualitative study of its kind"],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 2. Anthropic Economic Futures
entries.append({
    "source_url": "https://www.anthropic.com/economic-futures",
    "title": "Economic Futures",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面是Anthropic经济未来项目的门户，旨在支持AI经济影响的研究和政策制定。项目核心是Anthropic经济指数，通过分析Claude在各经济领域的实际使用情况，揭示AI在全球经济中的采用模式，覆盖美国各州和数百种职业。页面列出了最新的研究成果，包括经济基元报告、地理和企业AI采用不均等分析、以及对软件开发影响的研究。",
    "why_it_matters": "Anthropic经济指数提供了真实世界中AI应用的数据视角，对理解AI的经济影响和制定相关政策具有重要参考价值。",
    "action_hint": "浏览经济指数数据可了解AI在各行业的实际渗透情况，为投资和战略规划提供数据支持。",
    "key_points": ["Anthropic经济未来项目支持AI经济影响研究和政策制定", "经济指数通过分析Claude对话揭示AI在经济中的实际使用模式", "数据覆盖美国各州和数百种职业的AI使用情况", "2026年1月发布经济基元报告，定义AI使用的基本构建块", "研究显示AI采用呈不均匀的地理和企业分布特征", "使用Clio系统保护用户隐私的同时进行数据分析"],
    "evidence_quotes": ["The Anthropic Economic Futures program aims to support research and policy development for addressing the economic impacts of AI", "The Anthropic Economic Index reveals the shape of AI adoption across the world", "The Anthropic Economic Index is made possible by Clio, a system that allows us to analyze conversations with Claude while preserving user privacy"],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 3. Anthropic Services Track and Partner Hub (FULL ARTICLE)
entries.append({
    "source_url": "https://www.anthropic.com/news/services-track-partner-hub",
    "title": "Introducing the Services Track and Partner Hub of the Claude Partner Network",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic于2026年6月3日宣布推出Claude合作伙伴网络的服务层级（Services Track）和合作伙伴门户（Partner Hub）。自3月份启动以来，超过4万家公司申请加入，超过1万名顾问获得Claude认证。Accenture已培训3万名专业人员，Cognizant向约35万名员工推广，Deloitte向全球47万名员工开放。服务层级分Select、Preferred和Global Premier三级。合作伙伴门户可实时显示合作伙伴层级、认证团队和客户部署，支持通过MCP连接器在Claude内查询状态。Anthropic承诺投入1亿美元用于培训、技术支持和联合营销。",
    "why_it_matters": "该计划标志着AI企业级部署生态系统的成熟，通过标准化合作伙伴认证体系降低了企业采用AI的门槛，为AI服务的规模化交付奠定了基础。",
    "action_hint": "如果企业正在考虑将Claude集成到业务流程中，可以通过合作伙伴门户找到经过认证的、有实际交付经验的实施合作伙伴。",
    "key_points": ["超过40,000家公司申请加入Claude合作伙伴网络", "超过10,000名顾问已获得Claude认证", "服务层级分三级：Select、Preferred、Global Premier", "Accenture培训30,000名专业人员使用Claude", "Cognizant向约350,000名员工推广Claude", "Deloitte向全球470,000人开放Claude使用", "合作伙伴门户提供实时状态查看和MCP集成", "Anthropic投入1亿美元用于合作伙伴支持", "每年1月1日和7月1日进行层级晋升评审", "即将推出行业和用例专项认证"],
    "evidence_quotes": ["Almost every large enterprise is moving AI into production, and many have discovered something important: a successful pilot is not the same as a system a business can run on.", "More than 40,000 firms have applied to join and more than 10,000 consultants have earned a Claude certification", "The Services Track is a tiered structure that reflects what a firm has actually built and delivered with Claude."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 4. Anthropic AI-enabled cyber threats MITRE (FULL ARTICLE)
entries.append({
    "source_url": "https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack",
    "title": "What we learned mapping a year's worth of AI-enabled cyber threats",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic于2026年6月3日发布报告，分析了2025年3月至2026年3月间因恶意网络活动被封禁的832个账户，映射到MITRE ATT&CK框架。核心发现：67.3%的账户使用AI编写恶意软件，6.5%使用AI进行横向移动等复杂攻击。中高风险行为者比例在6个月内从33%跃升至56%。AI辅助的账户发现技术增长8.9%，钓鱼技术下降8.6%，表明攻击者正将AI应用于攻击链的后期阶段。传统风险评分方法已不再可靠，MITRE ATT&CK框架缺少AI自主编排攻击的技术分类。Anthropic已部署检测和阻止恶意软件开发及数据窃取的防护措施。",
    "why_it_matters": "该报告首次系统性地将AI辅助网络攻击映射到行业标准框架，揭示了现有安全框架的不足，对全球网络安全防御体系的演进具有重要指导意义。",
    "action_hint": "安全团队应参考此报告的发现，重新评估威胁建模方法，特别是关注AI如何在攻击链的后期阶段发挥作用。",
    "key_points": ["分析了832个因恶意网络活动被封禁的账户，映射到MITRE ATT&CK框架", "67.3%的账户使用AI编写恶意软件", "6.5%的账户使用AI进行横向移动等复杂攻击", "中高风险行为者比例在6个月内从33%跃升至56%", "AI辅助的账户发现技术增长8.9%，钓鱼技术下降8.6%", "AI使低技能攻击者也能执行过去需要专业知识的高级攻击技术", "传统风险评分方法已不再可靠", "MITRE ATT&CK框架缺少AI自主编排攻击的技术分类", "Anthropic已部署针对恶意软件开发和数据窃取的防护措施", "与MITRE讨论如何将AI相关行为纳入ATT&CK框架"],
    "evidence_quotes": ["Malicious actors are using AI in ways that make them more dangerous. More specifically, threat actors are using AI in the later, more complex stages of their cyber operations.", "Cyberattacks are becoming more autonomous, and the fact that AI can be used to chain together many parts of the attack means that the old ways of differentiating high- from low-risk actors are no longer as effective.", "The MITRE ATT&CK framework does not fully capture the tools and activities that make AI-enabled attackers so dangerous."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 5. Anthropic Expanding Project Glasswing (FULL ARTICLE)
entries.append({
    "source_url": "https://www.anthropic.com/news/expanding-project-glasswing",
    "title": "Expanding Project Glasswing",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Anthropic于2026年6月2日宣布扩大Project Glasswing规模，将合作伙伴从约50个扩展到约150个新组织，分布在超过15个国家，涵盖电力、水务、医疗、通信和硬件等关键基础设施行业。自2026年4月启动以来，合作伙伴使用Claude Mythos Preview扫描代码库，已发现超过10,000个高危或严重安全漏洞。Anthropic预计6-12个月内其他AI公司将拥有Mythos级别模型。项目目标从漏洞发现扩展到披露、修复和部署补丁。同时发布Claude Security产品用于代码扫描和补丁建议。",
    "why_it_matters": "Project Glasswing代表了AI在网络安全防御领域的前沿实践，其经验教训对整个行业应对即将到来的AI驱动网络攻击浪潮具有重要参考价值。",
    "action_hint": "如果你是关键基础设施或开源软件的维护者，应关注Project Glasswing的进展，考虑未来申请加入以保护代码库。",
    "key_points": ["Project Glasswing从约50个初始合作伙伴扩展到约150个新组织", "新合作伙伴分布在超过15个国家，涵盖电力、水务、医疗等行业", "已发现超过10,000个高危或严重安全漏洞", "Claude Mythos Preview在OpenBSD中发现存在27年的漏洞", "在FFmpeg中发现存在16年的漏洞，此前自动化测试工具已测试500万次", "预计6-12个月内其他公司将拥有Mythos级别模型", "发布了Claude Security产品用于代码扫描和补丁建议", "长期目标是将支持从漏洞发现扩展到补丁部署"],
    "evidence_quotes": ["Project Glasswing is our collaborative effort to secure the world's most important software.", "These partners have so far found more than 10,000 high- or critical-severity security flaws.", "Within 6 to 12 months, we expect that many other AI companies will have Mythos-class models, and they could release them without safeguards that prevent misuse."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 6. Anthropic Project Glasswing / Mythos Preview (FULL ARTICLE)
entries.append({
    "source_url": "https://www.anthropic.com/glasswing",
    "title": "Project Glasswing: Securing critical software for the AI era",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "本文详细介绍Anthropic发起的Project Glasswing计划，联合AWS、Apple、Cisco、Google、Microsoft、NVIDIA等12家核心合作伙伴，共同保护全球最关键软件安全。技术核心是Claude Mythos 2 Preview，其代码能力已超越除最顶尖人类外的所有人。Mythos Preview已发现数千个零日漏洞，包括OpenBSD中存在27年的远程崩溃漏洞、FFmpeg中存在16年且经过500万次自动化测试未被发现的漏洞、Linux内核中自主发现并组合多个漏洞实现权限提升。CyberGym基准测试中Mythos Preview得分83.1%，远超Claude Opus 4.6的66.6%。Anthropic承诺投入1亿美元使用额度并捐赠400万美元给开源安全组织。",
    "why_it_matters": "Mythos Preview展示了AI在网络安全领域的突破性能力，标志着AI在发现和利用软件漏洞方面已接近人类顶级专家水平，将深刻改变网络安全的攻防格局。",
    "action_hint": "安全团队应重新评估依赖人工代码审计的传统安全策略，考虑引入AI驱动的安全扫描工具以应对即将到来的AI攻击浪潮。",
    "key_points": ["Project Glasswing联合AWS、Apple、Cisco、Google、Microsoft、NVIDIA等12家核心合作伙伴", "Claude Mythos Preview代码能力已超越除最顶尖人类外的所有人", "发现包含27年历史的OpenBSD远程崩溃漏洞", "发现FFmpeg中存在16年、经过500万次自动化测试未被发现的漏洞", "在Linux内核中自主发现并组合多个漏洞实现提权", "CyberGym基准测试：Mythos Preview 83.1% vs Opus 4.6 66.6%", "已覆盖所有主要操作系统和网络浏览器的漏洞扫描", "Anthropic承诺投入1亿美元使用额度和400万美元捐赠", "当前全球网络犯罪经济损失约每年5000亿美元"],
    "evidence_quotes": ["AI models have reached a level of coding capability where they can surpass all but the most skilled humans at finding and exploiting software vulnerabilities.", "Mythos Preview has already found thousands of high-severity vulnerabilities, including some in every major operating system and web browser.", "It was able to identify nearly all of these vulnerabilities—and develop many related exploits—entirely autonomously, without any human steering."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 7. Anthropic Engineering (partial)
entries.append({
    "source_url": "https://www.anthropic.com/engineering",
    "title": "Engineering at Anthropic",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面是Anthropic工程团队的博客索引页，展示从2024年9月到2026年5月的工程文章，涵盖AI代理安全控制、Claude Code质量报告、托管代理扩展、自动模式设计、长时运行应用的框架设计、Opus 4.6的BrowseComp性能分析、代理评估基础设施噪声量化、使用并行Claude构建C编译器、防AI技术评估设计等主题。",
    "why_it_matters": "Anthropic工程博客分享了构建和部署大规模AI系统的实际经验，对AI工程实践具有重要参考价值。",
    "action_hint": "浏览Anthropic工程博客，重点关注代理安全性、评估方法和系统架构方面的最佳实践。",
    "key_points": ["博客涵盖从2024年9月到2026年5月的工程实践", "重点探讨AI代理的安全控制和权限管理", "介绍了Claude Code自动模式和托管代理的架构设计", "分析了代理评估中的基础设施噪声问题", "展示了使用并行Claude构建C编译器的实验", "讨论了防AI技术评估的设计方法"],
    "evidence_quotes": ["How we contain Claude across products: As agents grow more capable, so does their potential blast radius.", "Scaling Managed Agents: Decoupling the brain from the hands", "Building a C compiler with a team of parallel Claudes"],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 8. Anthropic Claude Code (partial)
entries.append({
    "source_url": "https://www.anthropic.com/product/claude-code",
    "title": "Inside Claude Code",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面是Claude Code的产品介绍页。Claude Code是Anthropic的代理编码系统，能读取代码库、跨文件修改、运行测试并交付代码。在Anthropic内部，大部分代码已由Claude Code编写。Stripe向1370名工程师部署，完成万行Scala到Java迁移仅用4天；Ramp将事件调查时间减少80%；Wiz用约20小时将5万行Python库迁移到Go；Rakuten将新功能交付时间从24天缩短到5天。",
    "why_it_matters": "Claude Code代表了AI从代码补全到自主编程的范式转变，正在重新定义软件工程师的工作方式和企业软件交付效率。",
    "action_hint": "开发团队应评估Claude Code在代码迁移、测试自动化和新功能开发中的应用，以显著提升工程效率。",
    "key_points": ["Claude Code具备跨文件修改和自动测试能力", "在Anthropic内部，大部分代码已由Claude Code编写", "Stripe向1370名工程师部署，完成万行Scala到Java迁移仅用4天", "Ramp将事件调查时间减少80%", "Wiz用约20小时完成5万行Python到Go的迁移", "Rakuten将新功能交付时间从24天缩短到5天", "支持git、Kubernetes等工具链的原生操作", "提供从全面审批到自动分类的安全控制级别", "非工程人员也能通过自然语言描述构建原型"],
    "evidence_quotes": ["At Anthropic, the majority of code is now written by Claude Code.", "Claude Code is an agentic coding system that reads your codebase, makes changes across files, runs tests, and delivers committed code.", "Stripe deployed Claude Code across 1,370 engineers of all levels through a zero-configuration enterprise binary."],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 9. Google DeepMind Explore Models (partial)
entries.append({
    "source_url": "https://deepmind.google/models/",
    "title": "Explore models",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面是Google DeepMind模型目录，展示了其AI模型生态系统，包括Gemini 3.5（前沿智能与行动能力）、Gemini Omni（全能创作）、Gemma 4（最智能的开源模型）、Nano Banana 2（图像生成与编辑）、Lyria 3（音乐创作）、Veo（视频生成）、Imagen（文本到图像）、Gemini Audio（音频）、Gemini Robotics（机器人视觉-语言-行动模型）、Genie 3（世界模型）和Gemini Embedding。还介绍了Google AI Studio、Antigravity、Enterprise Agent Platform等开发平台。",
    "why_it_matters": "Google DeepMind的模型组合覆盖了从语言、图像、视频、音频到机器人技术的全栈AI能力，代表了当前AI技术的最前沿。",
    "action_hint": "浏览Google DeepMind的模型目录，了解各模型的能力和适用场景，为技术选型提供参考。",
    "key_points": ["Gemini 3.5是主打前沿智能与行动能力的最新模型系列", "Gemini Omni实现从任意输入创作内容", "Gemma 4是最智能的开源模型系列", "Nano Banana 2提供专业级图像生成和编辑", "Lyria 3支持带人声的音乐创作", "Genie 3代表世界模型的新前沿", "SynthID为AI生成内容添加水印"],
    "evidence_quotes": ["Explore our next generation AI systems", "Gemini 3.5: Our latest family of models combining frontier intelligence with action", "Gemini Omni: Create anything from anything – with a leap in world understanding, multimodality, and editing"],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 10. Google DeepMind Gemini 3.5 (FULL ARTICLE)
entries.append({
    "source_url": "https://deepmind.google/models/gemini/",
    "title": "Gemini 3.5: Build intelligent agents",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Google DeepMind的Gemini 3.5 Flash在多项基准测试中表现卓越：Terminus-2代理终端编码76.2%、SWE-Bench Pro 55.1%、MCP Atlas多步骤工作流83.6%、OSWorld-Verified计算机使用78.4%、Finance Agent v2金融分析57.9%。企业应用方面，Shopify用于并行子代理数据分析、Macquarie Bank用于100页以上文档处理、Salesforce集成到Agentforce、Ramp用于智能OCR、Xero用于税务流程自动化、Databricks用于数据诊断。Gemini 3.5 Pro即将推出。",
    "why_it_matters": "Gemini 3.5在代理和编码任务上的性能表现标志着AI模型正向真正的自主代理方向发展，对企业自动化的影响深远。",
    "action_hint": "评估Gemini 3.5 Flash在代理工作流和编码任务中的表现，考虑在需要高自主性的场景中试用。",
    "key_points": ["Gemini 3.5 Flash在Terminus-2测试中达76.2%", "MCP Atlas多步骤工作流测试83.6%", "OSWorld-Verified计算机使用测试78.4%", "SWE-Bench Pro单次尝试55.1%", "Shopify用于并行子代理的长期数据分析", "Macquarie Bank用于100页+文档的智能处理", "Salesforce集成到Agentforce自动化企业任务", "Ramp用于智能OCR发票识别", "Xero用于自动管理复杂工作流"],
    "evidence_quotes": ["Gemini 3.5: Frontier intelligence with action", "Our most impressive model yet for agentic workflows. Gemini 3.5 is leading across a wide range of benchmarks.", "Gemini's newest flash model advances the frontier for intelligence per dollar."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 11. Google DeepMind Gemini Omni (FULL ARTICLE)
entries.append({
    "source_url": "https://deepmind.google/models/gemini-omni/",
    "title": "Gemini Omni: Create anything from anything",
    "reader_status": "read",
    "reader_agent": "Article Reader Agent",
    "article_summary": "Google DeepMind发布Gemini Omni，一个突破性多模态创作模型，能够从任意输入（文本、图像、视频、音频）生成和编辑视频内容。核心能力包括：通过自然对话交互进行视频编辑，保持场景一致性；应用现实世界物理知识如重力和流体动力学；理解历史、科学和文化背景进行叙事创作。功能包括改变视频美学风格、替换角色和物体、参考图像编辑、多轮对话保持一致性、文字与画面同步。Gemini Omni将Gemini的推理能力与创作能力相结合，实现了从静态图像生成到动态视频创作的重大跨越。",
    "why_it_matters": "Gemini Omni代表了AI从文本/图像生成向视频内容创作的重大跨越，其多模态理解和物理世界知识的融合将改变内容创作行业的范式。",
    "action_hint": "内容创作者和视频制作团队应关注Gemini Omni在视频编辑和生成方面的能力，探索其在创意工作流中的应用潜力。",
    "key_points": ["支持从文本、图像、视频、音频生成视频内容", "通过自然语言对话式交互进行视频编辑", "每次编辑保持场景一致性，支持多轮迭代", "理解重力、动能、流体动力学等物理规律", "融合历史、科学和文化知识进行叙事创作", "支持参考图像引导视频编辑", "可替换视频中的角色和物体", "支持文字与画面同步", "在Google Gemini和Google Flow中可用"],
    "evidence_quotes": ["Gemini Omni is where Gemini's ability to reason meets the ability to create.", "It delivers a leap in world understanding, multimodality, and editing.", "Think of Gemini Omni like Nano Banana, but for video. Every edit you make builds on the one before – maintaining a consistent, coherent scene."],
    "reading_quality": "high",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 12. Google DeepMind Nano Banana (partial)
entries.append({
    "source_url": "https://deepmind.google/models/gemini-image/",
    "title": "Nano Banana: Create and edit detailed images",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面介绍Google DeepMind的Gemini Image（Nano Banana）系列图像生成和编辑模型。Nano Banana 2基于Gemini 3.1 Flash，提供专业级图像生成和编辑且保持高速。Nano Banana Pro提供工作室级别精度。核心能力：多模态理解（上传图像加文字指令生成复杂图像）、对话式输入迭代优化、利用Gemini推理能力生成符合真实逻辑的图像。",
    "why_it_matters": "Nano Banana系列代表了AI图像生成向多模态、对话式、精确控制的演进方向。",
    "action_hint": "设计团队可探索Nano Banana在创意概念设计、广告素材生成等方面的应用，利用对话式迭代能力提升效率。",
    "key_points": ["Nano Banana 2基于Gemini 3.1 Flash，提供专业级图像生成和编辑", "Nano Banana Pro提供工作室级别精度和控制", "支持多模态理解：上传图像+文字指令", "支持对话式交互，通过自然语言迭代优化", "利用Gemini推理能力生成符合真实世界逻辑的图像"],
    "evidence_quotes": ["State-of-the-art image generation and editing models, built on Gemini", "Pro-level image generation and editing, at Flash speed", "Create and edit images with studio-quality levels of precision and control"],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

# 13. Google DeepMind Gemini Audio (partial)
entries.append({
    "source_url": "https://deepmind.google/models/gemini-audio/",
    "title": "Gemini Audio: Talk, create and control audio",
    "reader_status": "partial",
    "reader_agent": "Article Reader Agent",
    "article_summary": "该页面介绍Google DeepMind的Gemini Audio音频模型系列。3.1 Flash Live提供低延迟实时对话，识别音调语速等细微差别；3.1 Flash TTS通过音频标签精确控制风格、语速和语调。核心能力包括实时对话和翻译、从短片段到长篇叙事的语音生成、超越转录的音频理解。所有输出均使用SynthID水印标记。",
    "why_it_matters": "Gemini Audio的实时对话能力和精确语音控制为语音交互应用开辟了新可能。",
    "action_hint": "开发语音交互应用的团队应评估Gemini Audio的实时对话能力和语音控制精度，特别是在客服和内容创作场景中。",
    "key_points": ["3.1 Flash Live提供低延迟、自然流畅的实时对话", "3.1 Flash TTS通过音频标签精确控制风格、语速和语调", "支持实时对话和翻译功能", "音频理解能力可识别说话者和意图", "所有输出使用SynthID水印标记", "覆盖从短片段到长篇叙事的语音生成"],
    "evidence_quotes": ["Our most advanced audio models push new frontiers with intuitive inputs, intelligent understanding and natural expressiveness", "Fluid and natural live dialogue and translation capabilities, for powerful voice-first applications.", "Craft anything from short snippets to long-form narratives, with granular control over style, pace, delivery and performance."],
    "reading_quality": "medium",
    "summary_source": "article_reader_agent",
    "summary_language": "zh-CN"
})

out_path = 'data/agent-readings/2026/06/2026-06-04.article-reader-agent.jsonl'
with open(out_path, 'a', encoding='utf-8') as f:
    for entry in entries:
        line = json.dumps(entry, ensure_ascii=False)
        f.write(line + '\n')

print('SUCCESS: {} entries appended'.format(len(entries)))
