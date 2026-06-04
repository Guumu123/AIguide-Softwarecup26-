import 'package:dio/dio.dart';

class ApiService {
  static final Dio _dio = Dio(BaseOptions(
    baseUrl: 'https://api.scenic-guide.com', // Replace with actual base URL
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));

  static Future<Response> sendMessage(String text, String visitorId) async {
    return await _dio.post('/chat', data: {
      'user_id': visitorId,
      'message': text,
    });
  }

  static Future<Response> getRecommendedRoute(
    String visitorId, {
    int age = 25,
    String gender = '男',
    int groupSize = 1,
    List<String> interests = const ['佛教文化'],
  }) async {
    return await _dio.post('/route/recommend', data: {
      'user_id': visitorId,
      'age': age,
      'gender': gender,
      'group_size': groupSize,
      'interests': interests,
    });
  }

  static Future<Response> getTTSAudio(String text, Map<String, dynamic> config) async {
    return await _dio.post('/voice/synthesize', data: {
      'text': text,
      'config': config,
    });
  }
}
