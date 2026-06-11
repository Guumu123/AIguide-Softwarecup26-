from typing import List, Dict
from app.schemas.route import RouteRecommendRequest, RouteRecommendResponse, AttractionPoint

class RouteRecommendationService:
    # 兴趣标签映射到景点属性
    INTEREST_MAP = {
        '历史': ['祥符禅寺', '阿育王柱', '无尽意斋'],
        '自然风光': ['梵天花海', '五灯湖', '鹿鸣谷'],
        '佛教文化': ['灵山大佛', '九龙灌浴', '灵山梵宫', '五印坛城'],
        '非遗艺术': ['灵山梵宫', '曼飞龙塔'],
        '亲子': ['百子戏弥勒', '九龙灌浴']
    }

    # 景点-讲解侧重点
    HIGHLIGHTS_MAP = {
        '祥符禅寺': '侧重文化典故、年代背景',
        '阿育王柱': '侧重历史由来与石刻艺术',
        '无尽意斋': '侧重文化底蕴与静谧氛围',
        '梵天花海': '侧重季节性花卉与景观美学',
        '五灯湖': '侧重夜景灯光与生态特色',
        '鹿鸣谷': '侧重亲近自然与鹿群互动',
        '灵山大佛': '侧重建造工艺与佛教内涵',
        '九龙灌浴': '侧重《本行经》诞生传说与动态表演',
        '灵山梵宫': '侧重东阳木雕、琉璃、油画艺术',
        '五印坛城': '侧重藏传佛教文化与建筑特色',
        '曼飞龙塔': '侧重傣族雕刻艺术',
        '百子戏弥勒': '侧重互动体验与趣味故事'
    }

    def recommend(self, request: RouteRecommendRequest) -> Dict:
        # 1. 根据兴趣选择景点
        recommended_attractions = []
        for interest in request.interests:
            if interest in self.INTEREST_MAP:
                recommended_attractions.extend(self.INTEREST_MAP[interest])
        
        # 去重并保留顺序
        recommended_attractions = list(dict.fromkeys(recommended_attractions))
        
        # 2. 根据画像调整风格
        # 亲子家庭 -> 亲子互动型
        # 老年游客 -> 学术严谨型
        # 年轻情侣 -> 轻松故事型
        # 独行游客 -> 自由探索型
        speech_style = '自由探索型'
        if request.group_size > 1:
            if request.age < 12: speech_style = '亲子互动型'
            elif request.age > 60: speech_style = '学术严谨型'
            else: speech_style = '轻松故事型'
        
        # 3. 构造路线
        route_list = []
        speech_highlights = {}
        for i, name in enumerate(recommended_attractions):
            highlight = self.HIGHLIGHTS_MAP.get(name, "通用讲解")
            route_list.append(AttractionPoint(
                attraction_id=f"LS-{i+1:03d}",
                name=name,
                duration="45分钟",
                order=i+1,
                highlights=highlight
            ))
            speech_highlights[f"LS-{i+1:03d}"] = highlight

        # 4. 汇总返回
        return {
            'route': route_list,
            'total_duration': f"{len(route_list) * 0.8:.1f}小时",
            'estimated_cost': {'ticket': 210, 'food': 150, 'shopping': 100},
            'speech_highlights': speech_highlights,
            'speech_style': speech_style,
            'tips': "建议上午9:00入园，关注当日表演时间表。"
        }

route_service = RouteRecommendationService()
