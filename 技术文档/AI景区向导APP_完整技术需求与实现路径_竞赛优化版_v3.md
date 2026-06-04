# AI 景区向导 APP - 完整技术需求与实现路径（竞赛优化版 v3.0）

> **版本**: v3.0 | **日期**: 2026-05-28  
> **对标赛题**: AI 数字人景区导览服务系统  
> **核心升级**: 三模态交互（语音+文本+表情）| 个性化路线讲解 | 深度游客洞察 | 情感互动融合 | 数字人形象管理 | 知识库全生命周期管理

---

## 一、项目概述

### 1.1 赛题对接矩阵

#### 游客交互侧需求映射

| 赛题要求 | 本方案对应模块 | 实现方式 | 验证标准 |
|---------|--------------|---------|---------|
| **多模态交互**: 支持语音输入和文本输入，数字人以语音、表情和口型同步方式回答 | 前端 APP + Live2D 数字人 + FunASR + QwenTTS | 语音输入（FunASR本地识别）+ 文本输入（Flutter输入框）; 数字人输出: 语音（QwenTTS）+ 表情（Live2D情感驱动）+ 口型同步（双参数RMS+频谱比） | 专家评估自然度 |
| **智能问答与讲解**: 准确回答景区历史、文化、景点特色等常见问题 | RAG知识库 + Qwen2.5 LLM | BGE-M3本地嵌入 + ChromaDB语义检索 + LangChain上下文组装; 知识库覆盖灵山胜境16景点+拈花湾6景点的历史/文化/特色/建筑参数 | 事实性问答准确率 >= 90% |
| **个性化推荐**: 根据游客兴趣（如'对历史感兴趣'或'喜欢自然风光'）推荐不同游览路线和讲解重点 | **路线推荐引擎 + 讲解重点适配** | 基于游客画像（年龄/性别/同行人数/兴趣标签）+ 景点知识库分类（佛教文化/自然景观/非遗艺术/人文历史）-> 生成个性化路线 + 动态调整讲解重点 | 路线相关性评分 + 用户反馈 |

#### 管理后台侧需求映射

| 赛题要求 | 本方案对应模块 | 实现方式 |
|---------|--------------|---------|
| **知识库管理**: 管理员可上传、更新和维护景区的讲解词、文史资料、常见问题及答案等知识文档 | Vue3管理后台 - 知识库管理页 | 支持Markdown/Word/Excel上传; 自动分块 -> BGE-M3重新Embedding; 讲解词版本控制; FAQ独立维护表 |
| **数字人形象管理**: 可配置数字人的外观、服装、声音等，使其更贴合景区文化特色 | Vue3管理后台 - 数字人配置页 + 前端动态加载 | Live2D模型参数配置（服装贴图切换/声音音色选择/景区主题皮肤）; 支持多套形象方案（禅意主题/佛教主题/现代主题） |
| **游客感受度报告**: 系统能分析交互记录，生成游客关注点分析、情感趋势报告及服务建议反馈给管理方 | **游客洞察平台** | 基于14万条行为数据 + 对话情感数据 -> 关注点词云/情感趋势折线图/服务建议自动生成（LLM总结） |
| **数据大屏概览**: 展示当日/本周服务人次、热门问答、游客满意度趋势等核心运营数据 | Vue3数据大屏页 | ECharts实时图表: 服务人次柱状图/热门问答TOP10/满意度趋势折线图/情感分布饼图; WebSocket实时推送 |

#### 非功能性需求映射

| 赛题要求 | 本方案保障措施 | 指标 |
|---------|-------------|------|
| **至少使用1个多模态大模型作为核心AI能力支撑** | **Qwen2.5-14B/72B** 作为核心多模态大模型; 同时调用其文本理解、情感分析、路线生成能力 | 模型版本: Qwen2.5-14B-Instruct/72B-Instruct via DashScope |
| **构建本地景区知识库，确保回答准确性和自然度** | BGE-M3本地部署 + ChromaDB向量库; 导入比赛提供的灵山胜境/拈花湾结构化数据 + 游览指南文档 | 本地向量库 + 结构化数据双保险 |
| **准确度**: 事实性问答准确率不低于90% | RAG检索增强 + 结构化数据直接查询 + Prompt约束（要求基于知识库回答） | >= 90% |
| **自然度**: 口型同步、语音合成、表情配合等由专家评估 | 双参数口型同步（RMS+频谱比）+ Qwen3-TTS情感语音 + Live2D 5种情感表情Lerp过渡 | 专家演示视频评估 |
| **系统稳定，交互响应延迟<5秒** | FastAPI异步架构 + Redis缓存 + Uvicorn多worker + 本地模型减少网络延迟 | 语音问答端到端 < 5s |
| **稳定性**: 系统不应出现崩溃或长时间无响应 | Docker容器化部署 + 健康检查 + 自动重启 + 异常降级策略（本地模型兜底） | 7x24稳定运行 |


### 1.2 核心形态

| 项 | 说明 |
|----|------|
| **核心形态** | Flutter Android APP + FastAPI 后端 + 混合 AI 架构（本地+云端） |
| **交互方式** | **三模态闭环**: 语音/文本输入 -> AI 导游回答 -> **语音输出 + 文本展示 + Live2D 表情+口型同步** |
| **多模态范围** | **语音 + 文字 + 表情（口型+面部）**（不加入图片识别） |
| **AI 架构** | 本地模型（FunASR + BGE-M3 + ChromaDB）+ 云端多模态大模型（**Qwen2.5** + QwenTTS） |
| **竞赛加分重点** | **(1) Live2D数字人自然度（口型+表情+Idle+形象管理）** | **(2) 语音-文本双通道情感融合** | **(3) 个性化路线+讲解重点推荐** | **(4) 游客感受度报告+数据大屏** | **(5) 知识库全生命周期管理** |

---

## 二、整体架构

```
+-------------------------------------------------------------+
|  用户手机（Flutter + Android Native）                       |
|  +- Live2D Cubism SDK: 双参数口型 + 情感表情 + Idle动画       |
|  +- **数字人形象配置**: 服装贴图/声音音色/主题皮肤动态切换      |
|  +- speech_to_text: 本地语音输入(FunASR)                      |
|  +- 文本输入框: 快捷问题推荐 + 景点手动选择        |
|  +- audioplayers: 播放TTS音频(Qwen3-TTS)                     |
|  +- sqflite: 离线对话缓存 + 本地路线缓存 + 数字人配置缓存       |
|  +- **路线推荐页**: 个性化游览路线（时间轴+景点卡片+讲解重点）  |
+-------------------------------------------------------------+
|  服务器（推荐 4核8G+）                                       |
|  +- Docker: FastAPI（多worker）                             |
|  +- Docker: PostgreSQL 15（景点+游客行为+FAQ+数字人配置）       |
|  +- Docker: Redis（缓存+会话+限流+TTS缓存）                   |
|  +- Docker: ChromaDB（向量数据库-景区知识库）                   |
|  +- 本地部署: FunASR SenseVoice-Small（语音识别+语音情感）      |
|  +- 本地部署: BGE-M3（文本嵌入-RAG核心）                       |
|  +- 本地部署: 路线推荐算法（规则+协同过滤）                     |
|  +- 云端调用: DashScope 百炼 API                              |
|      +- **Qwen2.5-14B/72B: 多模态核心大模型**                  |
|         （导游问答+文本情感分析+路线生成+服务建议总结）         |
|      +- Qwen3-TTS: 语音合成（支持情感参数注入）                |
|      +- （可选）Qwen-VL: 预留扩展接口                          |
+-------------------------------------------------------------+
|  管理后台（Vue3 + ElementPlus + ECharts）                    |
|  +- 知识库管理: 讲解词/文史资料/FAQ上传维护+重新Embedding       |
|  +- 数字人形象管理: 外观/服装/声音/主题配置                     |
|  +- 游客感受度报告: 关注点分析+情感趋势+服务建议                 |
|  +- 数据大屏: 服务人次/热门问答/满意度趋势实时展示               |
+-------------------------------------------------------------+
```

---

## 三、各层技术需求与实现路径

### 3.1 前端 APP 层（Flutter + Live2D）

#### 3.1.1 技术清单

| 技术 | 版本 | 用途 |
|------|------|------|
| **Flutter SDK** | 3.19+ | 跨平台框架，仅构建 Android APK |
| **Dart** | 3.3+ | 空安全语法，异步 Future/Stream |
| **Live2D Cubism SDK Native** | 4.2+ | Android端模型渲染（PlatformView）+ **形象动态切换** |
| **speech_to_text** | 6.0+ | 本地语音识别，按住说话，动态权限申请 |
| **audioplayers** | 5.0+ | 播放TTS音频，获取播放状态与音量回调 |
| **dio** | 5.0+ | HTTP请求后端API，支持拦截器、超时、重试 |
| **shared_preferences** | 2.0+ | 本地轻量存储: 游客ID、语音设置、**数字人形象配置**、首次启动标记 |
| **sqflite** | 2.3+ | 本地SQLite: 离线缓存对话记录 + 路线缓存 + **数字人配置缓存** |

#### 3.1.2 三模态交互界面设计

| 模态 | 输入/输出 | 交互组件 | 说明 |
|------|----------|---------|------|
| **语音** | 输入 | 底部麦克风按钮（按住说话） | FunASR本地识别，支持方言降噪 |
| **语音** | 输出 | 音频播放器 + Live2D口型同步 | QwenTTS音频URL，双参数口型驱动（RMS+频谱比） |
| **文本** | 输入 | 底部文本输入框 | 支持快捷问题推荐、景点手动选择 |
| **文本** | 输出 | 对话气泡（Markdown渲染） | 支持景点卡片、路线卡片、讲解重点高亮 |
| **表情** | **输出** | **Live2D数字人面部** | **独立模态**: 根据情感融合结果实时反馈5种表情（happy/sad/surprised/confused/neutral） |

> **关键设计**: 数字人表情不仅是'情感装饰'，而是**独立的反馈模态**。当系统识别到游客情绪消极时，数字人通过 `sad` 表情 + 安慰性语音同步输出，实现真正意义上的'情感互动'。

#### 3.1.3 数字人形象管理（贴合景区文化特色）

**形象配置维度**:

| 维度 | 配置项 | 实现方式 | 景区适配 |
|------|--------|---------|---------|
| **外观** | 服装贴图 | Live2D模型多贴图切换 | 禅意主题（素色僧袍风格）/ 佛教主题（金色袈裟风格）/ 现代主题（休闲导游风格） |
| **声音** | 音色/语速/语调 | Qwen3-TTS参数配置 | 温暖女声（默认）/ 沉稳男声 / 童声（亲子模式） |
| **主题** | 背景/边框/UI色调 | Flutter主题切换 | 禅意青（默认）/ 佛教金 / 自然绿 |
| **讲解风格** | 文案风格 | LLM Prompt动态切换 | 学术严谨型 / 轻松故事型 / 亲子互动型 |

**配置存储与同步**:

```dart
// 本地缓存 + 后端同步
class AvatarConfig {
  String costumeTheme;      // 'zen' | 'buddhist' | 'modern'
  String voiceType;         // 'warm_female' | 'calm_male' | 'child'
  String uiTheme;           // 'zen_cyan' | 'buddhist_gold' | 'nature_green'
  String speechStyle;       // 'academic' | 'story' | 'family'
  double voiceSpeed;        // 0.8 ~ 1.2
}
```

**Flutter加载逻辑**:

```dart
// 启动时从后端拉取配置，fallback到本地默认
final config = await AvatarConfigService.load();
await platform.invokeMethod('loadModel', {
  'path': 'assets/hiyori',
  'costume': config.costumeTheme,  // 切换贴图
  'theme': config.uiTheme          // 通知Flutter UI层
});
```


#### 3.1.4 Live2D 数字人详细规范（竞赛加分重点）

**模型参数要求**（需在 `model3.json` 中确认）:

| 参数 ID | 作用 | 范围 | 必要性 |
|---------|------|------|--------|
| `ParamMouthOpenY` | 嘴巴开合程度 | 0.0 ~ 1.0 | **必须** |
| `ParamMouthForm` | 嘴巴形状（圆嘴/咧嘴） | -1.0 ~ 1.0 | **强烈建议** |
| `ParamEyeLOpen` / `ParamEyeROpen` | 左右眼睁开 | 0.0 ~ 1.0 | 必须 |
| `ParamBrowLY` / `ParamBrowRY` | 左右眉毛 Y 轴 | -1.0 ~ 1.0 | 必须（表情） |
| `ParamAngleX` / `ParamAngleY` | 头部转动 | -30 ~ 30 | 建议（视线跟随） |
| `ParamBreath` | 呼吸起伏 | 0.0 ~ 1.0 | 建议 |
| Physics (`.physics3.json`) | 头发/衣服物理飘动 | -- | 建议 |

**口型同步方案（双参数驱动）**:

| 驱动参数 | 音频特征源 | 映射逻辑 |
|----------|-----------|----------|
| **ParamMouthOpenY** | **RMS 能量**（响度） | 音量大 -> 嘴张得大; 平滑过渡（低通滤波系数 0.25） |
| **ParamMouthForm** | **频谱高频/低频能量比** | 高频多（嘶/咦）-> 偏向 1（咧嘴）; 低频多（啊/哦）-> 偏向 -1（圆嘴）; 平滑系数 0.15 |

**自然动画系统**:

| 动画类型 | 实现方式 | 参数 |
|----------|----------|------|
| **呼吸** | 正弦波循环 | `ParamBreath = 0.5 + 0.5 * sin(t / 3.2345)`，周期约 3 秒 |
| **眨眼** | 随机间隔触发 | 间隔 2~6 秒随机，闭眼动画 150ms |
| **头部微动** | Idle 状态正弦叠加 | `ParamAngleX = sin(t/5)*3deg`，`ParamAngleY = sin(t/7)*2deg` |
| **物理飘动** | Cubism Physics 引擎 | 自动更新，需模型绑定 `ParamHairFront` 等 |
| **视线跟随** | 触摸事件映射 | 手指坐标 -> 归一化 -> `ParamAngleX/Y` |

**情感-表情联动映射（三模态核心）**:

| 情感标签 | 眉毛 | 眼睛 | 嘴型 | **联动语音/文本** | 说明 |
|----------|------|------|------|------------------|------|
| `happy` | 上扬 (-0.3) | 明亮 (1.0) | 微笑 (0.5) | 轻快语调 + 积极文案 | 开心、满意 |
| `sad` | 下垂 (+0.5) | 黯淡 (0.6) | 下撇 (-0.2) | 舒缓语调 + 安慰文案 | 失望、疲惫 |
| `surprised` | 高挑 (-0.5) | 睁大 (1.0) | 微张 (0.0) | 惊叹语调 + 详细讲解 | 惊讶、赞叹 |
| `confused` | 不对称 (+0.2/-0.2) | 半眯 (0.8) | 平直 (0.0) | 放慢语速 + 引导式提问 | 疑惑、思考 |
| `neutral` | 默认 (0.0) | 正常 (1.0) | 自然 (0.0) | 标准讲解语调 | 常规讲解 |

> **过渡要求**: 表情切换必须使用插值（Lerp），过渡时间 0.3~0.5 秒，禁止瞬间跳变。

#### 3.1.5 新增: 个性化路线展示页 + 讲解重点适配

| 组件 | 功能 | 数据来源 |
|------|------|---------|
| **路线时间轴** | 纵向时间轴展示推荐游览顺序 | 后端 `/route/recommend` 返回 |
| **景点卡片** | 景点缩略图 + 名称 + 建议停留时长 + **讲解重点标签** | 知识库 `attractions` 表 |
| **讲解重点** | 根据游客兴趣动态高亮（如'历史爱好者'高亮文化典故） | LLM根据画像动态生成 |
| **预估信息** | 总时长、总步行距离、预估消费 | 基于知识库 + 游客行为数据统计 |
| **景点手动选择** | 下拉选择当前所在景点（**备选方案**） | 知识库景点列表 |
| **一键导航** | 调用系统地图APP（外部跳转） | 不内置地图，减少包体积 |

#### 3.1.6 Flutter <-> Native 通信接口

```dart
const platform = MethodChannel('com.yourteam.live2d');

// 基础方法
await platform.invokeMethod('loadModel', {'path': 'assets/hiyori', 'costume': 'zen'});
await platform.invokeMethod('speak', {'audioUrl': url, 'emotion': 'happy', 'intensity': 0.9});
await platform.invokeMethod('stopSpeaking');
await platform.invokeMethod('setLookAt', {'x': 0.5, 'y': 0.3});
await platform.invokeMethod('setExpression', {'emotion': 'surprised', 'intensity': 0.8});
```

#### 3.1.7 实现路径

| 天数 | 任务 | 产出 |
|------|------|------|
| 1-3 | 素材准备: 获取 Live2D 模型（推荐官方 Hiyori），确认参数完整; 准备**多套服装贴图**（禅意/佛教/现代） | 可用 `.model3.json` + `.moc3` + 多组贴图 |
| 4-7 | Native 渲染层: Android 集成 Cubism SDK，GLSurfaceView/TextureView 加载模型，启用 Physics 更新，基础渲染循环 | Flutter PlatformView 能显示会呼吸的小人 |
| 8-12 | 口型同步引擎: AudioTrack + Visualizer 实时取音频 PCM，计算 RMS -> `ParamMouthOpenY`，计算频谱比 -> `ParamMouthForm`，加平滑滤波 | 播放测试音频时嘴型与音量/音色匹配 |
| 13-15 | **三模态表情系统**: 定义情感参数映射表，实现插值过渡器，对接后端 `emotion` + `intensity` 字段; 表情作为独立模态与语音/文本同步输出 | 切换情感时眉毛眼神自然变化 |
| 16-18 | Idle 细节 + **形象切换**: 随机眨眼、头部微动、视线跟随触摸、物理飘动; 服装贴图动态切换逻辑 | Idle 状态生动不僵硬; 可切换主题 |
| 19-21 | **路线展示页 + 景点手动选择**: 时间轴 UI、景点卡片、讲解重点高亮、预估信息、手动选择景点 | 前端可展示个性化路线 |
| 22-24 | 联调: 对接后端 QwenTTS 音频 URL + 情感融合字段 + 路线推荐数据 + 形象配置数据，端到端测试 | 完整交互链路可用 |


### 3.2 后端服务层（Python / FastAPI）

#### 3.2.1 技术清单

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.10+ | 开发语言，类型注解，async/await |
| **FastAPI** | 0.110+ | 高性能 Web 框架，异步 API，自动 Swagger 文档 |
| **Uvicorn** | 0.27+ | ASGI 服务器，推荐 `--workers 2`（4核）或 `--workers 4`（8核） |
| **Pydantic** | 2.0+ | 请求/响应数据校验与序列化 |
| **SQLAlchemy** | 2.0+ | ORM，使用 `AsyncSession` + `asyncpg` 驱动 |
| **Alembic** | 1.13+ | 数据库迁移管理 |
| **PyJWT** | 2.8+ | 管理后台 Token 鉴权，HS256，24h 有效期 |
| **python-multipart** | 0.0.9+ | 接收 Flutter 上传的语音文件 / 知识库文档 |
| **Redis-py** | 5.0+ | 连接 Redis，缓存热点数据、会话状态、限流 |
| **APScheduler** | 3.10+ | 定时任务: 每日凌晨生成游客感受度报告 |
| **pandas** | 2.0+ | 游客行为数据分析 + 报告生成 |
| **scikit-learn** | 1.4+ | 路线推荐协同过滤 + 游客画像聚类 |
| **python-docx / openpyxl** | 最新 | 知识库文档解析（Word/Excel上传） |

#### 3.2.2 API 路由设计

**游客交互接口**:

| 接口 | 方法 | 请求 | 响应 | 说明 |
|------|------|------|------|------|
| `/chat` | POST | `{'user_id', 'message'}` | `{'text', 'audio_url', 'emotion', 'intensity'}` | 文本问答，含融合情感 |
| `/chat/stream` | POST | 同上 | SSE 流 | 流式输出（提升体验） |
| `/voice/upload` | POST | `multipart/form-data` 音频文件 | `{'text', 'audio_url', 'emotion', 'intensity', 'debug'}` | 语音识别 -> 问答 -> TTS，含双通道情感融合 |
| `/route/recommend` | POST | `{'user_id', 'age', 'gender', 'group_size', 'interests': ['历史', '自然风光']}` | `{'route': [...], 'total_duration', 'estimated_cost', 'speech_highlights': {...}}` | 个性化路线 + 讲解重点推荐 |
| `/route/detail/{id}` | GET | -- | 景点详情 + 游玩建议 + **讲解词（按兴趣标签过滤）** | 路线节点详情 |
| `/avatar/config` | GET/POST | `{'user_id'}` / `{'costume', 'voice', 'theme', 'style'}` | 数字人形象配置 | 游客端形象拉取/更新 |
| `/attractions/list` | GET | Query: `scenic_area` | 景点列表（用于手动选择） | 备选方案 |

**管理后台接口**:

| 接口 | 方法 | 说明 |
|------|------|------|
| `/admin/login` | POST | JWT 鉴权登录 |
| `/admin/stats` | GET | 统计数据: 服务人次/活跃用户数/情感分布/路线使用/满意度 |
| `/admin/conversations` | GET | 对话管理: 支持情感筛选 + 双通道来源展示 |
| `/admin/insights` | GET | 游客洞察: 年龄/性别/消费/满意度/情感多维分析 |
| `/admin/kb/upload` | POST | **知识库上传**: 讲解词/文史资料/FAQ文档（Markdown/Word/Excel） |
| `/admin/kb/documents` | GET/PUT/DELETE | **知识库管理**: 文档CRUD + 分块状态查看 + 触发重新Embedding |
| `/admin/kb/faq` | GET/POST/PUT/DELETE | **FAQ独立管理**: 常见问题及答案的独立维护 |
| `/admin/avatar/presets` | GET/POST/PUT/DELETE | **数字人形象管理**: 外观/服装/声音/主题配置方案CRUD |
| `/admin/reports/sentiment` | GET | **游客感受度报告**: 关注点分析 + 情感趋势 + 服务建议（LLM自动生成） |
| `/admin/dashboard/realtime` | GET | **数据大屏**: 当日/本周服务人次、热门问答TOP10、满意度趋势 |

#### 3.2.3 情感融合核心逻辑

```python
def fuse_emotion(voice_emotion: str, text_sentiment: str, text_confidence: float) -> dict:
    emotion_map = {
        'happy': 'happy', 'sad': 'sad', 'angry': 'angry',
        'neutral': 'neutral',
        '积极': 'happy', '消极': 'sad', '中性': 'neutral'
    }
    v = emotion_map.get(voice_emotion, 'neutral')
    t = emotion_map.get(text_sentiment, 'neutral')

    # 融合规则: 文本为主（70%权重），语音为辅（30%权重）
    if v == 'angry' or t == 'sad':
        final = 'sad'; intensity = 0.9 if v == 'angry' else 0.7
    elif v == 'happy' and t == 'happy':
        final = 'happy'; intensity = 0.95
    elif t == 'happy':
        final = 'happy'; intensity = 0.75
    else:
        final = 'neutral'; intensity = 0.5

    return {'emotion': final, 'intensity': intensity, 'sources': {'voice': v, 'text': t}}
```

#### 3.2.4 个性化路线推荐 + 讲解重点适配

```python
class RouteRecommendationService:
    def recommend(self, user_profile: dict, interests: list) -> dict:
        # 1. 兴趣标签映射到景点属性
        #    '历史' -> 祥符禅寺、阿育王柱、无尽意斋（侧重文化典故）
        #    '自然风光' -> 梵天花海、五灯湖、鹿鸣谷（侧重景观美学）
        #    '佛教文化' -> 灵山大佛、九龙灌浴、灵山梵宫、五印坛城（侧重宗教内涵）
        #    '非遗艺术' -> 灵山梵宫（东阳木雕/琉璃/油画）、曼飞龙塔（傣族雕刻）
        #    '亲子' -> 百子戏弥勒、九龙灌浴（互动性强）

        # 2. 画像匹配（年龄/性别/同行人数）
        #    亲子家庭 -> 优先百子戏弥勒、九龙灌浴，讲解风格切换为'亲子互动型'
        #    老年游客 -> 优先祥符禅寺、无尽意斋，减少步行，讲解风格'学术严谨型'
        #    年轻情侣 -> 优先五灯湖夜景、梵天花海，讲解风格'轻松故事型'

        # 3. 讲解重点适配（按兴趣标签动态生成）
        #    每个景点返回 'speech_highlight' 字段，LLM根据兴趣生成侧重内容
        #    例如: 九龙灌浴 + 历史兴趣 -> 侧重《本行经》诞生传说
        #    例如: 九龙灌浴 + 艺术兴趣 -> 侧重180吨耗铜量、鎏金工艺

        # 4. 时序排序 + 时长预估
        return {
            'route': [...],  # 含 attraction_id, name, duration, order, highlights
            'speech_highlights': {'LS-006': '侧重佛教诞生传说...', ...},
            'total_duration': '4.5小时',
            'estimated_cost': {'ticket': 210, 'food': 230, 'shopping': 240},
            'speech_style': 'story',  # 根据画像自动选择
            'tips': '建议上午9:00入园，先观看10:00九龙灌浴表演'
        }
```

#### 3.2.5 `/voice/upload` 完整链路（延迟<5秒保障）

```python
@app.post('/voice/upload')
async def handle_voice(file: UploadFile):
    # 1. 保存音频（<100ms）
    path = f'/tmp/{file.filename}'
    with open(path, 'wb') as f: f.write(await file.read())

    # 2. FunASR: 语音识别 + 语音情感（本地，<800ms）
    asr_result = asr_service.transcribe(path)
    text = asr_result['text']
    voice_emo = asr_result.get('emotion', 'neutral')

    # 3. RAG检索: BGE-M3嵌入 -> ChromaDB（本地，<500ms）
    context_docs = rag_service.retrieve(text, k=3)

    # 4. LLM: 导游问答 + 文本情感分析（云端，<2s）
    llm_response = llm_service.chat_with_sentiment(text, context=context_docs)
    answer = llm_response['answer']
    text_emo = llm_response['sentiment']
    confidence = llm_response['confidence']

    # 5. 双通道情感融合（本地，<10ms）
    final_emotion = fuse_emotion(voice_emo, text_emo, confidence)

    # 6. QwenTTS语音合成（云端，<1.5s）
    audio_url = tts_service.synthesize(answer, emotion=final_emotion['emotion'])

    # 总延迟: ~4.9s < 5s 达标
    return {
        'text': answer, 'audio_url': audio_url,
        'emotion': final_emotion['emotion'],
        'intensity': final_emotion['intensity'],
        'debug': final_emotion['sources']
    }
```

> **延迟优化策略**: (1) FunASR本地部署避免网络往返; (2) BGE-M3本地嵌入避免云端调用; (3) Redis缓存热点景点数据; (4) TTS结果缓存24h; (5) 流式输出 `/chat/stream` 降低首字延迟。


### 3.3 AI / 大模型层（多模态核心）

#### 3.3.1 技术清单

| 技术 | 部署方式 | 用途 | 资源占用 |
|------|----------|------|----------|
| **Qwen2.5-14B/72B** | 百炼 API | **多模态核心大模型**: 导游问答 + 文本情感分析 + 路线生成 + 服务建议总结 | 0 MB（云端） |
| **Qwen3-TTS** | 百炼 API | 语音合成（支持情感参数注入） | 0 MB（云端） |
| **BGE-M3** | **本地部署** | 文本嵌入模型: RAG 文档向量化 | **~2 GB 内存** |
| **FunASR SenseVoice-Small** | **本地部署** | 语音识别 + 语音情感识别（辅助） | **~500 MB** |
| **LangChain** | pip 安装 | RAG 框架: 文档加载、分块、检索、上下文组装 | ~100 MB |
| **ChromaDB** | Docker 本地 | 向量数据库: 存储文档向量，语义检索 | ~300-800 MB |
| **jieba** | pip 安装 | 中文分词: 辅助 RAG 关键词提取、词云 | 极轻量 |
| **DashScope SDK** | pip 安装 | 统一调用阿里云百炼 API | 极轻量 |

> **多模态大模型说明**: 本方案以 **Qwen2.5-14B/72B-Instruct** 作为核心多模态大模型，通过 DashScope 百炼平台统一调用。其承担的多模态能力包括: (1) **文本理解**: 理解游客问题并基于RAG知识库生成准确回答; (2) **情感分析**: 识别游客文本情绪（积极/消极/中性）; (3) **路线生成**: 根据游客画像生成个性化游览路线; (4) **服务建议总结**: 基于交互记录生成管理建议。满足赛题要求。

#### 3.3.2 知识库构建（对接比赛资料）

**知识库来源与分类**:

| 数据源 | 类型 | 内容 | 处理方式 | 用途 |
|--------|------|------|---------|------|
| **灵山胜境景点结构化数据集** | 结构化表格 | 16 个景点完整字段: 位置/参数/功能/文化内涵/详细介绍/游玩亮点/演艺信息 | 导入 PostgreSQL attractions 表 + 生成 Markdown 供 RAG | 智能问答事实性数据基础 |
| **拈花湾禅意小镇数据集** | 结构化表格 | 6 个景点禅意小镇数据 | 同上 | 扩展知识库覆盖范围 |
| **游客行为分析数据集** | 结构化数据 | 14万条记录: 年龄/性别/消费/停留时长/满意度/同行人数 | 导入 tourist_behaviors 表 | 游客洞察分析 + 路线推荐数据支撑 |
| **游览指南文档** | 非结构化文本 | 景区历史/文化/特色/个性化游览建议 | PaddleOCR提取 -> 分块 -> BGE-M3嵌入 -> ChromaDB | RAG语义检索增强 |
| **管理员上传文档** | 非结构化 | 讲解词/文史资料/常见问题及答案 | 上传 -> 自动分块 -> BGE-M3重新Embedding | 知识库动态更新 |

**RAG 文档分块与元数据策略**:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=100,
    separators=['\n\n', '\n', '。', '；', '，', ' ', '']
)

# 元数据标注（用于过滤检索 + 溯源）
metadata = {
    'attraction_id': 'LS-006',
    'attraction_name': '九龙灌浴',
    'category': '动态景观',
    'doc_type': '景点介绍',  # '讲解词' | '文史资料' | 'FAQ' | '景点介绍'
    'data_source': '灵山胜境景点结构化数据集',
    'version': '2026-05-28'
}
```

#### 3.3.3 LLM Prompt 设计（准确率保障）

```python
SYSTEM_PROMPT = '''你是一位专业景区导游助手，正在与游客对话。
当前服务景区为【灵山胜境】（国家AAAAA级旅游景区，集佛教文化、自然景观、人文体验于一体）。

任务:
1. 用亲切自然的语言回答游客问题，回答必须基于提供的景区知识库，准确引用景点信息
2. 对于事实性问题（如建筑高度/开放时间/历史年代），必须严格依据知识库数据回答，不得编造
3. 判断游客当前情绪，在回答末尾输出情感标签
4. 若游客询问游览路线，结合其画像（年龄/同行人数/兴趣）推荐个性化路线和讲解重点
5. 若游客兴趣为'历史'，侧重讲解文化典故和年代背景; 若兴趣为'自然风光'，侧重景观美学描述

情感分类（严格三选一）: 积极、消极、中性

输出格式:
[导游回答文本]
###sentiment###{'sentiment': '分类结果', 'confidence': 0.0~1.0}

示例:
游客: 灵山大佛有多高？
回答: 灵山大佛通高88米（主体79米+莲花瓣9米），含台基总高101.5米，耗铜量达725吨，由2000块铸铜面板拼接而成。
###sentiment###{'sentiment': '中性', 'confidence': 0.95}
'''
```

> **准确率保障措施**: (1) RAG检索优先返回结构化数据; (2) 对事实性问题启用strict_mode，要求LLM必须引用知识库原文; (3) 建立标准测试集（100条景区事实性问题），持续评测准确率; (4) FAQ高频问题直接匹配，绕过LLM生成。

#### 3.3.4 实现路径

| 天数 | 任务 |
|------|------|
| 1-3 | 阿里云百炼: 开通服务、获取 API Key、测试 Qwen2.5 / QwenTTS |
| 4-7 | **本地 BGE-M3 部署**: 下载模型（约 2GB），测试文本嵌入质量，配置 ChromaDB 持久化 |
| 8-10 | **RAG 知识库构建**: 导入灵山胜境16景点 + 拈花湾6景点结构化数据 -> 生成 Markdown -> 分块 -> BGE-M3嵌入 -> ChromaDB |
| 11-14 | LLM 接入: 封装 LLMService.chat_with_sentiment()，Prompt工程（植入景区背景+准确率约束），对接 LangChain RetrievalQA |
| 15-18 | FunASR 本地部署: SenseVoice-Small（234MB），测试语音情感输出字段 |
| 19-21 | **情感融合开发**: 编写 fuse_emotion() 规则，调试冲突 case，对接 Live2D |
| 22-24 | **路线生成 Prompt**: 设计路线推荐 Prompt，结合景点知识库 + 游客画像 + 讲解重点适配 |
| 25-26 | **准确率评测**: 构建100条标准测试集，评测事实性问答准确率，目标 >= 90% |
| 27-28 | 高级 RAG 优化: 重排序（Rerank）、Hyde假设嵌入、多路检索融合 |
| 29-32 | 全链路压测: 并发请求测试、响应延迟优化（目标<5s）、内存监控 |


### 3.4 数据层（完整版）

#### 3.4.1 技术清单

| 技术 | 版本 | 用途 | 配置 |
|------|------|------|------|
| **PostgreSQL** | 15 | 关系数据: 用户、对话记录、景点、FAQ、数字人配置、游客行为数据 | 标准配置 |
| **Redis** | 7.0+ | 缓存: 热点景点数据、会话状态、API限流、TTS音频URL缓存、路线缓存 | 默认配置 |
| **ChromaDB** | 0.4+ | 向量数据库: 文档向量存储与语义检索 | 持久化目录配置 |
| **SQLite** | Flutter 内置 | APP 本地离线缓存 | 无 |

#### 3.4.2 数据库表结构（含知识库管理 + 数字人配置 + 游客行为）

```sql
-- 游客表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(64) UNIQUE NOT NULL,
    age INTEGER,
    gender VARCHAR(10),
    group_size INTEGER DEFAULT 1,
    interests TEXT[],              -- ['历史', '自然风光', '佛教文化']
    created_at TIMESTAMP DEFAULT NOW()
);

-- 对话记录表（含双通道情感融合）
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    message_type VARCHAR(10),
    sentiment VARCHAR(10),
    sentiment_intensity FLOAT,
    voice_sentiment VARCHAR(10),
    text_sentiment VARCHAR(10),
    text_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 景点信息表（对接知识库）
CREATE TABLE attractions (
    id SERIAL PRIMARY KEY,
    attraction_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    scenic_area VARCHAR(50),
    location TEXT,
    parameters TEXT,
    core_function TEXT,
    cultural_meaning TEXT,
    detailed_intro TEXT,
    highlights TEXT,
    performance_info TEXT,
    notes TEXT,
    estimated_duration FLOAT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- FAQ表（独立维护常见问题及答案）
CREATE TABLE faq (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50),          -- '门票' | '交通' | '餐饮' | '景点' | '其他'
    hit_count INTEGER DEFAULT 0,   -- 命中次数统计
    is_hot BOOLEAN DEFAULT FALSE,  -- 是否为高频问题
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 数字人形象配置表
CREATE TABLE avatar_presets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,     -- '禅意主题' | '佛教主题' | '现代主题'
    costume_theme VARCHAR(20),     -- 'zen' | 'buddhist' | 'modern'
    voice_type VARCHAR(20),        -- 'warm_female' | 'calm_male' | 'child'
    ui_theme VARCHAR(20),          -- 'zen_cyan' | 'buddhist_gold' | 'nature_green'
    speech_style VARCHAR(20),     -- 'academic' | 'story' | 'family'
    voice_speed FLOAT DEFAULT 1.0,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 游客行为数据表（导入比赛数据集）
CREATE TABLE tourist_behaviors (
    id SERIAL PRIMARY KEY,
    tourist_id VARCHAR(20),
    user_nickname VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    attraction_name VARCHAR(100),
    attraction_type VARCHAR(50),
    visit_date DATE,
    stay_duration FLOAT,
    ticket_cost FLOAT,
    food_cost FLOAT,
    shopping_cost FLOAT,
    transport_cost FLOAT,
    entertainment_cost FLOAT,
    total_cost FLOAT,
    group_size INTEGER,
    satisfaction INTEGER,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- 知识库文档表（支持讲解词/文史资料/FAQ等类型）
CREATE TABLE kb_documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT NOT NULL,
    doc_type VARCHAR(50),          -- '讲解词' | '文史资料' | 'FAQ' | '景点介绍'
    source_file VARCHAR(200),
    chunk_index INTEGER,
    embedding_model VARCHAR(50),
    metadata JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 路线推荐记录表
CREATE TABLE route_recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    route_json JSONB NOT NULL,
    total_duration FLOAT,
    estimated_cost JSONB,
    speech_highlights JSONB,       -- 讲解重点映射
    user_feedback INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.4.3 Redis 缓存策略

| 缓存 Key | 内容 | TTL | 说明 |
|----------|------|-----|------|
| `attraction:{id}` | 景点详情 | 1 小时 | 热点景点数据 |
| `session:{user_id}` | 最近 3 轮对话历史 | 30 分钟 | 上下文保持 |
| `tts:{text_hash}` | TTS 音频 URL | 24 小时 | 避免重复合成 |
| `rate_limit:{ip}` | 请求计数 | 1 分钟 | API 限流保护 |
| `route:{user_id}:{hash}` | 推荐路线结果 | 2 小时 | 路线缓存 |
| `insights:daily` | 每日洞察报表 | 6 小时 | 游客洞察缓存 |
| `faq:hot` | 高频FAQ列表 | 1 小时 | 热门问题快速匹配 |
| `avatar:preset:{id}` | 数字人配置方案 | 12 小时 | 形象配置缓存 |


### 3.5 管理后台层（Vue 3）

#### 3.5.1 技术清单

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue 3** | 3.4+ | 前端框架，Composition API |
| **Vite** | 5.0+ | 构建工具，配置代理到后端 8000 端口 |
| **Element Plus** | 2.5+ | UI 组件库: 表格、表单、上传、弹窗、树形控件 |
| **Pinia** | 2.1+ | 状态管理，存储管理员 Token 和用户信息 |
| **ECharts** | 5.4+ | 数据可视化: 情感趋势折线图、词云、满意度饼图、游客画像雷达图 |
| **Axios** | 1.6+ | HTTP 请求后端管理 API，拦截器自动附加 Bearer Token |
| **Vue Router** | 4.2+ | 路由管理 |
| **WebSocket**（可选） | 原生 / Socket.io | 实时接收游客对话数据（数据大屏） |

#### 3.5.2 页面功能（全面对标赛题管理后台需求）

| 页面 | 功能 | 对接赛题要求 |
|------|------|-------------|
| **登录页** | JWT 鉴权登录 | -- |
| **数据总览** | ECharts: 今日对话数、活跃用户数、7日对话趋势、情感分布饼图、满意度评分、路线使用排行 | 数据大屏概览基础版 |
| **对话管理** | 表格查看所有游客对话，支持按时间/用户/情感类型筛选，显示双通道来源 | -- |
| **知识库管理** | 上传/编辑景区文档（讲解词/文史资料/FAQ），支持 Markdown/Word/Excel; 查看分块状态; 触发 BGE-M3 重新 Embedding; FAQ独立维护 | **知识库管理** |
| **数字人形象管理** | 配置多套形象方案: 外观（服装贴图上传/切换）/ 声音（音色选择/语速调节）/ 主题（UI色调）/ 讲解风格; 实时预览效果 | **数字人形象管理** |
| **游客感受度报告** | 基于交互记录生成: **关注点分析**（高频问题词云/热点话题TOP10）+ **情感趋势报告**（7日情感波动折线图/情感分布对比）+ **服务建议**（LLM自动总结负面反馈并生成改进建议） | **游客感受度报告** |
| **数据大屏** | 全屏展示: 当日/本周服务人次柱状图、热门问答TOP10滚动列表、游客满意度趋势折线图、实时情感波动、游客画像雷达图（WebSocket 实时推送） | **数据大屏概览** |
| **游客洞察** | 基于14万条行为数据的多维分析: 年龄-满意度散点图、性别-消费对比、停留时长分布、游客画像聚类（亲子/情侣/老年/独行） | -- |
| **路线效果分析** | 路线推荐使用率、用户反馈评分、热门路线TOP5、路线优化建议 | -- |

#### 3.5.3 游客感受度报告详细设计

**报告生成逻辑**:

```python
class SentimentReportService:
    def generate_daily_report(self, date: str) -> dict:
        # 1. 关注点分析
        #    - 提取当日所有对话中的高频关键词
        #    - jieba分词 + 停用词过滤 -> 生成词云数据
        #    - 统计各景点被询问次数TOP10
        #    - 统计FAQ命中次数，识别知识盲区

        # 2. 情感趋势分析
        #    - 当日情感分布（积极/消极/中性占比）
        #    - 7日情感波动折线图数据
        #    - 负面情感高发时段识别
        #    - 情感-景点关联分析（如: 哪个景点讲解后游客满意度最高）

        # 3. 服务建议生成（LLM自动总结）
        #    - 输入: 当日负面对话记录 + 高频问题 + 情感趋势
        #    - LLM Prompt: '基于以下游客反馈数据，生成3条具体的服务改进建议...'
        #    - 输出: 结构化建议列表（问题描述/改进措施/优先级）

        return {
            'date': date,
            'total_conversations': 156,
            'sentiment_dist': {'positive': 60, 'neutral': 30, 'negative': 10},
            'hot_topics': ['九龙灌浴表演时间', '梵宫门票', '素斋位置'],
            'word_cloud_data': [...],
            'service_suggestions': [
                {'issue': '多名游客反馈九龙灌浴排队时间长', 'action': '建议增加表演场次或提前广播提示', 'priority': '高'}
            ]
        }
```

#### 3.5.4 数字人形象管理页设计

| 功能模块 | 操作 | 后端对接 |
|---------|------|---------|
| **方案列表** | 查看/新增/编辑/删除形象方案 | `/admin/avatar/presets` CRUD |
| **外观配置** | 上传服装贴图（PNG格式，Live2D兼容）/ 选择预设服装 | 文件存储 + 配置表更新 |
| **声音配置** | 选择音色（温暖女声/沉稳男声/童声）/ 调节语速（0.8x~1.2x） | QwenTTS参数配置 + 配置表更新 |
| **主题配置** | 选择UI色调（禅意青/佛教金/自然绿）/ 预览APP界面效果 | 配置表更新 + 前端主题切换 |
| **讲解风格** | 选择风格（学术严谨/轻松故事/亲子互动）/ 预览示例文案 | LLM Prompt模板切换 |
| **实时预览** | 在管理后台嵌入Live2D预览窗口，实时查看配置效果 | 调用前端渲染组件 |

#### 3.5.5 实现路径

| 天数 | 任务 |
|------|------|
| 1-2 | 项目初始化: `npm create vue@latest`，安装 Element Plus / Pinia / Axios / ECharts |
| 3-6 | 登录页 + 数据总览页（ECharts 对接 `/admin/stats`） |
| 7-10 | 对话管理页（支持情感筛选 + 来源展示）+ **知识库管理页**（文档上传/分块查看/重新Embedding/FAQ维护） |
| 11-14 | **数字人形象管理页**: 外观/声音/主题/讲解风格配置 + 实时预览 |
| 15-18 | **游客感受度报告页**: 关注点词云 + 情感趋势图表 + LLM服务建议展示 |
| 19-21 | **数据大屏页**: 全屏布局，服务人次/热门问答/满意度趋势实时展示（WebSocket） |
| 22-24 | 游客洞察页 + 路线效果分析页 |

---

## 五、服务器资源分配建议

### 6.1 推荐配置

| 场景 | 推荐配置 | 说明 |
|------|----------|------|
| **开发/演示** | 4核8G | 支持本地 BGE-M3（2GB）+ FunASR（500MB）+ 基础服务（1.5GB），余量充足 |
| **竞赛演示（高并发）** | 4核16G | 支持 BGE-M3 + 更高并发 Uvicorn workers + Redis + 余量缓冲 |
| **生产环境** | 8核16G+ | 支持 GPU 加速（BGE-M3 / FunASR 可上 CUDA）、多实例负载均衡 |

### 6.2 4核8G 环境下的资源分配

| 服务 | 内存占用 | 说明 |
|------|----------|------|
| FastAPI (2 workers) | ~300 MB | 并发处理能力提升 |
| PostgreSQL | ~500 MB | 标准配置（含景点数据 + FAQ + 14万条行为数据） |
| Redis | ~200 MB | 缓存 + 会话 |
| ChromaDB | ~600 MB | 向量数据量增大时自动扩展 |
| BGE-M3 (本地) | **~2 GB** | 文本嵌入，RAG 核心 |
| FunASR SenseVoice-Small | ~500 MB | 语音识别 + 语音情感 |
| Nginx | ~50 MB | alpine |
| Docker 运行时 | ~200 MB | 容器开销 |
| **合计** | **~4.35 GB** | |
| **剩余可用** | **~3.65 GB** | 充裕，可支持突发峰值 |

---

## 六、8周 Sprint 开发计划（完整版）

| 阶段 | 时间 | 核心目标 | 关键交付物 |
|------|------|----------|----------|
| **Sprint 1** | 第1-2周 | **基础跑通** | Flutter 对话页 + FastAPI + PostgreSQL + Redis + 文本问答（直连 Qwen2.5） |
| **Sprint 2** | 第3-4周 | **语音 + Live2D 三模态** | FunASR 本地部署 + QwenTTS + **Live2D 双参数口型同步 + 情感表情 + Idle 动画 + 形象切换** |
| **Sprint 3** | 第5-6周 | **RAG + 情感融合 + 路线推荐 + 知识库管理** | **BGE-M3 本地部署** + 知识库构建（灵山胜境 16 景点 + 拈花湾 6 景点）+ **语音-文本双通道情感融合** + **个性化路线推荐引擎** + **讲解重点适配** |
| **Sprint 4** | 第7-8周 | **后台管理 + 游客洞察 + 优化 + 演示** | **Vue 管理后台**（知识库管理 + 数字人形象管理 + 游客感受度报告 + 数据大屏）+ RAG 调优 + 口型 Smoothing 优化 + **准确率测试（目标>=90%）** + **演示视频录制** |

### 7.1 各 Sprint 详细任务

**Sprint 1: 基础跑通**
- [ ] Flutter 项目搭建，对话页 UI，Dio 封装
- [ ] FastAPI 脚手架，PostgreSQL 建模（含景点表/FAQ表/游客行为表/数字人配置表），Alembic 迁移
- [ ] Redis 部署，缓存策略设计
- [ ] 对接 Qwen2.5 API，实现基础 `/chat` 接口
- [ ] 管理后台登录接口

**Sprint 2: 语音 + Live2D 三模态**
- [ ] FunASR SenseVoice-Small 本地部署，语音识别测试
- [ ] 提取 FunASR 语音情感字段（如有）
- [ ] Qwen3-TTS 接入，音频 URL 返回
- [ ] Android Native 集成 Cubism SDK，PlatformView 渲染
- [ ] 双参数口型同步（RMS + 频谱比）
- [ ] **三模态情感表情联动**（接收后端 emotion 字段，与语音/文本同步输出）
- [ ] **数字人形象切换**（禅意/佛教/现代三套服装贴图动态切换）
- [ ] Idle 动画系统（呼吸 + 眨眼 + 头部微动 + 物理飘动）

**Sprint 3: RAG + 情感融合 + 路线推荐 + 知识库管理**
- [ ] BGE-M3 本地部署，测试嵌入质量
- [ ] **导入比赛知识库**: 灵山胜境 16 景点 + 拈花湾 6 景点结构化数据 -> 生成 Markdown -> 分块 -> BGE-M3 嵌入 -> ChromaDB
- [ ] **导入游客行为数据集**: 14万条记录 -> PostgreSQL `tourist_behaviors` 表
- [ ] RAG 检索链路打通: 用户问题 -> BGE-M3 嵌入 -> ChromaDB 检索 -> TopK 文档 -> LLM 上下文组装
- [ ] LLM Prompt 加入情感分析指令 + 景区背景知识 + 准确率约束
- [ ] **编写 fuse_emotion() 融合规则，联调双通道**
- [ ] **路线推荐引擎**: 基于规则（画像匹配）+ 协同过滤，实现 `/route/recommend`
- [ ] **讲解重点适配**: 根据游客兴趣标签动态生成景点讲解侧重点
- [ ] **知识库管理 API**: 文档上传解析 + FAQ维护 + 重新 Embedding 触发
- [ ] 前端路线展示页: 时间轴 + 景点卡片 + 讲解重点高亮 + 预估信息

**Sprint 4: 后台管理 + 游客洞察 + 优化 + 演示**
- [ ] **Vue 管理后台 - 知识库管理页**: 讲解词/文史资料/FAQ 上传维护 + 分块状态查看 + 重新 Embedding
- [ ] **Vue 管理后台 - 数字人形象管理页**: 外观/服装/声音/主题/讲解风格配置 + 实时预览
- [ ] **Vue 管理后台 - 游客感受度报告页**: 关注点词云 + 情感趋势图表 + LLM 服务建议自动生成
- [ ] **Vue 管理后台 - 数据大屏页**: 当日/本周服务人次、热门问答 TOP10、满意度趋势实时展示（WebSocket）
- [ ] **Vue 游客洞察页**: 对接 `/admin/insights`，展示年龄/性别/消费/满意度/情感多维分析
- [ ] **准确率评测**: 构建 100 条标准测试集，评测事实性问答准确率，目标 >= 90%
- [ ] RAG 高级优化: 重排序、Hyde 假设嵌入、多路检索融合
- [ ] Redis 缓存优化: TTS 音频缓存、热点景点缓存、路线缓存、FAQ 缓存
- [ ] 口型 Smoothing 参数调优，表情过渡打磨
- [ ] 全链路压测，并发测试，延迟优化（目标 < 5s）
- [ ] **演示视频脚本 + 录制（3-5 分钟）**: 重点展示三模态交互、情感融合、路线推荐、知识库管理、游客洞察

---

## 七、环境变量清单

| 变量名 | 来源 | 用途 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 阿里云百炼控制台 | 调用 Qwen2.5、QwenTTS |
| `DATABASE_URL` | 自建 | PostgreSQL 异步连接串 |
| `REDIS_URL` | 自建 | Redis 连接串 |
| `JWT_SECRET` | 自建 | 管理后台 Token 签名密钥 |
| `DB_PASSWORD` | 自建 | PostgreSQL root 密码 |

---

## 八、技术边界确认

| 功能 | 状态 | 说明 |
|------|------|------|
| 语音输入 | 保留 | FunASR SenseVoice-Small 本地 |
| 语音输出 | 保留 | Qwen3-TTS 云端 |
| 文本问答 | 保留 | Qwen2.5 云端 + RAG |
| **表情输出** | **保留（三模态核心）** | **Live2D 情感表情作为独立反馈模态** |
| Live2D 数字人 | 保留 | 双参数口型 + 情感表情 + Idle + **形象管理** |
| **语音-文本情感融合** | **核心亮点** | FunASR 语音情感 + LLM 文本情感 -> fuse_emotion |
| **个性化路线讲解** | **新增核心功能** | 基于游客画像 + 景点知识库 -> 生成推荐路线 + 讲解重点适配 |
| **知识库管理** | **新增核心功能** | 管理员上传/更新/维护讲解词、文史资料、FAQ |
| **数字人形象管理** | **新增核心功能** | 外观/服装/声音/主题/讲解风格配置 |
| **游客感受度报告** | **新增核心功能** | 关注点分析 + 情感趋势 + LLM服务建议 |
| **数据大屏概览** | **新增核心功能** | 服务人次/热门问答/满意度趋势实时展示 |
| RAG 知识库 | 保留 | BGE-M3 本地 + ChromaDB + LangChain，**对接灵山胜境/拈花湾结构化数据** |
| **游客洞察分析** | **新增核心功能** | 基于 14万条游客行为数据的多维分析 |
| Redis 缓存 | 保留 | 热点数据 + 会话 + TTS 缓存 + 路线缓存 + FAQ 缓存 |
| 管理后台 | 保留 | Vue 3 + Element Plus + ECharts，**新增知识库/形象/报告/大屏模块** |
| 图片识别 | 砍掉 | 多模态仅限语音+文字+表情 |
| 地图定位 | 砍掉 | 路线导航调用外部地图APP，不内置地图 |

---

> **文档生成说明**: 本文档 v3.0 基于比赛要求进行了全面对接优化。游客交互侧覆盖: 多模态交互（语音+文本+表情/口型）、智能问答与讲解（RAG+准确率>=90%保障）、个性化推荐（路线+讲解重点）。管理后台侧覆盖: 知识库管理（讲解词/文史资料/FAQ上传维护）、数字人形象管理（外观/服装/声音/主题配置）、游客感受度报告（关注点分析+情感趋势+服务建议）、数据大屏概览（服务人次/热门问答/满意度趋势）。非功能性需求覆盖: 多模态大模型（Qwen2.5）、本地知识库（BGE-M3+ChromaDB）、准确度>=90%、自然度专家评估、延迟<5秒、稳定性保障、备选方案。
