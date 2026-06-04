import 'package:flutter/material.dart';

class Attraction {
  final String name;
  final String duration;
  final List<String> highlights;
  final String imageUrl;

  Attraction({
    required this.name,
    required this.duration,
    required this.highlights,
    required this.imageUrl,
  });
}

class RouteView extends StatelessWidget {
  const RouteView({super.key});

  @override
  Widget build(BuildContext context) {
    // Mock data based on document requirements
    final List<Attraction> route = [
      Attraction(
        name: '大雄宝殿',
        duration: '30分钟',
        highlights: ['历史文化', '建筑特色'],
        imageUrl: 'https://via.placeholder.com/150',
      ),
      Attraction(
        name: '藏经阁',
        duration: '20分钟',
        highlights: ['经书典籍', '禅意空间'],
        imageUrl: 'https://via.placeholder.com/150',
      ),
      Attraction(
        name: '塔林',
        duration: '45分钟',
        highlights: ['佛教艺术', '历代高僧'],
        imageUrl: 'https://via.placeholder.com/150',
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('个性化路线')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildOverview(),
            const SizedBox(height: 24),
            const Text(
              '游览顺序',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            ...route.asMap().entries.map((entry) {
              return _buildTimelineItem(context, entry.value, entry.key == route.length - 1);
            }).toList(),
          ],
        ),
      ),
    );
  }

  Widget _buildOverview() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildInfoItem(Icons.timer, '预计时长', '2.5小时'),
                _buildInfoItem(Icons.directions_walk, '总距离', '1.8公里'),
                _buildInfoItem(Icons.attach_money, '预估消费', '¥0'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoItem(IconData icon, String label, String value) {
    return Column(
      children: [
        Icon(icon, color: Colors.blue),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildTimelineItem(BuildContext context, Attraction attraction, bool isLast) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            const CircleAvatar(
              radius: 6,
              backgroundColor: Colors.blue,
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 120,
                color: Colors.blue.withOpacity(0.3),
              ),
          ],
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Card(
                margin: const EdgeInsets.only(bottom: 16),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: Image.network(
                          attraction.imageUrl,
                          width: 80,
                          height: 80,
                          fit: BoxFit.cover,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              attraction.name,
                              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                            ),
                            Text('建议停留: ${attraction.duration}'),
                            const SizedBox(height: 8),
                            Wrap(
                              spacing: 4,
                              children: attraction.highlights.map((h) {
                                return Chip(
                                  label: Text(h, style: const TextStyle(fontSize: 10)),
                                  padding: EdgeInsets.zero,
                                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                                );
                              }).toList(),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
