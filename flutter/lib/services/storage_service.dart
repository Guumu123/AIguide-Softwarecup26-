import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/avatar_config.dart';

class StorageService {
  static const String _keyAvatarConfig = 'avatar_config';
  static const String _keyVisitorId = 'visitor_id';

  static Future<void> saveAvatarConfig(AvatarConfig config) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyAvatarConfig, jsonEncode(config.toJson()));
  }

  static Future<AvatarConfig> getAvatarConfig() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString(_keyAvatarConfig);
    if (jsonStr == null) {
      return AvatarConfig.defaultConfig();
    }
    return AvatarConfig.fromJson(jsonDecode(jsonStr));
  }

  static Future<void> saveVisitorId(String id) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyVisitorId, id);
  }

  static Future<String?> getVisitorId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyVisitorId);
  }
}
