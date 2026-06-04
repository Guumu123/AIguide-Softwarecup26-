# AI 景区向导 APP - 技术文档

## 第二部分：前端 APP 层（Flutter + Live2D）

---

## 1. 技术清单

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

---

## 2. 三模态交互界面设计

| 模态 | 输入/输出 | 交互组件 | 说明 |
|------|----------|---------|------|
| **语音** | 输入 | 底部麦克风按钮（按住说话） | FunASR本地识别，支持方言降噪 |
| **语音** | 输出 | 音频播放器 + Live2D口型同步 | QwenTTS音频URL，双参数口型驱动（RMS+频谱比） |
| **文本** | 输入 | 底部文本输入框 | 支持快捷问题推荐、景点手动选择 |
| **文本** | 输出 | 对话气泡（Markdown渲染） | 支持景点卡片、路线卡片、讲解重点高亮 |
| **表情** | **输出** | **Live2D数字人面部** | **独立模态**: 根据情感融合结果实时反馈5种表情（happy/sad/surprised/confused/neutral） |

> **关键设计**: 数字人表情不仅是'情感装饰'，而是**独立的反馈模态**。当系统识别到游客情绪消极时，数字人通过 `sad` 表情 + 安慰性语音同步输出，实现真正意义上的'情感互动'。

---

## 3. 数字人形象管理（贴合景区文化特色）

### 3.1 形象配置维度

| 维度 | 配置项 | 实现方式 | 景区适配 |
|------|--------|---------|---------|
| **外观** | 服装贴图 | Live2D模型多贴图切换 | 禅意主题（素色僧袍风格）/ 佛教主题（金色袈裟风格）/ 现代主题（休闲导游风格） |
| **声音** | 音色/语速/语调 | Qwen3-TTS参数配置 | 温暖女声（默认）/ 沉稳男声 / 童声（亲子模式） |
| **主题** | 背景/边框/UI色调 | Flutter主题切换 | 禅意青（默认）/ 佛教金 / 自然绿 |
| **讲解风格** | 文案风格 | LLM Prompt动态切换 | 学术严谨型 / 轻松故事型 / 亲子互动型 |

### 3.2 配置存储与同步

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

### 3.3 Flutter加载逻辑

```dart
// 启动时从后端拉取配置，fallback到本地默认
final config = await AvatarConfigService.load();
await platform.invokeMethod('loadModel', {
  'path': 'assets/hiyori',
  'costume': config.costumeTheme,  // 切换贴图
  'theme': config.uiTheme          // 通知Flutter UI层
});
```

---

## 4. Live2D 数字人详细规范（竞赛加分重点）

### 4.1 模型参数要求

| 参数 ID | 作用 | 范围 | 必要性 |
|---------|------|------|--------|
| `ParamMouthOpenY` | 嘴巴开合程度 | 0.0 ~ 1.0 | **必须** |
| `ParamMouthForm` | 嘴巴形状（圆嘴/咧嘴） | -1.0 ~ 1.0 | **强烈建议** |
| `ParamEyeLOpen` / `ParamEyeROpen` | 左右眼睁开 | 0.0 ~ 1.0 | 必须 |
| `ParamBrowLY` / `ParamBrowRY` | 左右眉毛 Y 轴 | -1.0 ~ 1.0 | 必须（表情） |
| `ParamAngleX` / `ParamAngleY` | 头部转动 | -30 ~ 30 | 建议（视线跟随） |
| `ParamBreath` | 呼吸起伏 | 0.0 ~ 1.0 | 建议 |
| Physics (`.physics3.json`) | 头发/衣服物理飘动 | -- | 建议 |

### 4.2 口型同步方案（双参数驱动）

| 驱动参数 | 音频特征源 | 映射逻辑 |
|----------|-----------|----------|
| **ParamMouthOpenY** | **RMS 能量**（响度） | 音量大 -> 嘴张得大; 平滑过渡（低通滤波系数 0.25） |
| **ParamMouthForm** | **频谱高频/低频能量比** | 高频多（嘶/咦）-> 偏向 1（咧嘴）; 低频多（啊/哦）-> 偏向 -1（圆嘴）; 平滑系数 0.15 |

### 4.3 自然动画系统

| 动画类型 | 实现方式 | 参数 |
|----------|----------|------|
| **呼吸** | 正弦波循环 | `ParamBreath = 0.5 + 0.5 * sin(t / 3.2345)`，周期约 3 秒 |
| **眨眼** | 随机间隔触发 | 间隔 2~6 秒随机，闭眼动画 150ms |
| **头部微动** | Idle 状态正弦叠加 | `ParamAngleX = sin(t/5)*3deg`，`ParamAngleY = sin(t/7)*2deg` |
| **物理飘动** | Cubism Physics 引擎 | 自动更新，需模型绑定 `ParamHairFront` 等 |
| **视线跟随** | 触摸事件映射 | 手指坐标 -> 归一化 -> `ParamAngleX/Y` |

### 4.4 情感-表情联动映射（三模态核心）

| 情感标签 | 眉毛 | 眼睛 | 嘴型 | **联动语音/文本** | 说明 |
|----------|------|------|------|------------------|------|
| `happy` | 上扬 (-0.3) | 明亮 (1.0) | 微笑 (0.5) | 轻快语调 + 积极文案 | 开心、满意 |
| `sad` | 下垂 (+0.5) | 黯淡 (0.6) | 下撇 (-0.2) | 舒缓语调 + 安慰文案 | 失望、疲惫 |
| `surprised` | 高挑 (-0.5) | 睁大 (1.0) | 微张 (0.0) | 惊叹语调 + 详细讲解 | 惊讶、赞叹 |
| `confused` | 不对称 (+0.2/-0.2) | 半眯 (0.8) | 平直 (0.0) | 放慢语速 + 引导式提问 | 疑惑、思考 |
| `neutral` | 默认 (0.0) | 正常 (1.0) | 自然 (0.0) | 标准讲解语调 | 常规讲解 |

> **过渡要求**: 表情切换必须使用插值（Lerp），过渡时间 0.3~0.5 秒，禁止瞬间跳变。

---

## 5. 个性化路线展示页 + 讲解重点适配

| 组件 | 功能 | 数据来源 |
|------|------|---------|
| **路线时间轴** | 纵向时间轴展示推荐游览顺序 | 后端 `/route/recommend` 返回 |
| **景点卡片** | 景点缩略图 + 名称 + 建议停留时长 + **讲解重点标签** | 知识库 `attractions` 表 |
| **讲解重点** | 根据游客兴趣动态高亮（如'历史爱好者'高亮文化典故） | LLM根据画像动态生成 |
| **预估信息** | 总时长、总步行距离、预估消费 | 基于知识库 + 游客行为数据统计 |
| **景点手动选择** | 下拉选择当前所在景点（**备选方案**） | 知识库景点列表 |
| **一键导航** | 调用系统地图APP（外部跳转） | 不内置地图，减少包体积 |

---

## 6. Flutter <-> Native 通信接口

```dart
const platform = MethodChannel('com.yourteam.live2d');

// 基础方法
await platform.invokeMethod('loadModel', {'path': 'assets/hiyori', 'costume': 'zen'});
await platform.invokeMethod('speak', {'audioUrl': url, 'emotion': 'happy', 'intensity': 0.9});
await platform.invokeMethod('stopSpeaking');
await platform.invokeMethod('setLookAt', {'x': 0.5, 'y': 0.3});
await platform.invokeMethod('setExpression', {'emotion': 'surprised', 'intensity': 0.8});
```

---

## 7. 实现路径

| 天数 | 任务 | 产出 |
|------|------|------|
| 1-3 | 素材准备: 获取 Live2D 模型（推荐官方 Hiyori），确认参数完整; 准备**多套服装贴图**（禅意/佛教/现代） | 可用 `.model3.json` + `.moc3` + 多组贴图 |
| 4-7 | Native 渲染层: Android 集成 Cubism SDK，GLSurfaceView/TextureView 加载模型，启用 Physics 更新，基础渲染循环 | Flutter PlatformView 能显示会呼吸的小人 |
| 8-12 | 口型同步引擎: AudioTrack + Visualizer 实时取音频 PCM，计算 RMS -> `ParamMouthOpenY`，计算频谱比 -> `ParamMouthForm`，加平滑滤波 | 播放测试音频时嘴型与音量/音色匹配 |
| 13-15 | **三模态表情系统**: 定义情感参数映射表，实现插值过渡器，对接后端 `emotion` + `intensity` 字段; 表情作为独立模态与语音/文本同步输出 | 切换情感时眉毛眼神自然变化 |
| 16-18 | Idle 细节 + **形象切换**: 随机眨眼、头部微动、视线跟随触摸、物理飘动; 服装贴图动态切换逻辑 | Idle 状态生动不僵硬; 可切换主题 |
| 19-21 | **路线展示页 + 景点手动选择**: 时间轴 UI、景点卡片、讲解重点高亮、预估信息、手动选择景点 | 前端可展示个性化路线 |
| 22-24 | 联调: 对接后端 QwenTTS 音频 URL + 情感融合字段 + 路线推荐数据 + 形象配置数据，端到端测试 | 完整交互链路可用 |

---

## 8. 关键代码片段

### 8.1 音频特征提取（口型驱动）

```dart
// 使用 Visualizer 获取音频 PCM 数据
final visualizer = Visualizer(audioSessionId);
visualizer.setCaptureSize(Visualizer.getCaptureSizeRange()[1]);

// 计算 RMS 能量
final pcmData = visualizer.getFft();
double rms = 0;
for (int i = 0; i < pcmData.length; i++) {
  rms += pcmData[i] * pcmData[i];
}
rms = math.sqrt(rms / pcmData.length);

// 计算频谱比（高频/低频）
double lowFreq = 0, highFreq = 0;
for (int i = 0; i < pcmData.length / 2; i++) {
  lowFreq += pcmData[i];
}
for (int i = pcmData.length ~/ 2; i < pcmData.length; i++) {
  highFreq += pcmData[i];
}
double spectralRatio = highFreq / (lowFreq + 1e-6);

// 映射到 Live2D 参数
final mouthOpenY = math.min(1.0, rms * 2.0);  // 放大系数可调
final mouthForm = math.max(-1.0, math.min(1.0, (spectralRatio - 1.0) * 2.0));
```

### 8.2 情感插值过渡器

```dart
class EmotionInterpolator {
  Map<String, double> currentParams = {};
  Map<String, double> targetParams = {};
  double lerpSpeed = 0.3; // 0.3~0.5秒过渡

  void setTargetEmotion(String emotion, double intensity) {
    // 根据 emotion 查表获取目标参数
    targetParams = emotionParamMap[emotion]!;
    // 按 intensity 缩放
    for (var key in targetParams.keys) {
      targetParams[key] = targetParams[key]! * intensity;
    }
  }

  void update(double dt) {
    for (var key in targetParams.keys) {
      currentParams[key] = lerp(currentParams[key] ?? 0, targetParams[key]!, lerpSpeed * dt);
    }
  }

  double lerp(double a, double b, double t) {
    return a + (b - a) * t;
  }
}
```

---

> **文档说明**: 本部分详细规定了前端 APP 的技术实现，重点聚焦 Live2D 数字人的三模态交互（口型同步、情感表情、Idle动画）以及形象管理、路线展示等竞赛加分功能。
