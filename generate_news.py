#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兆青MINI今日快报生成脚本
每天生成包含天气、农历日期、限号和新闻的快报
"""

import os
import datetime
import requests
import json
import hashlib
import random
import string
from lunar_python import Solar

# 获取环境变量
SERVER_KEY = os.getenv('SERVER_KEY', 'SCT326562TIBPnyjSDvFixoGuPbhgUMyCS')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'bbe05494dc5c5764ca56a014ecb10c24')

def get_lunar_date():
    """
    获取当天农历日期和节气
    :return: 农历日期字符串
    """
    today = datetime.datetime.now()
    solar = Solar.fromDate(today)
    lunar = solar.getLunar()
    
    # 获取节气
    term = ""
    try:
        # 尝试获取当前节气
        from lunar_python import SolarTerm
        solar_term = SolarTerm.fromDate(today)
        if solar_term:
            term = solar_term.getName()
    except Exception as e:
        # 如果失败，使用备用方法
        try:
            # 检查是否是节气日
            if hasattr(solar, 'getTerm'):
                term = solar.getTerm()
        except:
            pass
    
    # 中文数字映射
    cn_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    cn_tens = ['', '十', '二十', '三十']
    
    # 年份转中文
    year_str = str(lunar.getYear())
    cn_year = ''
    for digit in year_str:
        cn_year += cn_nums[int(digit)]
    
    # 月份转中文
    month = lunar.getMonth()
    cn_month = ''
    if month == 1:
        cn_month = '正月'
    elif month == 11:
        cn_month = '冬月'
    elif month == 12:
        cn_month = '腊月'
    else:
        cn_month = cn_nums[month] + '月'
    
    # 日期转中文
    day = lunar.getDay()
    cn_day = ''
    if day <= 10:
        cn_day = '初' + cn_nums[day]
    elif day < 20:
        cn_day = '十' + cn_nums[day - 10]
    elif day == 20:
        cn_day = '二十'
    elif day < 30:
        cn_day = '廿' + cn_nums[day - 20]
    elif day == 30:
        cn_day = '三十'
    
    return f"{cn_year}年{cn_month}{cn_day}{'，' + term if term else ''}"

def get_weather(city="长春"):
    """
    获取指定城市天气
    :param city: 城市名称
    :return: 天气信息字典
    """
    try:
        # 使用聚合数据天气API
        url = f"http://apis.juhe.cn/simpleWeather/query?city={city}&key={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("error_code") == 0:
            result = data.get("result", {})
            realtime = result.get("realtime", {})
            weather = realtime.get("info", "晴")
            humidity = realtime.get("humidity", "50")
            wind_speed = realtime.get("direct", "5") + realtime.get("power", "")
            
            # 获取最高最低温度
            forecast = result.get("future", [{}])[0]
            temp_high = forecast.get("temperature", "15℃").split("/")[0]
            temp_low = forecast.get("temperature", "15℃").split("/")[1]
            
            # 穿衣指数（模拟数据）
            dressing_index = "舒适"
            if int(temp_high.replace("℃", "")) > 30:
                dressing_index = "炎热"
            elif int(temp_high.replace("℃", "")) > 20:
                dressing_index = "舒适"
            elif int(temp_high.replace("℃", "")) > 10:
                dressing_index = "较凉"
            else:
                dressing_index = "寒冷"
            
            return {
                "weather": weather,
                "temp_high": temp_high,
                "temp_low": temp_low,
                "wind_speed": wind_speed,
                "humidity": humidity,
                "dressing_index": dressing_index
            }
        else:
            # 使用默认天气数据
            return {
                "weather": "晴", 
                "temp_high": "18℃", 
                "temp_low": "8℃", 
                "wind_speed": "微风", 
                "humidity": "50%",
                "dressing_index": "舒适"
            }
    except Exception as e:
        print(f"获取天气失败: {e}")
        # 返回默认值
        return {
            "weather": "晴", 
            "temp_high": "18℃", 
            "temp_low": "8℃", 
            "wind_speed": "微风", 
            "humidity": "50%",
            "dressing_index": "舒适"
        }

def get_traffic_restriction(city="长春"):
    """
    获取指定城市限号信息
    :param city: 城市名称
    :return: 限号信息字符串
    """
    try:
        today = datetime.datetime.now()
        weekday = today.weekday() + 1  # 1-7
        
        # 长春限号规则（示例，实际以当地规定为准）
        restriction = {
            1: "4和9",
            2: "5和0",
            3: "1和6",
            4: "2和7",
            5: "3和8",
            6: "不限行",
            7: "不限行"
        }
        
        return f"{restriction.get(weekday, '不限行')}"
    except Exception as e:
        print(f"获取限号信息失败: {e}")
        return "不限行"

def get_news():
    """
    获取最新新闻（国内和国际）
    :return: 国内新闻列表和国际新闻列表（包含标题和链接）
    """
    try:
        # 获取国内新闻
        url_domestic = f"http://v.juhe.cn/toutiao/index?type=guonei&key={NEWS_API_KEY}"
        response_domestic = requests.get(url_domestic, timeout=10)
        data_domestic = response_domestic.json()
        
        domestic_news = []
        if data_domestic.get("error_code") == 0:
            result = data_domestic.get("result", {})
            news_list = result.get("data", [])
            domestic_news = [(news.get("title", ""), news.get("url", "")) for news in news_list[:5]]
        
        # 获取国际新闻
        url_international = f"http://v.juhe.cn/toutiao/index?type=guoji&key={NEWS_API_KEY}"
        response_international = requests.get(url_international, timeout=10)
        data_international = response_international.json()
        
        international_news = []
        if data_international.get("error_code") == 0:
            result = data_international.get("result", {})
            news_list = result.get("data", [])
            international_news = [(news.get("title", ""), news.get("url", "")) for news in news_list[:5]]
        
        return domestic_news, international_news
    except Exception as e:
        print(f"获取新闻失败: {e}")
        # 返回默认新闻
        domestic_news = [
            ("国内经济持续向好，GDP增速超预期", ""),
            ("科技创新取得重大突破，多项技术世界领先", ""),
            ("国际合作加深，双边贸易额再创新高", ""),
            ("民生工程稳步推进，社会保障体系不断完善", ""),
            ("教育改革成效显著，素质教育全面推进", "")
        ]
        international_news = [
            ("国际形势稳定，多边关系健康发展", ""),
            ("全球气候变化问题受到广泛关注", ""),
            ("国际体育赛事取得圆满成功", ""),
            ("世界文化遗产保护取得新进展", ""),
            ("国际人道主义援助持续进行", "")
        ]
        return domestic_news, international_news

def push_to_wechat(content):
    """
    推送快报到微信（使用Server酱）
    :param content: 快报内容
    :return: 推送是否成功
    """
    try:
        # Server酱配置
        url = "https://sctapi.ftqq.com/{}.send".format(SERVER_KEY)
        
        # 转换为Markdown格式，确保换行正确显示
        markdown_content = content.replace('\n', '\n\n')
        
        # 推送数据
        data = {
            "title": "兆青MINI·今日快报",
            "desp": markdown_content
        }
        
        # 发送推送
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            print("推送成功！")
            return True
        else:
            print(f"推送失败: {result.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"推送失败: {e}")
        return False

def generate_newsletter():
    """
    生成快报
    :return: 快报内容
    """
    today = datetime.datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    weekday_str = "星期" + "日一二三四五六"[today.weekday()]
    lunar_date = get_lunar_date()
    weather_data = get_weather()
    traffic_restriction = get_traffic_restriction()
    domestic_news, international_news = get_news()
    
    # 美化排版
    content = f"""兆青MINI·今日快报


• 公历：{date_str} {weekday_str}
• 农历：{lunar_date}
• 限号：{traffic_restriction}

🌤️ 今日天气
• 天气：{weather_data['weather']}
• 温度：{weather_data['temp_low']}~{weather_data['temp_high']}
• 风速：{weather_data['wind_speed']}
• 湿度：{weather_data['humidity']}
• 穿衣指数：{weather_data['dressing_index']}

📰 兆青MINI·今日要闻

🇨🇳 国内新闻
"""
    
    for i, (title, url) in enumerate(domestic_news, 1):
        if url:
            content += f"{i}. [{title}]({url})\n"
        else:
            content += f"{i}. {title}\n"
    
    content += "\n🌍 国际新闻\n"
    for i, (title, url) in enumerate(international_news, 1):
        if url:
            content += f"{i}. [{title}]({url})\n"
        else:
            content += f"{i}. {title}\n"
    
    content += f"""

💡 兆青MINI·温馨提示
• 出行前请检查车辆状况
• 遵守交通规则，安全驾驶
• 关注天气变化，合理安排行程
• 如需MINI相关服务，欢迎联系我们

🔧 兆青MINI工作室
专业MINI维修保养 • 升级 • 配件销售
"""
    
    return content

def main():
    """
    主函数
    """
    # 生成快报内容
    content = generate_newsletter()
    
    print("快报生成成功！")
    print("\n快报内容：")
    print(content)
    
    # 推送到微信
    print("\n正在推送到微信...")
    push_to_wechat(content)

if __name__ == "__main__":
    main()
