# Token的基本原理 — 研究笔记

> 信息来源：2026-06-29 四路并行调研。价格/窗口数字会随时间变，引用前以官方页为准；倍率类（缓存、输入输出比）相对稳定。

## 1. token是什么（机制）

- token = LLM真正读和预测的原子单位，是**子词片段**，不是字也不是词。由**BPE（字节对编码）**切出。
- BPE机制：从语料的原始字节开始，反复合并最高频的相邻对，直到词表达到目标大小（5万–20万）。高频串（"the"、代码关键字）压成一个token，罕见串拆成小片。byte-level BPE以UTF-8字节兜底，任何字符都能编码。
- 密度经验值：
  - 英文：~4字符≈1token；~0.75词≈1token（100token≈75词，1.33token/词）。
  - 中文：在GPT/Claude里约1.1–1.7 token/汉字；同样语义比英文**多耗最多64% token**。
  - 代码：~1.5–2.0 token/词，比散文高（括号、缩进、标识符碎片化）。
- **"中文税"机制**：早期BPE语料以英文为主，汉字太罕见没被合并成整字token，很多回退到原始UTF-8字节（一字≈3字节token）。这是分词器训练语料的属性，不是语言本身——国产模型反转：Qwen 3.6 <1.0x，DeepSeek-V3≈0.65x（中文比英文还便宜）。
- 来源：HuggingFace BPE课程；BigGo "language tax"；16x Prompt code-to-tokens。

## 2. 上下文窗口是什么（机制）

- 定义：一次前向推理能引用的**token总预算**，输入+输出**共享**同一池子。Anthropic原话："包括回复本身"。是工作记忆，不是训练数据。
- 为什么有限——两个叠加成本：
  - **(a) 自注意力O(n²)**：每个token要attend所有token，n×n注意力矩阵，算力和内存随长度平方增长。翻倍上下文≈四倍注意力成本。prefill阶段是O(n²)，可能OOM。
  - **(b) KV cache线性增长**：每个token在每层投影出Q/K/V；生成第N+1个token要用到前面所有token的K和V。算过一次就缓存复用（否则O(n²)重复）。缓存要存 每token×每层×每注意力头 的K/V，内存随序列长度**线性增长**，长上下文里它是最大的显存消耗——这是厂商给窗口设上限的实际原因。
  - 公式：KV cache mem = 2 × B × S × L × H_kv × D × bits。
- 来源：Anthropic context-windows文档；DigitalOcean KV caching；Brenndoerfer quadratic attention。

## 3. 窗口不是记忆 / 每次tool call在干啥

- 模型**跨轮无状态**，不"记得"上一轮。每轮把**整段历史**重新拼接、从头喂进去，重新读、重新理解。
- Anthropic原话：每轮的user消息和assistant回复在窗口里累积，"context使用随轮次线性增长"。
- **agent loop（Anthropic框架）**：tool use让模型"更像你调用的一个函数"。模型不执行任何东西——它发出结构化`tool_use`请求，你的代码执行，把结果喂回去。
  - 循环：发请求(带tools)→模型返回`stop_reason:"tool_use"`→执行工具→**发新请求，包含原始messages+assistant回复+带tool_result的user消息**→重复，直到`end_turn`。
  - Messages API无状态：每次往返都要重发 系统prompt + 工具定义 + 所有历史消息 + 所有tool_use + 所有tool_result。
- **为什么越长越贵越慢**：每轮把前面所有token当新输入重算；N轮对话早期上下文被重算约N次；成本随长度近似线性上升；prefill更长→首token更慢。
- 缓解：prompt caching缓存稳定前缀（系统prompt+工具定义）；自动compaction压缩老历史。

## 4. token怎么算 / 四种价位

- 按token计费，无按请求的固定费。
- 四类（Anthropic usage对象）：
  | 类别 | 字段 | 相对基础输入价 |
  |---|---|---|
  | 未命中输入 | input_tokens | 1.0x |
  | 输出 | output_tokens | ~5x |
  | 缓存写(5分钟TTL) | cache_creation_input_tokens | 1.25x |
  | 缓存写(1小时TTL) | (ephemeral_1h) | 2.0x |
  | 缓存读(命中) | cache_read_input_tokens | 0.1x |
- prompt caching：`cache_control:{type:"ephemeral"}`标断点，默认5分钟TTL（命中免费刷新），可选1小时。每请求最多4个断点，20-block回溯。最小可缓存1024 token（Opus 4.8/Sonnet 4.6）。`input_tokens`只报最后一个断点之后的token；总输入=cache_read+cache_creation+input_tokens（常见踩坑）。
- 对比OpenAI缓存：**自动**（无需标断点），>1024 token生效，缓存输入**5折**，**无写入费**。Anthropic=手动+更深折扣(~9折读)但有写入溢价；OpenAI=自动+浅折扣(5折)无溢价。
- **输出为什么贵~5x**：输入=prefill并行处理（一次大矩阵乘，GPU高效）；输出=自回归解码严格串行（每个token要走完整网络一遍，1000输出≈1000次串行前向），GPU利用率低→单token更贵。Sonnet 3/15=5x，GPT-4o 2.5/10=4x，普遍3–5x。
- 工具定义和系统prompt每次都算输入token：`tools`参数（名/描述/JSON schema）每次重发；API在有tools时**自动注入特殊系统prompt**（Opus 4.8约290/410 token）。这正是缓存稳定前缀重要的原因。
- 来源：Anthropic prompt-caching / tool-use overview / agent-sdk文档；OpenAI prompt caching blog。
- ⚠️ 传闻：claude-code #46829称2026年3月初默认缓存TTL从1h悄悄退回5m，社区说法未官方确认。

## 5. API计费 vs 订阅（成本差多少）

### API按量价（2026, USD/MTok 输入/输出）[官方]
- Claude Opus 4.5–4.8：$5 / $25（缓存读$0.50）。从Opus 4/4.1的$15/$75砍了~67%。所有Claude层都是**5:1**输出输入比。注：Opus 4.7+新分词器同样文本可能多耗35% token（隐性涨价）。
- Claude Sonnet 4.5/4.6：$3 / $15。Haiku 4.5：$1 / $5。
- GPT-5.5（旗舰,2026-04-23）：$5 / $30（缓存$0.50）。GPT-5.4：$2.50 / $15。GPT-5.5比5.4翻倍。
- Gemini 3.1 Pro：≤200k $2/$12，>200k $4/$18（**上下文分层定价**，区别于Claude/OpenAI平价）。
- 三家batch都5折。

### 订阅与隐性补贴
- Claude Pro ~$20/mo；Max 5x $100；Max 20x $200。ChatGPT Plus $20 / Pro $200。
- 限额=滚动**5小时窗口**+**周上限**（Anthropic不公布精确token数）。Pro约45 prompts/5h；Max约225–900 msg/5h[报道]。
- **补贴头条数字**：
  - [报道/轶事] 一开发者8个月在Claude Code Max烧~100亿token，API价值$15,000+，只付~$800订阅费。
  - [报道，区间] Max 20x($200)满用估算消耗$600–$8,000/mo API等价；ChatGPT Pro($200)理论上限~$14,000/mo。
  - [报道] Anthropic自述：agent在flat-rate登录上提取**12–175倍**补贴。
  - 回本经验：Max 20x约$6.67/天API等价回本；聊天用<5M输入token/mo订阅划算，生产/agent负载通常API更便宜。
- **机制**：①订阅按平均用户定价，重度用户被轻度用户交叉补贴；②限速作为成本上限（5h窗口+周上限+公平使用）。
- **2026政策收紧（已记录事件）**：4月Anthropic限制第三方工具消耗flat-rate；5月中宣布、**6月15日生效**：订阅用量拆**两池**——交互用走正常订阅限额，计量/超额走**按标准API token价计费的credit池**。直接回应补贴套利。

## 6. token中转站的秘密

- 定义：夹在开发者和官方基础设施之间的第三方代理，收**OpenAI兼容格式**请求转发。中国流行因官方门槛高（支付/网络/访问限制）。价格常**比官方低70–90%**，低至官方~10%（"1元285万token"广告）。
- **"一鱼三吃"价差来源**：
  - 吃法1 接入套利：批量注册薅$5免费额度；倒卖闲置quota；企业/教育/批发价套利；**APImaxxing**——把一个$200 Max订阅按token/小时配额拆给多人转售；**逆向端点**——逆向ChatGPT/Claude/Cursor客户端协议重新包装成"API"（最便宜最脆，厂商一更新风控就挂）；盗刷信用卡开户。
  - 吃法2 **换模型/降智**：显示`claude-opus-4.x`后台偷偷跑Sonnet/Haiku/GLM/Qwen甚至7B；高峰期切换；偷偷**缩短上下文窗口**省钱（"模型变笨"主因）。**CISPA审计(2026年3月)**[最强证据]：24个端点45.83%通不过模型指纹验证；"Gemini-2.5"代理医学基准37.00% vs官方83.82%。
  - 吃法3 **数据收割**：全量明文记录prompt/回复/工具调用/思维链，卖作训练数据；HuggingFace上来源不明的"Claude数据集"。
- **风险**：①数据记录泄露（代码/业务文档被卖）；②降智（付Opus价拿Sonnet/量化/开源）；③恶意代码窃密（Aikido发现npm/PyPI "GPT-Proxy"后门外传API key/AWS凭证/GitHub token/加密私钥）；④不稳定+**跑路**生命周期（低价送额度→引流→涨价掉质→封投诉者→域名消失余额清零）；⑤封号（账号池薄触发风控）；⑥法律风险（[单一报道]2026年5月上海一中转站运营者因非法获取API被刑拘37天）。
- 来源：ChinaTalk "how to buy cheap claude tokens"（CISPA+一鱼三吃）；Aikido凭证窃取；腾讯云深度指南；知乎45%假模型审计；stcn跑路+刑拘。

## 7. 三种API接口差异

### OpenAI Chat Completions `/v1/chat/completions`（事实标准，无状态）
- `messages`数组，role=system(新模型developer)/user/assistant/tool；客户端每轮回灌完整历史。
- `tools`数组：`{type:"function", function:{name,description,parameters(JSON Schema)}}`。
- 工具调用：assistant message带`tool_calls`，`function.arguments`是**JSON字符串**（要parse）。工具结果作为**新消息**`{role:"tool", tool_call_id, content}`回灌。
- 响应：`choices[0].message.content`，`finish_reason`(stop/length/tool_calls/content_filter)。
- usage：`prompt_tokens`/`completion_tokens`/`total_tokens`，缓存在`prompt_tokens_details.cached_tokens`。
- **为什么成通用标准**：可移植——改`base_url`就能指向自建/第三方。vLLM、Ollama、LiteLLM都暴露这个形状。

### Anthropic Messages `/v1/messages`（开箱不兼容OpenAI）
- system是**顶层独立参数**不进messages；content是string或**block数组**；`max_tokens`**必填**；role只有user/assistant（**没有独立tool role**）。
- content blocks：`text`/`tool_use`(input是**真JSON对象**)/`tool_result`(放在`role:"user"`消息的content里，靠`tool_use_id`关联)/`thinking`(带signature)/image/document。
- 工具定义顶层`tools`：`{name,description,input_schema}`——是`input_schema`不是嵌套`function.parameters`。
- usage更丰富：input_tokens/output_tokens+cache_creation_input_tokens+cache_read_input_tokens+output_tokens_details.thinking_tokens。**注意`input_tokens`=最后断点之后未命中的token**，总输入=cache_read+cache_creation+input_tokens（与OpenAI的`prompt_tokens`=总输入语义不同）。
- 扩展思考：`thinking:{type:"enabled",budget_tokens:N}`；多轮/工具时**必须原样回传thinking block**否则推理连续性丢失。
- stop_reason（非finish_reason）：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal。

### OpenAI Responses `/v1/responses`（新的有状态API，Chat Completions前向替代但未弃用后者）
- `input`(字符串或Item数组)+顶层`instructions`(≈system)；`max_output_tokens`；`output`是typed item数组(message/reasoning/function_call/function_call_output)，便捷字段`output_text`。
- **有状态**：`previous_response_id`链接上次响应，`store`默认true留存30天。函数调用靠`call_id`关联。
- **推理连续性（核心动机）**：跨轮自动访问之前的reasoning items保留思考链（OpenAI自报GPT-5经Responses在TAUBench高~5%）。reasoning token计入output_tokens，`output_tokens_details.reasoning_tokens`单列。
- 内置server-side工具：web search/file search/code interpreter/MCP。
- 加密推理退路：`store:false`+`include:["reasoning.encrypted_content"]`，既无状态又保推理连续性，原始思考链对客户端隐藏。
- 动机：模型从纯补全演化成多模态推理+工具调用agent，单一content字符串+客户端手搓状态不够用了。

### 中转站只暴露Chat Completions形状，翻译丢了什么
- **prompt caching失效/不可控**：`cache_control`断点、cache_creation/cache_read在OpenAI形状里无对应字段，要么不透传断点(成本上升)，要么usage只有一个`prompt_tokens`(缓存读写区分丢失)。
- **thinking/reasoning丢失降级**：thinking block+signature、Responses reasoning item在Chat Completions里没标准位置，常塞进`content`或非标`reasoning_content`，signature往往丢掉→**跨轮推理连续性断裂**。
- **原生工具语义抹平**：`tool_use.input`(对象)被迫序列化成`arguments`(字符串)；tool结果从"user消息里的block"改写成"独立tool消息"；server-side内置工具、有状态`previous_response_id`无法表达。
- 一句话：用Chat Completions当最小公分母换普适兼容，代价是把各家高级能力（缓存经济性、思考连续性、原生工具/有状态语义）降维。

## 8. coding agent的KV缓存工程（新增章节素材，2026-06-29二轮调研）

### claude-code（正面教材，源码探查 C:\Users\kvenu\playground\claude-code）
- 系统提示词显式切静态/动态两段，边界标记 `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__`（src/constants/prompts.ts:114-115, 560-577）。
- 静态前缀：身份"You are an interactive agent..."、工具用法、行为规则、输出风格——整场/跨会话不变。
- 动态尾巴：session_guidance、MEMORY.md、env_info（cwd/git/platform/model id）、language、output_style、MCP说明（带DANGEROUS_uncachedSystemPromptSection因服务器会连断）、scratchpad等。
- 缓存断点打在边界：splitSysPromptPrefix()(src/utils/api.ts:321-400)边界前 cacheScope:'global'、后 null；buildSystemPromptBlocks()(src/services/api/claude.ts:3213-3237)给静态块挂 cache_control:{type:'ephemeral',scope:'global'}。
- 设计文档 system-prompt-design.md:154-156：静态段在个性化开始前结束，"95%+ 系统提示词token命中缓存"。
- 代码注释警告：别移动/重排边界标记，否则缓存逻辑废（prompts.ts:110-112）。
- 有 promptCacheBreakDetection.ts：命中率掉>5%或>2000token就记 tengu_prompt_cache_break，区分客户端改动/TTL过期/服务端驱逐。

### opencode（确证的反面案例）
- packages/opencode/src/session/system.ts 的 environment() 把 `Today's date: ${new Date().toDateString()}` 放进被缓存前缀。
- issue #29672：过午夜该字段变→后续所有token缓存miss。建议拿掉日期或把更稳定的skill列表排到env前。https://github.com/sst/opencode/issues/29672
- issue #5224：同块还列最多~200个工作目录文件，文件增删→前缀变→成本上升。https://github.com/sst/opencode/issues/5224
- **精度纠正**：日期粒度（午夜翻天+上下文变化才失效），不是每请求都变。
- **别张冠李戴**：$0.12→$0.016(降87%)那组数来自 opencode 走第三方代理没传 promptCacheKey 的另一个问题，不是时间戳bug。

### oh-my-opencode（更极端形态，但被部分推翻）
- opencode 的插件/编排层，作者 code-yeongyu，已改名 oh-my-openagent。https://github.com/code-yeongyu/oh-my-openagent
- issue #1247：报告者称插件注入每秒变的"当前时间"+Math.random()/Date.now()随机消息ID→0%命中 vs 关插件~49-50%；session成本 $0.0848 vs $0.0213。https://github.com/code-yeongyu/oh-my-openagent/issues/1247
- **关键：报告者自己部分推翻**——静态化后仍0%；又发现插件开着也能命中；疑似首次测量混用模型(Model: approx)导致误读；issue无定论关闭，无fix PR。
- 教训定位：佐证"缓存命中率极易误判"；原理（每请求变的东西混进前缀→为整段历史反复付全价）独立成立。
- 一般原理来源：Anthropic prompt-caching docs；OpenAI "Prompt Caching 201"；arXiv "Don't Break the Cache" 2601.06007。

## 9. 本机实测：订阅 vs API 等价成本（作者第一人称数据，已写入第七节佐证）

两个 $200/月 的 20× 订阅（Codex + Claude Code），按官方 API list price 折算等价成本，除以 $200 得倍数。**不打折、不合计**——窗口平均只用六七成没跑满，所以实测倍数是地板，再按利用率折算满载估算。满载倍数 = 等价成本 ÷ 利用率 ÷ $200。

| 工具 | 统计区间(Asia/Shanghai) | 实测token | 等价API成本 | 实测倍数(地板) | 窗口利用率 | 估算满载倍数 |
|---|---|---|---|---|---|---|
| Claude Code | 2026-05-29~06-29 | 7,433,932,701 (74.3亿) | $6,729.39 | ≈33.6×(文中≈34×) | ~60% | $6,729/0.6/200 ≈ 56× |
| Codex | 2026-05-11~06-10 | 12,013,209,621 (120.1亿) | $9,535.14 | ≈47.7×(文中≈48×) | ~80% | $9,535/0.8/200 ≈ 60× |

Claude 成本拆分：input $79.85 / cache write $1,901.58 / cache read $3,733.56(7,162M tokens,占55%) / output $1,014.40。按模型：Opus 4.8 $5,632.89、Fable 5 $586.17、Opus 4.7 $451.83、Sonnet 4.6 $37.07、Haiku 4.5 $21.43。

Codex 成本：gpt-5.5 $9,460.80（$5/$0.50/$30 per MTok）、gpt-5.3-codex-spark $74.34（无公开单价，按 gpt-5.3-codex $1.75/$0.175/$14 代理估算，Spark 是 research preview）。

口径：Claude 扫 `C:\Users\kvenu\.claude\projects\**\*.jsonl` 含子agent，窗口内 usage 行 101,370，按 requestId 去重 42,591 次请求 / 475 session / 2,111 文件；WSL 下为 0。Codex 扫 Windows+WSL 的 `.codex/sessions`，用 last_token_usage 增量避免累计型重复。

要点（呼应文章）：cache read 是 Claude 最大单项($3,733,55%)，7,162M cache-read token 若按全价 input 值约 $37,335——补贴里缓存功不可没；佐证了第七节"12–175× 补贴"的网上说法，作者实测落在偏保守的三四十倍档。
