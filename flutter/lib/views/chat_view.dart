import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:provider/provider.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../providers/chat_provider.dart';

class ChatView extends StatefulWidget {
  const ChatView({super.key});

  @override
  State<ChatView> createState() => _ChatViewState();
}

class _ChatViewState extends State<ChatView> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI 景区向导'),
        actions: [
          IconButton(
            icon: const Icon(Icons.route),
            onPressed: () => Navigator.pushNamed(context, '/route'),
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => Navigator.pushNamed(context, '/settings'),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Consumer<ChatProvider>(
              builder: (context, provider, child) {
                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: provider.messages.length,
                  itemBuilder: (context, index) {
                    final msg = provider.messages[index];
                    final isUser = msg['role'] == 'user';
                    return Align(
                      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                      child: Container(
                        margin: const EdgeInsets.symmetric(vertical: 4),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: isUser ? Colors.blue[100] : Colors.grey[200],
                          borderRadius: BorderRadius.circular(12),
                        ),
                        constraints: BoxConstraints(
                          maxWidth: MediaQuery.of(context).size.width * 0.7,
                        ),
                        child: MarkdownBody(data: msg['content'] ?? ''),
                      ),
                    );
                  },
                );
              },
            ),
          ),
          _buildInputSection(context),
        ],
      ),
    );
  }

  Widget _buildInputSection(BuildContext context) {
    final provider = context.read<ChatProvider>();
    final isListening = context.select<ChatProvider, bool>((p) => p.isListening);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                hintText: '输入问题...',
                border: OutlineInputBorder(),
              ),
              onSubmitted: (val) {
                if (val.isNotEmpty) {
                  provider.sendMessage(val);
                  _controller.clear();
                }
              },
            ),
          ),
          const SizedBox(width: 8),
          _buildMicButton(context, provider, isListening),
        ],
      ),
    );
  }

  // 分离麦克风按钮避免整个 input section 重建
  Widget _buildMicButton(BuildContext context, ChatProvider provider, bool isListening) {
    // Web 端隐藏语音按钮
    if (kIsWeb) return const SizedBox.shrink();

    return GestureDetector(
      onLongPressStart: (_) => provider.startListening(),
      onLongPressEnd: (_) => provider.stopListening(),
      child: CircleAvatar(
        backgroundColor: isListening ? Colors.red : Colors.blue,
        child: Icon(
          isListening ? Icons.mic : Icons.mic_none,
          color: Colors.white,
        ),
      ),
    );
  }
}
