import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:audioplayers/audioplayers.dart';
import '../services/api_service.dart';
import '../services/database_service.dart';

class ChatProvider with ChangeNotifier {
  final List<Map<String, dynamic>> _messages = [];
  final stt.SpeechToText _speech = stt.SpeechToText();
  final AudioPlayer _audioPlayer = AudioPlayer();
  
  bool _isListening = false;
  String _currentWords = '';

  List<Map<String, dynamic>> get messages => _messages;
  bool get isListening => _isListening;
  String get currentWords => _currentWords;

  ChatProvider() {
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final history = await DatabaseService.getChatHistory();
    _messages.addAll(history);
    notifyListeners();
  }

  Future<void> startListening() async {
    bool available = await _speech.initialize();
    if (available) {
      _isListening = true;
      notifyListeners();
      _speech.listen(onResult: (val) {
        _currentWords = val.recognizedWords;
        notifyListeners();
      });
    }
  }

  Future<void> stopListening() async {
    _isListening = false;
    _speech.stop();
    if (_currentWords.isNotEmpty) {
      await sendMessage(_currentWords);
      _currentWords = '';
    }
    notifyListeners();
  }

  Future<void> sendMessage(String text) async {
    // Add user message
    _messages.add({'role': 'user', 'content': text});
    await DatabaseService.insertChatMessage('user', text);
    notifyListeners();

    try {
      // Get AI response
      final response = await ApiService.sendMessage(text, 'visitor_123');
      final aiContent = response.data['text'] ?? '';
      
      _messages.add({'role': 'assistant', 'content': aiContent});
      await DatabaseService.insertChatMessage('assistant', aiContent);
      notifyListeners();

      // Play TTS if URL provided
      if (response.data['audio_url'] != null && response.data['audio_url'].toString().isNotEmpty) {
        await _audioPlayer.play(UrlSource(response.data['audio_url']));
      }
    } catch (e) {
      print('Error sending message: $e');
    }
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }
}
