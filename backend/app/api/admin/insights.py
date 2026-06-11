from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_admin
from typing import Optional
import random

router = APIRouter()

@router.get('/overview', dependencies=[Depends(get_current_admin)])
async def get_insight_overview():
    return {
        "total_tourists": 142560,
        "avg_satisfaction": 4.6,
        "avg_cost": 358.5,
        "avg_duration": 3.2,
        "peak_hours": ["10:00-11:00", "14:00-15:00"],
        "peak_season": ["五一", "十一", "春节"]
    }

@router.get('/portrait', dependencies=[Depends(get_current_admin)])
async def get_portrait():
    """游客画像 - 雷达图数据"""
    return {
        "clusters": [
            {
                "type": "亲子家庭", "tag": "success", "ratio": 35, "avg_age": 35,
                "avg_cost": 520, "avg_satisfaction": 4.7,
                "preferences": {"文化偏好": 60, "自然风光": 40, "互动体验": 90, "静谧禅修": 30, "美食购物": 70},
                "hot_attractions": ["百子戏弥勒", "九龙灌浴", "灵山大佛"],
                "suggestion": "增设亲子互动项目，推出家庭套票优惠"
            },
            {
                "type": "年轻情侣", "tag": "primary", "ratio": 28, "avg_age": 26,
                "avg_cost": 380, "avg_satisfaction": 4.5,
                "preferences": {"文化偏好": 50, "自然风光": 80, "互动体验": 60, "静谧禅修": 40, "美食购物": 60},
                "hot_attractions": ["梵天花海", "五灯湖", "灵山梵宫"],
                "suggestion": "开发夜景游览线路，增加拍照打卡点"
            },
            {
                "type": "老年游客", "tag": "warning", "ratio": 22, "avg_age": 65,
                "avg_cost": 210, "avg_satisfaction": 4.8,
                "preferences": {"文化偏好": 90, "自然风光": 50, "互动体验": 20, "静谧禅修": 80, "美食购物": 30},
                "hot_attractions": ["灵山大佛", "祥符禅寺", "五印坛城"],
                "suggestion": "增加休息设施，提供慢行游览解说"
            },
            {
                "type": "独行游客", "tag": "info", "ratio": 15, "avg_age": 32,
                "avg_cost": 310, "avg_satisfaction": 4.3,
                "preferences": {"文化偏好": 70, "自然风光": 70, "互动体验": 30, "静谧禅修": 70, "美食购物": 20},
                "hot_attractions": ["灵山梵宫", "无尽意斋", "鹿鸣谷"],
                "suggestion": "推出单人游览套餐，优化自助讲解体验"
            }
        ]
    }

@router.get('/gender-cost', dependencies=[Depends(get_current_admin)])
async def get_gender_cost():
    return {
        "categories": ["门票", "餐饮", "购物", "娱乐", "交通"],
        "male": [180, 120, 150, 80, 60],
        "female": [170, 130, 180, 85, 55],
        "total_male": 590,
        "total_female": 620
    }

@router.get('/age-satisfaction', dependencies=[Depends(get_current_admin)])
async def get_age_satisfaction():
    data = []
    for age in [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]:
        data.append({
            "age": age,
            "avg_satisfaction": round(3.5 + random.random() * 1.5, 1),
            "count": random.randint(500, 5000)
        })
    return {"scatter_data": data}

@router.get('/duration', dependencies=[Depends(get_current_admin)])
async def get_duration_distribution():
    return {
        "buckets": ["0-1h", "1-2h", "2-3h", "3-4h", "4-5h", "5-6h", "6h+"],
        "counts": [1520, 8500, 18540, 22100, 16800, 9200, 3900]
    }
