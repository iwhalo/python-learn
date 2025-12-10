import datetime
import math
import requests
import json
from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


@dataclass
class Location:
    """地理位置信息"""
    name: str
    latitude: float  # 纬度
    longitude: float  # 经度
    timezone: int  # 时区偏移（小时）


@dataclass
class SkyCondition:
    """天空条件"""
    cloud_cover: float  # 云量 (0-100%)
    humidity: float  # 湿度 (0-100%)
    wind_speed: float  # 风速 (m/s)
    temperature: float  # 温度 (°C)
    pressure: float  # 气压 (hPa)


@dataclass
class SunriseSunset:
    """日出日落时间"""
    sunrise: datetime
    sunset: datetime
    dawn: datetime
    dusk: datetime


class SkyPredictor:
    """天空现象预测器"""

    def __init__(self):
        self.locations = {
            '北京': Location('北京', 39.9042, 116.4074, 8),
            '上海': Location('上海', 31.2304, 121.4737, 8),
            '广州': Location('广州', 23.1291, 113.2644, 8),
            '成都': Location('成都', 30.5728, 104.0668, 8),
            '西安': Location('西安', 34.2639, 108.9480, 8)
        }

    def calculate_sun_position(self, location: Location, date: datetime) -> Dict:
        """计算太阳位置"""

        # 将日期转换为Julian日期
        def julian_date(date):
            a = (14 - date.month) // 12
            y = date.year + 4800 - a
            m = date.month + 12 * a - 3
            j = date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
            return j

        # 计算太阳的赤纬和时角
        j = julian_date(date)
        n = j - 2451545.0
        L = 280.46 + 0.9856474 * n  # 太阳的均近点角
        L = L % 360
        g = 357.528 + 0.9856003 * n  # 太阳的异常
        g = g % 360

        # 计算太阳赤纬
        epsilon = 23.439 - 0.0000004 * n  # 黄赤交角
        lambda_sun = L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
        lambda_sun = lambda_sun % 360

        # 太阳赤纬
        delta = math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)))

        # 计算时角
        # 这里简化计算，实际应用中需要更复杂的计算
        hour_angle = 15 * (12 - (date.hour + date.minute / 60))  # 时角

        # 计算太阳高度角和方位角
        sin_altitude = math.sin(math.radians(location.latitude)) * math.sin(delta) + \
                       math.cos(math.radians(location.latitude)) * math.cos(delta) * math.cos(math.radians(hour_angle))
        altitude = math.asin(sin_altitude)

        # 计算方位角
        cos_azimuth = (math.sin(delta) - math.sin(math.radians(location.latitude)) * sin_altitude) / \
                      (math.cos(math.radians(location.latitude)) * math.cos(altitude))

        return {
            'altitude': math.degrees(altitude),
            'azimuth': math.degrees(math.acos(cos_azimuth)),
            'delta': math.degrees(delta)
        }

    def calculate_sunrise_sunset(self, location: Location, date: datetime) -> SunriseSunset:
        """计算日出日落时间"""
        # 简化的日出日落计算
        # 实际应用中应该使用更精确的天文算法

        # 基于纬度的近似计算
        lat = math.radians(location.latitude)
        declination = 23.44 * math.cos(2 * math.pi * (date.timetuple().tm_yday - 81) / 365.25)
        declination_rad = math.radians(declination)

        # 计算太阳赤纬
        cos_hour_angle = -(math.sin(math.radians(90.833)) + math.sin(lat) * math.sin(declination_rad)) / \
                         (math.cos(lat) * math.cos(declination_rad))

        if abs(cos_hour_angle) > 1:
            # 极昼或极夜
            if cos_hour_angle > 1:
                # 极昼
                sunrise = date.replace(hour=0, minute=0)
                sunset = date.replace(hour=23, minute=59)
            else:
                # 极夜
                sunrise = date.replace(hour=0, minute=0)
                sunset = date.replace(hour=0, minute=0)
        else:
            hour_angle = math.acos(cos_hour_angle)
            hour_angle_deg = math.degrees(hour_angle)

            # 计算日出日落时间
            sunrise_hour = 12 - hour_angle_deg / 15
            sunset_hour = 12 + hour_angle_deg / 15

            sunrise = date.replace(hour=int(sunrise_hour), minute=int((sunrise_hour % 1) * 60))
            sunset = date.replace(hour=int(sunset_hour), minute=int((sunset_hour % 1) * 60))

        # 计算黎明和黄昏
        dawn = sunrise - timedelta(minutes=30)  # 黎明
        dusk = sunset + timedelta(minutes=30)  # 黄昏

        return SunriseSunset(sunrise, sunset, dawn, dusk)

    def get_weather_data(self, location: Location) -> SkyCondition:
        """获取天气数据（模拟）"""
        # 这里使用模拟数据，实际应用中应该调用天气API
        return SkyCondition(
            cloud_cover=np.random.uniform(0, 80),  # 云量
            humidity=np.random.uniform(30, 90),  # 湿度
            wind_speed=np.random.uniform(0, 10),  # 风速
            temperature=np.random.uniform(-10, 35),  # 温度
            pressure=np.random.uniform(980, 1030)  # 气压
        )

    def predict_fire_cloud_time(self, location: Location, date: datetime) -> Dict:
        """预测火烧云时间"""
        # 计算日出日落时间
        sun_times = self.calculate_sunrise_sunset(location, date)

        # 获取天气数据
        weather = self.get_weather_data(location)

        # 计算最佳观赏时间
        best_times = []

        # 朝霞时间（日出前后1小时）
        if sun_times.sunrise:
            morning_start = sun_times.sunrise - timedelta(minutes=30)
            morning_end = sun_times.sunrise + timedelta(minutes=30)
            best_times.append({
                'type': '朝霞',
                'start': morning_start,
                'end': morning_end,
                'weather': weather,
                'probability': self._calculate_cloud_probability(weather, sun_times.sunrise)
            })

        # 晚霞时间（日落前后1小时）
        if sun_times.sunset:
            evening_start = sun_times.sunset - timedelta(minutes=30)
            evening_end = sun_times.sunset + timedelta(minutes=30)
            best_times.append({
                'type': '晚霞',
                'start': evening_start,
                'end': evening_end,
                'weather': weather,
                'probability': self._calculate_cloud_probability(weather, sun_times.sunset)
            })

        # 火烧云时间（日出后1小时和日落前1小时）
        fire_cloud_times = []
        if sun_times.sunrise:
            fire_start = sun_times.sunrise + timedelta(minutes=30)
            fire_end = sun_times.sunrise + timedelta(minutes=90)
            fire_cloud_times.append({
                'type': '火烧云',
                'start': fire_start,
                'end': fire_end,
                'weather': weather,
                'probability': self._calculate_fire_probability(weather, sun_times.sunrise)
            })

        if sun_times.sunset:
            fire_start = sun_times.sunset - timedelta(minutes=90)
            fire_end = sun_times.sunset - timedelta(minutes=30)
            fire_cloud_times.append({
                'type': '火烧云',
                'start': fire_start,
                'end': fire_end,
                'weather': weather,
                'probability': self._calculate_fire_probability(weather, sun_times.sunset)
            })

        return {
            'location': location.name,
            'date': date.strftime('%Y-%m-%d'),
            'sun_times': sun_times,
            'weather': weather,
            'best_times': best_times,
            'fire_cloud_times': fire_cloud_times
        }

    def _calculate_cloud_probability(self, weather: SkyCondition, sun_time: datetime) -> float:
        """计算云量概率"""
        # 云量越低，观赏概率越高
        cloud_prob = max(0, 100 - weather.cloud_cover)
        humidity_prob = max(0, 100 - weather.humidity * 0.5)  # 湿度高会降低观赏效果
        wind_prob = max(0, 100 - weather.wind_speed * 5)  # 风速大可能影响云层形态

        return (cloud_prob + humidity_prob + wind_prob) / 3

    def _calculate_fire_probability(self, weather: SkyCondition, sun_time: datetime) -> float:
        """计算火烧云概率"""
        # 火烧云需要：
        # 1. 云量适中（不是完全晴天也不是完全阴天）
        # 2. 湿度适中
        # 3. 风速适中
        # 4. 气压稳定

        # 云量适中（30-70%）
        if 30 <= weather.cloud_cover <= 70:
            cloud_prob = 100
        else:
            cloud_prob = max(0, 100 - abs(weather.cloud_cover - 50) * 2)

        # 湿度适中（40-80%）
        if 40 <= weather.humidity <= 80:
            humidity_prob = 100
        else:
            humidity_prob = max(0, 100 - abs(weather.humidity - 60) * 2)

        # 风速适中（0-5 m/s）
        if 0 <= weather.wind_speed <= 5:
            wind_prob = 100
        else:
            wind_prob = max(0, 100 - weather.wind_speed * 10)

        # 气压稳定（1000-1020 hPa）
        if 1000 <= weather.pressure <= 1020:
            pressure_prob = 100
        else:
            pressure_prob = max(0, 100 - abs(weather.pressure - 1010) * 2)

        return (cloud_prob + humidity_prob + wind_prob + pressure_prob) / 4

    def generate_forecast_report(self, location_name: str, days: int = 3) -> List[Dict]:
        """生成未来几天的预测报告"""
        location = self.locations.get(location_name)
        if not location:
            raise ValueError(f"未找到位置: {location_name}")

        reports = []
        today = datetime.now().date()

        for i in range(days):
            date = today + timedelta(days=i)
            report = self.predict_fire_cloud_time(location, datetime.combine(date, datetime.min.time()))
            reports.append(report)

        return reports

    def plot_sky_conditions(self, location_name: str, days: int = 3):
        """绘制天空条件变化图"""
        reports = self.generate_forecast_report(location_name, days)

        dates = [datetime.strptime(report['date'], '%Y-%m-%d') for report in reports]

        # 提取数据
        cloud_cover = [report['weather'].cloud_cover for report in reports]
        humidity = [report['weather'].humidity for report in reports]
        temperature = [report['weather'].temperature for report in reports]

        # 创建图表
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # 云量
        ax1.plot(dates, cloud_cover, 'o-', color='blue', label='云量 (%)')
        ax1.set_title('未来天气云量变化')
        ax1.set_ylabel('云量 (%)')
        ax1.grid(True)
        ax1.legend()

        # 湿度
        ax2.plot(dates, humidity, 'o-', color='green', label='湿度 (%)')
        ax2.set_title('未来天气湿度变化')
        ax2.set_ylabel('湿度 (%)')
        ax2.grid(True)
        ax2.legend()

        # 温度
        ax3.plot(dates, temperature, 'o-', color='red', label='温度 (°C)')
        ax3.set_title('未来天气温度变化')
        ax3.set_ylabel('温度 (°C)')
        ax3.set_xlabel('日期')
        ax3.grid(True)
        ax3.legend()

        # 格式化x轴
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()
        plt.show()


def main():
    """主函数"""
    predictor = SkyPredictor()

    print("=== 天空现象预测系统 ===")
    print("支持的城市:", list(predictor.locations.keys()))

    # 选择城市
    city = input("请输入城市名称 (默认: 北京): ").strip()
    if not city:
        city = "北京"

    # 生成预测报告
    try:
        reports = predictor.generate_forecast_report(city, 3)

        print(f"\n=== {city} 未来3天天空现象预测 ===")
        for report in reports:
            print(f"\n日期: {report['date']}")
            print(f"位置: {report['location']}")

            # 日出日落时间
            sun_times = report['sun_times']
            print(f"日出时间: {sun_times.sunrise.strftime('%H:%M')}")
            print(f"日落时间: {sun_times.sunset.strftime('%H:%M')}")

            # 天气状况
            weather = report['weather']
            print(f"天气状况: 云量 {weather.cloud_cover:.1f}%, 湿度 {weather.humidity:.1f}%, "
                  f"风速 {weather.wind_speed:.1f}m/s, 温度 {weather.temperature:.1f}°C")

            # 最佳观赏时间
            print("\n最佳观赏时间:")
            for time_info in report['best_times']:
                print(f"  {time_info['type']}: {time_info['start'].strftime('%H:%M')} - "
                      f"{time_info['end'].strftime('%H:%M')} (概率: {time_info['probability']:.1f}%)")

            # 火烧云时间
            print("\n火烧云时间:")
            for time_info in report['fire_cloud_times']:
                print(f"  {time_info['type']}: {time_info['start'].strftime('%H:%M')} - "
                      f"{time_info['end'].strftime('%H:%M')} (概率: {time_info['probability']:.1f}%)")

        # 询问是否绘制图表
        plot_choice = input("\n是否绘制天气变化图表? (y/n): ").strip().lower()
        if plot_choice == 'y':
            predictor.plot_sky_conditions(city, 3)

    except Exception as e:
        print(f"预测过程中出现错误: {e}")


# 使用示例
def example_usage():
    """使用示例"""
    predictor = SkyPredictor()

    # 预测北京的天空现象
    print("=== 北京天空现象预测示例 ===")
    report = predictor.predict_fire_cloud_time(predictor.locations['北京'], datetime.now())

    print(f"日期: {report['date']}")
    print(f"日出时间: {report['sun_times'].sunrise.strftime('%H:%M')}")
    print(f"日落时间: {report['sun_times'].sunset.strftime('%H:%M')}")

    print("\n最佳观赏时间:")
    for time_info in report['best_times']:
        print(f"  {time_info['type']}: {time_info['start'].strftime('%H:%M')} - "
              f"{time_info['end'].strftime('%H:%M')} (概率: {time_info['probability']:.1f}%)")

    print("\n火烧云时间:")
    for time_info in report['fire_cloud_times']:
        print(f"  {time_info['type']}: {time_info['start'].strftime('%H:%M')} - "
              f"{time_info['end'].strftime('%H:%M')} (概率: {time_info['probability']:.1f}%)")


if __name__ == "__main__":
    # 可以先运行示例
    example_usage()
    print("\n" + "=" * 50 + "\n")

    # 然后运行交互式程序
    main()
