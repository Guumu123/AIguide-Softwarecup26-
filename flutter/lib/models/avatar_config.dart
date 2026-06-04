class AvatarConfig {
  String costumeTheme; // 'zen' | 'buddhist' | 'modern'
  String voiceType; // 'warm_female' | 'calm_male' | 'child'
  String uiTheme; // 'zen_cyan' | 'buddhist_gold' | 'nature_green'
  String speechStyle; // 'academic' | 'story' | 'family'
  double voiceSpeed; // 0.8 ~ 1.2

  AvatarConfig({
    required this.costumeTheme,
    required this.voiceType,
    required this.uiTheme,
    required this.speechStyle,
    required this.voiceSpeed,
  });

  factory AvatarConfig.defaultConfig() {
    return AvatarConfig(
      costumeTheme: 'zen',
      voiceType: 'warm_female',
      uiTheme: 'zen_cyan',
      speechStyle: 'academic',
      voiceSpeed: 1.0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'costumeTheme': costumeTheme,
      'voiceType': voiceType,
      'uiTheme': uiTheme,
      'speechStyle': speechStyle,
      'voiceSpeed': voiceSpeed,
    };
  }

  factory AvatarConfig.fromJson(Map<String, dynamic> json) {
    return AvatarConfig(
      costumeTheme: json['costumeTheme'] ?? 'zen',
      voiceType: json['voiceType'] ?? 'warm_female',
      uiTheme: json['uiTheme'] ?? 'zen_cyan',
      speechStyle: json['speechStyle'] ?? 'academic',
      voiceSpeed: (json['voiceSpeed'] ?? 1.0).toDouble(),
    );
  }
}
