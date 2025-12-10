# 天气预测Python工程

# 下面是一个完整的天气预测工程，包含数据获取、预处理、模型训练和预测功能。


"""
天气预测系统
功能：获取历史天气数据，训练预测模型，预测未来天气
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import os


class WeatherPredictor:
    def __init__(self, api_key=None, city="Beijing"):
        """
        初始化天气预测器

        参数:
            api_key: OpenWeatherMap API密钥 (可选)
            city: 城市名称
        """
        self.api_key = api_key
        self.city = city
        self.model = None
        self.feature_columns = None
        self.data = None

    def fetch_historical_data(self, days=30):
        """
        获取历史天气数据

        参数:
            days: 获取过去多少天的数据

        返回:
            DataFrame: 包含历史天气数据的DataFrame
        """
        print(f"正在获取 {self.city} 的历史天气数据...")

        # 如果没有API密钥，使用模拟数据
        if not self.api_key:
            print("未提供API密钥，使用模拟数据...")
            return self._generate_mock_data(days)

        # 使用OpenWeatherMap API获取历史数据
        base_url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

        data_list = []

        for i in range(days, 0, -1):
            # 计算日期
            target_date = datetime.now() - timedelta(days=i)
            timestamp = int(target_date.timestamp())

            try:
                # 构建请求URL
                url = f"{base_url}?lat=39.9042&lon=116.4074&dt={timestamp}&appid={self.api_key}&units=metric"

                # 发送请求
                response = requests.get(url)
                response.raise_for_status()

                # 解析响应
                weather_data = response.json()

                # 提取所需数据
                daily_data = {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'temp': weather_data['current']['temp'],
                    'feels_like': weather_data['current']['feels_like'],
                    'pressure': weather_data['current']['pressure'],
                    'humidity': weather_data['current']['humidity'],
                    'wind_speed': weather_data['current']['wind_speed'],
                    'clouds': weather_data['current']['clouds']
                }

                data_list.append(daily_data)

            except Exception as e:
                print(f"获取 {target_date.strftime('%Y-%m-%d')} 数据失败: {e}")
                continue

        # 创建DataFrame
        if data_list:
            df = pd.DataFrame(data_list)
            df['date'] = pd.to_datetime(df['date'])
            self.data = df
            print(f"成功获取 {len(df)} 天的历史天气数据")
            return df
        else:
            print("无法获取历史数据，使用模拟数据...")
            return self._generate_mock_data(days)

    def _generate_mock_data(self, days):
        """生成模拟天气数据"""
        dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]

        # 生成模拟数据
        np.random.seed(42)
        base_temp = 20  # 基础温度

        data = {
            'date': dates,
            'temp': base_temp + np.random.normal(0, 5, days) + np.sin(np.arange(days) * 2 * np.pi / 7) * 3,
            'feels_like': base_temp + np.random.normal(0, 6, days) + np.sin(np.arange(days) * 2 * np.pi / 7) * 3.5,
            'pressure': 1013 + np.random.normal(0, 10, days),
            'humidity': 50 + np.random.normal(0, 15, days),
            'wind_speed': 5 + np.random.exponential(2, days),
            'clouds': np.random.randint(0, 100, days)
        }

        df = pd.DataFrame(data)
        df['temp'] = df['temp'].clip(0, 40)  # 限制温度在合理范围
        df['feels_like'] = df['feels_like'].clip(0, 45)
        df['humidity'] = df['humidity'].clip(0, 100)

        self.data = df
        print(f"生成 {len(df)} 天的模拟天气数据")
        return df

    def preprocess_data(self, df):
        """
        预处理数据，创建特征

        参数:
            df: 原始数据DataFrame

        返回:
            DataFrame: 处理后的特征DataFrame
        """
        print("正在预处理数据...")

        # 复制数据以避免修改原始数据
        df_processed = df.copy()

        # 添加时间特征
        df_processed['day_of_year'] = df_processed['date'].dt.dayofyear
        df_processed['day_of_week'] = df_processed['date'].dt.dayofweek
        df_processed['month'] = df_processed['date'].dt.month

        # 添加滞后特征（前几天的天气）
        for lag in [1, 2, 3]:
            df_processed[f'temp_lag_{lag}'] = df_processed['temp'].shift(lag)
            df_processed[f'humidity_lag_{lag}'] = df_processed['humidity'].shift(lag)
            df_processed[f'pressure_lag_{lag}'] = df_processed['pressure'].shift(lag)

        # 添加移动平均特征
        df_processed['temp_rolling_3'] = df_processed['temp'].rolling(window=3).mean()
        df_processed['pressure_rolling_3'] = df_processed['pressure'].rolling(window=3).mean()

        # 删除包含NaN的行（由于滞后特征）
        df_processed = df_processed.dropna()

        # 定义特征列和目标列
        self.feature_columns = [
            'day_of_year', 'day_of_week', 'month',
            'feels_like', 'pressure', 'humidity', 'wind_speed', 'clouds',
            'temp_lag_1', 'temp_lag_2', 'temp_lag_3',
            'humidity_lag_1', 'humidity_lag_2',
            'pressure_lag_1', 'pressure_lag_2',
            'temp_rolling_3', 'pressure_rolling_3'
        ]

        print(f"数据预处理完成，创建了 {len(self.feature_columns)} 个特征")
        return df_processed

    def train_model(self, df_processed, target='temp'):
        """
        训练预测模型

        参数:
            df_processed: 预处理后的数据
            target: 预测目标（默认为温度）

        返回:
            训练好的模型
        """
        print("正在训练模型...")

        # 准备特征和目标
        X = df_processed[self.feature_columns]
        y = df_processed[target]

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 创建并训练模型
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        # 评估模型
        y_pred = self.model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f"模型训练完成!")
        print(f"测试集平均绝对误差 (MAE): {mae:.2f}°C")
        print(f"测试集均方根误差 (RMSE): {rmse:.2f}°C")

        return self.model

    def predict_weather(self, days_ahead=3):
        """
        预测未来天气

        参数:
            days_ahead: 预测未来多少天

        返回:
            DataFrame: 包含预测结果的DataFrame
        """
        if self.model is None or self.data is None:
            print("错误: 请先获取数据并训练模型")
            return None

        print(f"正在预测未来 {days_ahead} 天的天气...")

        # 使用最近的数据作为预测起点
        last_data = self.data.iloc[-1].copy()

        predictions = []

        for day in range(1, days_ahead + 1):
            # 创建预测日期
            pred_date = datetime.now() + timedelta(days=day)

            # 准备特征数据
            features = {}

            # 基础特征
            features['day_of_year'] = pred_date.timetuple().tm_yday
            features['day_of_week'] = pred_date.weekday()
            features['month'] = pred_date.month

            # 使用最后已知值或预测值
            if day == 1:
                # 第一天使用最后已知值
                features['feels_like'] = last_data['feels_like']
                features['pressure'] = last_data['pressure']
                features['humidity'] = last_data['humidity']
                features['wind_speed'] = last_data['wind_speed']
                features['clouds'] = last_data['clouds']

                # 滞后特征使用最后几天的实际值
                if len(self.data) >= 3:
                    features['temp_lag_1'] = self.data.iloc[-1]['temp']
                    features['temp_lag_2'] = self.data.iloc[-2]['temp']
                    features['temp_lag_3'] = self.data.iloc[-3]['temp']

                    features['humidity_lag_1'] = self.data.iloc[-1]['humidity']
                    features['humidity_lag_2'] = self.data.iloc[-2]['humidity']

                    features['pressure_lag_1'] = self.data.iloc[-1]['pressure']
                    features['pressure_lag_2'] = self.data.iloc[-2]['pressure']
                else:
                    # 如果没有足够的历史数据，使用最后已知值
                    features.update({f'temp_lag_{i}': last_data['temp'] for i in range(1, 4)})
                    features.update({f'humidity_lag_{i}': last_data['humidity'] for i in range(1, 3)})
                    features.update({f'pressure_lag_{i}': last_data['pressure'] for i in range(1, 3)})

                # 移动平均
                if len(self.data) >= 3:
                    features['temp_rolling_3'] = self.data['temp'].tail(3).mean()
                    features['pressure_rolling_3'] = self.data['pressure'].tail(3).mean()
                else:
                    features['temp_rolling_3'] = last_data['temp']
                    features['pressure_rolling_3'] = last_data['pressure']
            else:
                # 后续天数使用预测值
                prev_pred = predictions[-1]

                features['feels_like'] = prev_pred['temp'] * 1.05  # 体感温度略高
                features['pressure'] = prev_pred['pressure']
                features['humidity'] = prev_pred['humidity']
                features['wind_speed'] = prev_pred['wind_speed']
                features['clouds'] = prev_pred['clouds']

                # 更新滞后特征
                if day == 2:
                    features['temp_lag_1'] = last_data['temp']
                    features['temp_lag_2'] = self.data.iloc[-2]['temp'] if len(self.data) >= 2 else last_data['temp']
                    features['temp_lag_3'] = self.data.iloc[-3]['temp'] if len(self.data) >= 3 else last_data['temp']
                elif day == 3:
                    features['temp_lag_1'] = predictions[0]['temp']
                    features['temp_lag_2'] = last_data['temp']
                    features['temp_lag_3'] = self.data.iloc[-2]['temp'] if len(self.data) >= 2 else last_data['temp']
                else:
                    features['temp_lag_1'] = predictions[-2]['temp']
                    features['temp_lag_2'] = predictions[-3]['temp']
                    features['temp_lag_3'] = predictions[-4]['temp'] if day > 4 else last_data['temp']

                # 其他滞后特征
                features['humidity_lag_1'] = prev_pred['humidity']
                features['humidity_lag_2'] = predictions[-2]['humidity'] if day > 2 else last_data['humidity']

                features['pressure_lag_1'] = prev_pred['pressure']
                features['pressure_lag_2'] = predictions[-2]['pressure'] if day > 2 else last_data['pressure']

                # 移动平均
                if day >= 3:
                    features['temp_rolling_3'] = np.mean([p['temp'] for p in predictions[-3:]])
                    features['pressure_rolling_3'] = np.mean([p['pressure'] for p in predictions[-3:]])
                else:
                    features['temp_rolling_3'] = prev_pred['temp']
                    features['pressure_rolling_3'] = prev_pred['pressure']

            # 转换为DataFrame并预测
            features_df = pd.DataFrame([features])

            # 确保所有特征都存在
            for col in self.feature_columns:
                if col not in features_df.columns:
                    features_df[col] = 0

            # 重新排列列顺序以匹配训练数据
            features_df = features_df[self.feature_columns]

            # 预测温度
            temp_pred = self.model.predict(features_df)[0]

            # 生成其他天气参数的预测（简化版）
            pred_entry = {
                'date': pred_date.strftime('%Y-%m-%d'),
                'temp': round(temp_pred, 1),
                'feels_like': round(temp_pred * 1.05, 1),
                'pressure': round(features['pressure'], 1),
                'humidity': round(np.clip(features['humidity'] + np.random.normal(0, 5), 20, 90), 1),
                'wind_speed': round(np.clip(features['wind_speed'] + np.random.exponential(0.5), 0, 20), 1),
                'clouds': round(np.clip(features['clouds'] + np.random.normal(0, 10), 0, 100), 0)
            }

            predictions.append(pred_entry)

        # 创建预测结果DataFrame
        predictions_df = pd.DataFrame(predictions)

        print("天气预测完成!")
        return predictions_df

    def save_model(self, filename='weather_model.pkl'):
        """保存训练好的模型"""
        if self.model is None:
            print("错误: 没有训练好的模型可以保存")
            return

        with open(filename, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_columns': self.feature_columns,
                'city': self.city
            }, f)

        print(f"模型已保存到 {filename}")

    def load_model(self, filename='weather_model.pkl'):
        """加载已保存的模型"""
        try:
            with open(filename, 'rb') as f:
                saved_data = pickle.load(f)

            self.model = saved_data['model']
            self.feature_columns = saved_data['feature_columns']
            self.city = saved_data.get('city', self.city)

            print(f"模型已从 {filename} 加载")
            return True
        except Exception as e:
            print(f"加载模型失败: {e}")
            return False

    def visualize_predictions(self, historical_data, predictions):
        """可视化历史数据和预测结果"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 准备数据
        hist_dates = historical_data['date']
        pred_dates = pd.to_datetime(predictions['date'])

        # 1. 温度对比
        axes[0, 0].plot(hist_dates[-10:], historical_data['temp'].tail(10), 'b-o', label='历史温度')
        axes[0, 0].plot(pred_dates, predictions['temp'], 'r--o', label='预测温度')
        axes[0, 0].set_title('温度预测')
        axes[0, 0].set_xlabel('日期')
        axes[0, 0].set_ylabel('温度 (°C)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # 2. 湿度对比
        axes[0, 1].plot(hist_dates[-10:], historical_data['humidity'].tail(10), 'g-o', label='历史湿度')
        axes[0, 1].plot(pred_dates, predictions['humidity'], 'r--o', label='预测湿度')
        axes[0, 1].set_title('湿度预测')
        axes[0, 1].set_xlabel('日期')
        axes[0, 1].set_ylabel('湿度 (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # 3. 气压对比
        axes[1, 0].plot(hist_dates[-10:], historical_data['pressure'].tail(10), 'purple', marker='o', label='历史气压')
        axes[1, 0].plot(pred_dates, predictions['pressure'], 'r--o', label='预测气压')
        axes[1, 0].set_title('气压预测')
        axes[1, 0].set_xlabel('日期')
        axes[1, 0]
