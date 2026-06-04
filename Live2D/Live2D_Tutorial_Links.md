# Live2D 数字人快速制作教程汇总

本文档整理了从模型制作到移动端（Android/Flutter）集成的全流程教程链接，旨在帮助你在近期内快速完成项目。

---

## 🎨 第一部分：模型制作（Cubism Editor）
*适合美术及快速原型设计*

- **官方快速入门（视频+图文）**
    - [10 分钟学会“眨眼”设置](https://docs.live2d.com/cubism-editor-tutorials/eye-blink/) - 掌握最基本的动作参数设置。
    - [20 分钟学会“口型 (あいうえお)”](https://docs.live2d.com/cubism-editor-tutorials/mouth-aiueo/) - 实现口型同步的基础。
    - [以图形记忆 Live2D 基础概念](https://docs.live2d.com/4.2/zh-CHS/cubism-editor-tutorials/figure/) - 快速理解网格、变形器与参数。

- **高效率技巧**
    - [使用模板功能轻松建模](https://docs.live2d.com/cubism-editor-tutorials/template/) - **最快路径**：利用官方模板自动生成变形器，节省大量手工时间。
    - [嵌入式模型导出规范](https://docs.live2d.com/4.2/zh-CHS/cubism-editor-tutorials/exporting-data-for-embedding/) - 确保导出为移动端 SDK 支持的 `.moc3` 格式。

---

## 🤖 第二部分：Android 原生开发（Cubism SDK Native）
*适合底层渲染与口型驱动开发*

- **SDK 基础与 Demo 跑通**
    - [Android 示例项目运行指南](https://docs.live2d.com/ko/cubism-sdk-tutorials/android-sample-run/) - 先跑通官方 Demo，确认环境无误。
    - [SDK for Native 官方手册](https://docs.live2d.com/cubism-sdk-manual/cubism-sdk-for-native/) - 深入了解渲染循环与模型加载逻辑。

- **核心交互功能**
    - [基于音频音量的口型同步实现](https://docs.live2d.com/ko/cubism-sdk-tutorials/native-lipsync-from-wav-native/) - 文档要求的 RMS 能量映射嘴型实现参考。
    - [多动作与部位管理](https://docs.live2d.com/ko/cubism-sdk-tutorials/multi-motion-management/) - 学习如何控制局部动作（如招手、点头）。

---

## 🚀 第三部分：Flutter 集成与应用层
*适合界面逻辑与 Native 通信*

- **快速集成插件**
    - [flutter_live2d (Pub.dev)](https://pub.dev/packages/flutter_live2d) - 现成的 Flutter 插件，可快速加载并显示模型。

- **原生视图嵌入（符合竞赛文档）**
    - [Flutter AndroidView 嵌入与黑屏解决](https://community.live2d.com/discussion/2037/live2d-pageview-switch-with-in-flutter-andorid) - 解决页面切换与渲染状态保持的关键讨论。
    - [Flutter + Live2D + AI 对话实战参考](https://valgo.co.jp/tech/flutter_use_live2d_and_gemini/) - 虽然是 Unity 方案，但其中的逻辑设计（UI 堆叠、异步请求）极具参考价值。

---

## 💡 快速制作建议
1. **优先使用官方模型测试**：在自己的模型制作完成前，使用 [官方 Hiyori 样本数据](http://www.live2d.com/download/sample-data/) 进行程序调试。
2. **善用自动功能**：Cubism Editor 中的“自动生成网格”和“自动生成变形器”是缩短周期的核心工具。
3. **参数 ID 对齐**：务必使用标准 ID（如 `ParamMouthOpenY`），以确保 SDK 默认代码能直接驱动模型。

---
*文档生成日期: 2026-06-04*
