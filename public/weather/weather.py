import requests
import json

# --- 配置和全局变量 ---
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
CITY_LIST_URL = 'https://www.amap.com/service/cityList'
WEATHER_API_URL = 'https://www.amap.com/service/weather'

# --- 功能函数 1：获取所有城市数据 ---
def get_all_cities():
    """从高德API获取所有城市列表数据"""
    try:
        response = requests.get(CITY_LIST_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {}).get("cityData", {}).get("provinces", {})
    except requests.exceptions.RequestException as e:
        print(f"获取城市列表失败: {e}")
        return None

# --- 功能函数 2：根据用户输入查找并选择城市 ---
def find_and_select_city(city_query, all_city_data):
    """从城市数据中查找匹配项，并让用户选择"""
    if not all_city_data:
        return None, None

    matching_cities = []
    city_query_lower = city_query.lower().replace(" ", "")
    for province_code, province in all_city_data.items():
        if city_query_lower in province["spell"].lower() or city_query_lower in province["label"]:
            matching_cities.append({"name": province["label"], "adcode": province["adcode"], "level": "province"})
        if "cities" in province:
            for city_info in province["cities"]:
                if city_query_lower in city_info["spell"].lower() or city_query_lower in city_info["label"]:
                    matching_cities.append({"name": city_info["label"], "adcode": city_info["adcode"], "province": province["label"], "level": "city"})
    
    selected_adcode = None
    selected_name = None
    
    if not matching_cities:
        print("未找到匹配的城市")
    elif len(matching_cities) == 1:
        selected_adcode = matching_cities[0]['adcode']
        selected_name = matching_cities[0]['name']
        print(f"自动为您选择: {selected_name}")
    else:
        print(f"找到 {len(matching_cities)} 个匹配的城市:")
        for i, city in enumerate(matching_cities, 1):
            if city["level"] == "province":
                print(f"{i}. {city['name']} (省/直辖市) - 编码: {city['adcode']}")
            else:
                print(f"{i}. {city['name']} (位于{city['province']}) - 编码: {city['adcode']}")
        try:
            selection = int(input("\n请输入城市序号选择具体城市: "))
            if 1 <= selection <= len(matching_cities):
                selected_adcode = matching_cities[selection-1]['adcode']
                selected_name = matching_cities[selection-1]['name']
            else:
                print("无效的选择")
        except ValueError:
            print("请输入有效的数字")
            
    return selected_adcode, selected_name

# --- 功能函数 3：根据 adcode 获取天气信息 ---
def get_weather(adcode, city_name):
    """根据给定的 adcode 获取天气信息"""
    print(f"\n正在获取{city_name}的天气信息...\n")
    params = {'adcode': adcode}
    try:
        response = requests.get(WEATHER_API_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        if weather_data.get("status") == "1":

            data = weather_data.get("data", {}).get("data", [{}])

            weather_name = data[0].get("live", {}).get("weather_name")

            weather_code = data[0].get("live", {}).get("weather_code")
            weather_description = get_weather_description(weather_code)

            temperature = data[0].get("live", {}).get("temperature")

            print(f"查询成功！\n\n{city_name}当前天气：")
            print("="*30)
            print(f"\n天气状况: {weather_name} - {temperature}°C   {weather_description}")

            # --- 添加天气预报 ---
            print("\n--- 天气预报 ---")
            if len(data) > 1:
                # 今天预报
                today_forecast = data[0].get("forecast_data", [{}])[0]
                print(f"\n【今天 - {data[0].get('forecast_date')}】")
                print(f"  天气: {today_forecast.get('weather_name', 'N/A')}, 温度: {today_forecast.get('min_temp', 'N/A')}°C ~ {today_forecast.get('max_temp', 'N/A')}°C")
                print(f"  风力: {today_forecast.get('wind_direction_desc', 'N/A')} {today_forecast.get('wind_power_desc', 'N/A')} 级")

                # 明天预报
                tomorrow_forecast = data[1].get("forecast_data", [{}])[0]
                print(f"\n【明天 - {data[1].get('forecast_date')}】")
                print(f"  天气: {tomorrow_forecast.get('weather_name', 'N/A')}, 温度: {tomorrow_forecast.get('min_temp', 'N/A')}°C ~ {tomorrow_forecast.get('max_temp', 'N/A')}°C")
                print(f"  风力: {tomorrow_forecast.get('wind_direction_desc', 'N/A')} {tomorrow_forecast.get('wind_power_desc', 'N/A')} 级")
                print("="*30)
            else:
                print("未能获取到详细的预报信息。")

        else:
            print("获取天气失败，API返回错误信息。")

    except requests.exceptions.RequestException as e:
        print(f"请求天气API时发生错误: {e}")

# --- 功能函数 4：根据 weather_code 获取天气描述 ---
def get_weather_description(weather_code):
    """根据天气代码获取天气描述"""
    with open('weather_code.json', 'r', encoding='utf-8') as f:
        weather_codes = json.load(f)
    return weather_codes.get(weather_code, "未知天气")

# --- 主函数：程序的入口和流程控制 ---
def main():
    """程序主入口"""
    all_city_data = get_all_cities()
    if not all_city_data:
        return

    city_input = input("请输入城市名称（如'北京'或'beijing'）：").strip()
    selected_adcode, selected_name = find_and_select_city(city_input, all_city_data)

    if selected_adcode:
        get_weather(selected_adcode, selected_name)

# --- 程序的启动点 ---
if __name__ == "__main__":
    main()