import 'package:flutter/material.dart';
import '../models/avatar_config.dart';
import '../services/storage_service.dart';

class SettingsView extends StatefulWidget {
  const SettingsView({super.key});

  @override
  State<SettingsView> createState() => _SettingsViewState();
}

class _SettingsViewState extends State<SettingsView> {
  late AvatarConfig _config;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  Future<void> _loadConfig() async {
    _config = await StorageService.getAvatarConfig();
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    return Scaffold(
      appBar: AppBar(title: const Text('数字人设置')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildSectionTitle('讲解风格'),
          _buildRadioGroup<String>(
            value: _config.speechStyle,
            options: {
              'academic': '学术严谨型',
              'story': '轻松故事型',
              'family': '亲子互动型',
            },
            onChanged: (val) => setState(() => _config.speechStyle = val!),
          ),
          const Divider(),
          _buildSectionTitle('声音设置'),
          _buildRadioGroup<String>(
            value: _config.voiceType,
            options: {
              'warm_female': '温暖女声',
              'calm_male': '沉稳男声',
              'child': '童声',
            },
            onChanged: (val) => setState(() => _config.voiceType = val!),
          ),
          ListTile(
            title: const Text('语速'),
            subtitle: Slider(
              value: _config.voiceSpeed,
              min: 0.8,
              max: 1.2,
              divisions: 4,
              label: _config.voiceSpeed.toStringAsFixed(1),
              onChanged: (val) => setState(() => _config.voiceSpeed = val),
            ),
          ),
          const Divider(),
          _buildSectionTitle('主题设置'),
          _buildRadioGroup<String>(
            value: _config.uiTheme,
            options: {
              'zen_cyan': '禅意青',
              'buddhist_gold': '佛教金',
              'nature_green': '自然绿',
            },
            onChanged: (val) => setState(() => _config.uiTheme = val!),
          ),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: () async {
              await StorageService.saveAvatarConfig(_config);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('配置已保存')),
              );
            },
            child: const Text('保存配置'),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(
        title,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.blue),
      ),
    );
  }

  Widget _buildRadioGroup<T>({
    required T value,
    required Map<T, String> options,
    required ValueChanged<T?> onChanged,
  }) {
    return Column(
      children: options.entries.map((entry) {
        return RadioListTile<T>(
          title: Text(entry.value),
          value: entry.key,
          groupValue: value,
          onChanged: onChanged,
        );
      }).toList(),
    );
  }
}
