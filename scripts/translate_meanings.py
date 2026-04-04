#!/usr/bin/env python3
"""
Translate English meanings to Chinese for nouns.json entries that lack Chinese.
Uses a combination of:
1. Direct English-Chinese dictionary mapping
2. Japanese kanji → Chinese meaning inference
3. Common pattern matching
"""

import json
import re
import sys

# English to Chinese dictionary for common translations
EN_ZH = {
    # Basic
    "to open": "打开", "to close": "关闭", "to be": "在；存在", "to have": "有",
    "to raise": "举起；抬起", "to lift": "抬起", "to sell": "卖", "to buy": "买",
    "to answer": "回答", "to reply": "回答", "to finish": "结束", "to wear": "穿",
    "to put on": "穿上；戴上", "to call": "打电话", "to sit down": "坐下",
    "to become": "变成", "to bathe": "沐浴", "to shower": "淋浴", "to tie": "系",
    "to fasten": "系紧", "to tighten": "勒紧", "to copy": "复制", "to dial": "拨打",
    "to walk": "走路", "to run": "跑", "to swim": "游泳", "to fly": "飞",
    "to sing": "唱", "to dance": "跳舞", "to play": "玩", "to study": "学习",
    "to teach": "教", "to learn": "学", "to work": "工作", "to rest": "休息",
    "to sleep": "睡觉", "to wake up": "醒来", "to eat": "吃", "to drink": "喝",
    "to cook": "做饭", "to wash": "洗", "to clean": "打扫", "to read": "读",
    "to write": "写", "to speak": "说", "to listen": "听", "to see": "看",
    "to look": "看", "to watch": "看", "to wait": "等", "to meet": "见面",
    "to think": "想", "to know": "知道", "to understand": "理解", "to forget": "忘记",
    "to remember": "记住", "to believe": "相信", "to decide": "决定",
    "to choose": "选择", "to use": "使用", "to make": "做", "to break": "打破",
    "to fix": "修理", "to change": "改变", "to move": "移动", "to stop": "停止",
    "to start": "开始", "to begin": "开始", "to end": "结束", "to continue": "继续",
    "to return": "返回", "to go": "去", "to come": "来", "to enter": "进入",
    "to leave": "离开", "to arrive": "到达", "to turn": "转", "to cross": "穿过",
    "to push": "推", "to pull": "拉", "to carry": "搬", "to hold": "拿",
    "to give": "给", "to receive": "收到", "to send": "送", "to take": "拿；带",
    "to borrow": "借", "to lend": "借出", "to pay": "付", "to cost": "花费",
    "to check": "检查", "to try": "尝试", "to practice": "练习",
    "to pass": "通过", "to fail": "失败", "to win": "赢", "to lose": "输",
    "to help": "帮助", "to save": "保存；救", "to protect": "保护",
    "to stand": "站", "to climb": "爬",

    # Nouns
    "breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐", "meal": "饭；餐",
    "rice": "米饭", "food": "食物", "water": "水", "tea": "茶",
    "coffee": "咖啡", "milk": "牛奶", "sugar": "糖", "salt": "盐",
    "egg": "鸡蛋", "meat": "肉", "fish": "鱼", "vegetable": "蔬菜",
    "fruit": "水果", "bread": "面包", "cake": "蛋糕",
    "foot": "脚", "leg": "腿", "hand": "手", "head": "头",
    "face": "脸", "eye": "眼睛", "ear": "耳朵", "mouth": "嘴",
    "nose": "鼻子", "hair": "头发", "body": "身体",
    "apartment": "公寓", "house": "房子", "room": "房间", "door": "门",
    "window": "窗户", "floor": "地板", "wall": "墙", "roof": "屋顶",
    "kitchen": "厨房", "bathroom": "浴室", "toilet": "厕所",
    "bag": "包", "basket": "篮子", "cup": "杯子", "plate": "盘子",
    "dish": "盘子", "vase": "花瓶", "calendar": "日历",
    "river": "河", "mountain": "山", "sea": "海", "lake": "湖",
    "forest": "森林", "park": "公园", "garden": "花园",
    "car": "汽车", "bus": "公交车", "train": "电车", "airplane": "飞机",
    "bicycle": "自行车", "taxi": "出租车",
    "school": "学校", "university": "大学", "library": "图书馆",
    "hospital": "医院", "station": "车站", "airport": "机场",
    "restaurant": "餐厅", "hotel": "酒店", "store": "商店", "shop": "店",
    "bank": "银行", "post office": "邮局",
    "morning": "早上", "afternoon": "下午", "evening": "晚上", "night": "夜晚",
    "today": "今天", "tomorrow": "明天", "yesterday": "昨天",
    "week": "周", "month": "月", "year": "年", "season": "季节",
    "spring": "春天", "summer": "夏天", "autumn": "秋天", "winter": "冬天",
    "weather": "天气", "rain": "雨", "snow": "雪", "wind": "风", "cloud": "云",
    "friend": "朋友", "family": "家庭", "parent": "父母",
    "father": "父亲", "mother": "母亲", "brother": "兄弟", "sister": "姐妹",
    "child": "孩子", "baby": "婴儿", "man": "男人", "woman": "女人",
    "teacher": "老师", "student": "学生", "doctor": "医生",
    "police officer": "警察", "policeman": "警察",
    "foreigner": "外国人", "marriage": "结婚",
    "shopping": "购物", "walk": "散步", "stroll": "散步",
    "English": "英语", "Japanese": "日语", "Chinese": "中文",
    "dictionary": "字典", "letter": "信",
    "color": "颜色", "yellow": "黄色", "red": "红色", "blue": "蓝色",
    "white": "白色", "black": "黑色", "green": "绿色",
    "good": "好的", "bad": "坏的", "big": "大的", "small": "小的",
    "new": "新的", "old": "旧的", "same": "相同的", "different": "不同的",
    "various": "各种各样的", "enough": "足够",
    "no": "不", "yes": "是", "well": "那么",
    "however": "但是", "because": "因为", "if": "如果",
    "there": "那里", "here": "这里", "over there": "那边",
    "this way": "这边", "that place": "那个地方",
    "immediately": "马上", "soon": "很快", "already": "已经",
    "still": "还", "always": "总是", "sometimes": "有时",
    "never": "从不", "perhaps": "也许", "probably": "大概",
    "very": "非常", "a little": "一点点", "not very": "不太",
    "how many": "几个", "how much": "多少", "how old": "几岁",
    "how": "怎么样", "in what way": "以何种方式",
    "best": "最好的", "first": "第一", "number one": "第一名",
    "together": "一起", "alone": "独自",
    "plan": "计划", "project": "项目", "schedule": "日程",
    "gram": "克", "shower": "淋浴",
    "splendid": "很好", "tolerably": "还行",
    "surplus": "剩余",
    "coat": "外套", "jacket": "夹克",
    "uncle": "叔叔", "aunt": "阿姨",
    "bath": "洗澡", "boxed lunch": "便当",
    "katakana": "片假名", "kanji": "汉字",
    "Chinese character": "汉字",
    "class": "班级",
    "cloudiness": "阴天", "cloudy weather": "多云",
    "to become cloudy": "变阴", "to become dim": "变暗",
    "automobile": "汽车",
    "marriage": "结婚",
    "such": "这样的", "like this": "像这样",
    "year after next": "后年",
    "five days": "五天", "nine days": "九天",
    "five things": "五个", "nine things": "九个",
    "fifth day of the month": "五号",
    "ninth day of the month": "九号",
    "home": "家", "family": "家庭",
    "correct": "正确", "wrong": "错误",
    "practice": "练习", "test": "测试", "exam": "考试",
    "question": "问题", "answer": "回答",
    "meaning": "意思", "example": "例子",
    "word": "单词", "sentence": "句子", "grammar": "语法",
    "culture": "文化", "history": "历史", "economy": "经济",
    "politics": "政治", "science": "科学", "technology": "技术",
    "art": "艺术", "music": "音乐", "movie": "电影",
    "book": "书", "newspaper": "报纸", "magazine": "杂志",
    "photo": "照片", "picture": "图片",
    "telephone": "电话", "computer": "电脑", "internet": "互联网",
    "email": "邮件", "message": "消息",
    "money": "钱", "price": "价格", "cost": "费用",
    "job": "工作", "company": "公司", "office": "办公室",
    "meeting": "会议", "business": "商务",
    "health": "健康", "medicine": "药", "illness": "病",
    "life": "生活", "experience": "经验", "memory": "记忆",
    "dream": "梦", "hope": "希望", "fear": "恐惧",
    "feeling": "感觉", "heart": "心", "mind": "心理",
    "reason": "理由", "cause": "原因", "result": "结果",
    "problem": "问题", "trouble": "麻烦",
    "place": "地方", "area": "地区", "country": "国家",
    "city": "城市", "town": "城镇", "village": "村庄",
    "street": "街道", "road": "道路", "bridge": "桥",
    "building": "建筑", "temple": "寺庙", "shrine": "神社",
    "event": "活动", "festival": "祭典", "ceremony": "仪式",
    "game": "游戏", "sport": "运动", "travel": "旅行",
    "hobby": "爱好", "interest": "兴趣",
    "the day before yesterday": "前天", "the day after tomorrow": "后天",
    "last week": "上周", "next week": "下周",
    "last month": "上个月", "next month": "下个月",
    "last year": "去年", "next year": "明年",
    "year before last": "前年",
}


def translate_one(word: str, en_meaning: str) -> str:
    """Try to translate an English meaning to Chinese."""
    en = en_meaning.strip()

    # Direct full match
    if en.lower() in EN_ZH:
        return EN_ZH[en.lower()]

    # Split by semicolons/commas and try each part
    parts = re.split(r'[;；]', en)
    zh_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Try direct match
        low = part.lower()
        if low in EN_ZH:
            zh_parts.append(EN_ZH[low])
            continue

        # Try stripping parenthetical
        core = re.sub(r'\s*\(.*?\)\s*', '', part).strip().lower()
        if core in EN_ZH:
            zh_parts.append(EN_ZH[core])
            continue

        # Try sub-parts split by comma
        subparts = [s.strip().lower() for s in part.split(',')]
        matched = [EN_ZH[s] for s in subparts if s in EN_ZH]
        if matched:
            zh_parts.append('；'.join(dict.fromkeys(matched)))  # dedupe
            continue

        # Try "to X" verb pattern
        if low.startswith('to '):
            verb = low[3:].split(',')[0].split('(')[0].strip()
            key = 'to ' + verb
            if key in EN_ZH:
                zh_parts.append(EN_ZH[key])
                continue

        # Not found, keep English
        zh_parts.append(part)

    result = '；'.join(zh_parts) if zh_parts else en
    return result


def main():
    with open('public/data/nouns.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    levels = sys.argv[1:] if len(sys.argv) > 1 else ['N5', 'N4']

    translated = 0
    still_en = 0
    for item in data:
        if item.get('level') not in levels:
            continue
        m = item.get('meaning', '')
        if re.search(r'[\u4e00-\u9fff]', m):
            continue  # already Chinese

        zh = translate_one(item['word'], m)

        # Check if still English
        if not re.search(r'[\u4e00-\u9fff]', zh):
            still_en += 1
            print(f'  [STILL EN] {item["word"]}|{m}|{zh}')
        else:
            translated += 1

        item['meaning'] = zh

    with open('public/data/nouns.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\nLevels: {levels}')
    print(f'Translated: {translated}')
    print(f'Still English: {still_en}')


if __name__ == '__main__':
    main()
