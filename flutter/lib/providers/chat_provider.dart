import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:audioplayers/audioplayers.dart';
import '../services/api_service.dart';
import '../services/database_service.dart';

class ChatProvider with ChangeNotifier {
  final List<Map<String, dynamic>> _messages = [];
  AudioPlayer? _audioPlayer;
  
  bool _isListening = false;
  String _currentWords = '';

  // Web 平台不支持语音识别，使用标志位跳过
  bool get supportsVoice => !kIsWeb;
  List<Map<String, dynamic>> get messages => _messages;
  bool get isListening => _isListening;
  String get currentWords => _currentWords;

  ChatProvider() {
    // Web 端延迟初始化 AudioPlayer 避免不兼容
    try {
      _audioPlayer = AudioPlayer();
    } catch (_) {
      _audioPlayer = null;
    }
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    try {
      final history = await DatabaseService.getChatHistory();
      _messages.addAll(history);
      notifyListeners();
    } catch (_) {
      // Web 端 sqlite 不可用时忽略
    }
  }

  Future<void> startListening() async {
    if (kIsWeb) return;
    try {
      final speech = stt.SpeechToText();
      bool available = await speech.initialize();
      if (available) {
        _isListening = true;
        notifyListeners();
        speech.listen(onResult: (val) {
          _currentWords = val.recognizedWords;
          notifyListeners();
        });
      }
    } catch (_) {
      _isListening = false;
    }
  }

  Future<void> stopListening() async {
    _isListening = false;
    notifyListeners();
  }

  Future<void> sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    
    // Add user message
    _messages.add({'role': 'user', 'content': text});
    notifyListeners();
    
    try {
      await DatabaseService.insertChatMessage('user', text);
    } catch (_) {}

    try {
      // Get AI response
      final response = await ApiService.sendMessage(text, 'visitor_123');
      final aiContent = response.data['text'] ?? '';
      
      _messages.add({'role': 'assistant', 'content': aiContent});
      notifyListeners();
      
      try {
        await DatabaseService.insertChatMessage('assistant', aiContent);
      } catch (_) {}

      // Play TTS if URL provided
      if (response.data['audio_url'] != null && response.data['audio_url'].toString().isNotEmpty) {
        try {
          await _audioPlayer?.play(UrlSource(response.data['audio_url']));
        } catch (_) {}
      }
    } catch (e) {
      _messages.add({'role': 'assistant', 'content': '抱歉，服务暂时不可用，请稍后再试。'});
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _audioPlayer?.dispose();
    super.dispose();
  }
}
