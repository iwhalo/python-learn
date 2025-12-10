# 天气预测Python工程

下面是一个完整的天气预测工程，包含数据获取、预处理、模型训练和预测功能。

```python
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
        
        all_data = []
        
        for i in range(days, 0, -1):
            target_date = datetime.now() - timedelta(days=i)
            timestamp = int(target_date.timestamp())
            
            params = {
                'lat': '39.9042',  # 北京纬度
                'lon': '116.4074',  # 北京经度
                'dt': timestamp,
                'appid': self.api_key,
                'units': 'metric'  # 使用摄氏度
            }
            
            try:
                response = requests.get(base_url, params=params)
                data = response.json()
                
                if 'current' in data:
                    current = data['current']
                    daily_data = {
                        'date': datetime.fromtimestamp(current['dt']).strftime('%Y-%m-%d'),
                        'temperature': current['temp'],
                        'feels_like': current['feels_like'],
                        'pressure': current['pressure'],
                        'humidity': current['humidity'],
                        'wind_speed': current['wind_speed'],
                        'clouds': current.get('clouds', 0),
                        'weather_main': current['weather'][0]['main'] if current['weather'] else 'Unknown'
                    }
                    all_data.append(daily_data)
                    
            except Exception as e:
                print(f"获取第{i}天数据时出错: {e}")
                continue
        
        if not all_data:
            print("无法获取API数据，使用模拟数据...")
            return self._generate_mock_data(days)
        
        df = pd.DataFrame(all_data)
        self.data = df
        print(f"成功获取 {len(df)} 天的历史数据")
        return df
    
    def _generate_mock_data(self, days=30):
        """生成模拟天气数据"""
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, 0, -1)]
        
        # 生成模拟数据
        np.random.seed(42)
        base_temp = 20  # 基础温度
        
        data = {
            'date': dates,
            'temperature': base_temp + np.random.normal(0, 5, days) + np.sin(np.arange(days) * 0.2) * 10,
            'feels_like': base_temp + np.random.normal(0, 5, days) + np.sin(np.arange(days) * 0.2) * 10 + np.random.normal(0, 2, days),
            'pressure': 1013 + np.random.normal(0, 10, days),
            'humidity': np.clip(50 + np.random.normal(0, 20, days), 10, 100),
            'wind_speed': np.clip(np.random.exponential(3, days), 0, 20),
            'clouds': np.random.randint(0, 100, days),
            'weather_main': np.random.choice(['Clear', 'Clouds', 'Rain', 'Snow'], days, p=[0.4, 0.3, 0.2, 0.1])
        }
        
        df = pd.DataFrame(data)
        self.data = df
        print(f"生成 {len(df)} 天的模拟数据")
        return df
    
    def preprocess_data(self, df):
        """
        预处理数据，为模型训练做准备
        
        参数:
            df: 原始数据DataFrame
            
        返回:
            tuple: (特征数据, 目标数据)
        """
        print("正在预处理数据...")
        
        # 复制数据以避免修改原始数据
        df_processed = df.copy()
        
        # 将日期转换为数值特征
        df_processed['date'] = pd.to_datetime(df_processed['date'])
        df_processed['day_of_year'] = df_processed['date'].dt.dayofyear
        df_processed['month'] = df_processed['date'].dt.month
        df_processed['day'] = df_processed['date'].dt.day
        
        # 对天气类型进行编码
        weather_dummies = pd.get_dummies(df_processed['weather_main'], prefix='weather')
        df_processed = pd.concat([df_processed, weather_dummies], axis=1)
        
        # 添加滞后特征（前一天的天气）
        for col in ['temperature', 'humidity', 'pressure', 'wind_speed']:
            df_processed[f'{col}_lag1'] = df_processed[col].shift(1)
        
        # 添加移动平均特征
        df_processed['temp_3day_avg'] = df_processed['temperature'].rolling(window=3).mean()
        
        # 删除包含NaN的行
        df_processed = df_processed.dropna()
        
        # 定义特征列和目标列
        feature_cols = ['day_of_year', 'month', 'day', 'pressure', 'humidity', 
                       'wind_speed', 'clouds', 'temperature_lag1', 'humidity_lag1',
                       'pressure_lag1', 'wind_speed_lag1', 'temp_3day_avg']
        
        # 添加天气类型特征列
        weather_cols = [col for col in df_processed.columns if col.startswith('weather_')]
        feature_cols.extend(weather_cols)
        
        self.feature_columns = feature_cols
        
        # 目标变量：明天的温度
        df_processed['temperature_tomorrow'] = df_processed['temperature'].shift(-1)
        
        # 删除最后一行（没有明天的温度）
        df_processed = df_processed.iloc[:-1]
        
        X = df_processed[feature_cols]
        y = df_processed['temperature_tomorrow']
        
        print(f"数据预处理完成，特征数量: {len(feature_cols)}")
        return X, y
    
    def train_model(self, X, y, test_size=0.2):
        """
        训练预测模型
        
        参数:
            X: 特征数据
            y: 目标数据
            test_size: 测试集比例
            
        返回:
            dict: 模型评估指标
        """
        print("正在训练模型...")
        
        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # 创建并训练随机森林模型
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # 在测试集上评估模型
        y_pred = self.model.predict(X_test)
        
        # 计算评估指标
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        # 计算准确率（温度误差在2度内视为正确）
        accuracy = np.mean(np.abs(y_test - y_pred) <= 2) * 100
        
        metrics = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'Accuracy (%)': accuracy,
            '训练样本数': len(X_train),
            '测试样本数': len(X_test)
        }
        
        print("模型训练完成!")
        print(f"平均绝对误差 (MAE): {mae:.2f}°C")
        print(f"均方根误差 (RMSE): {rmse:.2f}°C")
        print(f"预测准确率 (误差≤2°C): {accuracy:.1f}%")
        
        return metrics
    
    def predict_next_days(self, days=7):
        """
        预测未来几天的天气
        
        参数:
            days: 预测未来多少天
            
        返回:
            DataFrame: 包含预测结果的DataFrame
        """
        if self.model is None or self.data is None:
            raise ValueError("请先获取数据并训练模型")
        
        print(f"正在预测未来 {days} 天的天气...")
        
        # 使用最后一天的数据作为起点
        last_data = self.data.iloc[-1:].copy()
        
        predictions = []
        
        for i in range(1, days + 1):
            # 准备预测数据
            pred_date = datetime.now() + timedelta(days=i)
            
            # 创建特征行
            features = {}
            
            # 基本日期特征
            features['day_of_year'] = pred_date.timetuple().tm_yday
            features['month'] = pred_date.month
            features['day'] = pred_date.day
            
            # 使用最后已知的天气数据
            features['pressure'] = last_data['pressure'].values[0]
            features['humidity'] = last_data['humidity'].values[0]
            features['wind_speed'] = last_data['wind_speed'].values[0]
            features['clouds'] = last_data['clouds'].values[0]
            
            # 滞后特征
            features['temperature_lag1'] = last_data['temperature'].values[0]
            features['humidity_lag1'] = last_data['humidity'].values[0]
            features['pressure_lag1'] = last_data['pressure'].values[0]
            features['wind_speed_lag1'] = last_data['wind_speed'].values[0]
            
            # 移动平均特征
            features['temp_3day_avg'] = last_data['temperature'].values[0]
            
            # 天气类型特征
            for col in self.feature_columns:
                if col.startswith('weather_'):
                    features[col] = 1 if col == f"weather_{last_data['weather_main'].values[0]}" else 0
            
            # 转换为DataFrame
            features_df = pd.DataFrame([features])
            
            # 确保特征顺序与训练时一致
            features_df = features_df[self.feature_columns]
            
            # 预测温度
            predicted_temp = self.model.predict(features_df)[0]
            
            # 基于预测温度确定天气类型
            if predicted_temp < 0:
                weather = 'Snow'
            elif predicted_temp < 10:
                weather = 'Cold'
            elif predicted_temp > 30:
                weather = 'Hot'
            elif np.random.random() < 0.3:
                weather = 'Rain'
            elif np.random.random() < 0.5:
                weather = 'Clouds'
            else:
                weather = 'Clear'
            
            # 创建预测记录
            prediction = {
                'date': pred_date.strftime('%Y-%m-%d'),
                'predicted_temperature': round(predicted_temp, 1),
                'predicted_weather': weather,
                'day_of_week': pred_date.strftime('%A')
            }
            
            predictions.append(prediction)
            
            # 更新最后的数据用于下一次预测
            last_data['temperature'] = predicted_temp
            last_data['weather_main'] = weather
        
        predictions_df = pd.DataFrame(predictions)
        return predictions_df
    
    def save_model(self, filename='weather_model.pkl'):
        """保存训练好的模型"""
        if self.model is None:
            raise ValueError("没有训练好的模型可以保存")
        
        with open(filename, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_columns': self.feature_columns,
                'city': self.city
            }, f)
        
        print(f"模型已保存到 {filename}")
    
    def load_model(self, filename='weather_model.pkl'):
        """加载已保存的模型"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"模型文件 {filename} 不存在")
        
        with open(filename, 'rb') as f:
            saved_data = pickle.load(f)
        
        self.model = saved_data['model']
        self.feature_columns = saved_data['feature_columns']
        self.city = saved_data.get('city', self.city)
        
        print(f"模型已从 {filename} 加载")
    
    def visualize_predictions(self, predictions_df, historical_days=14):
        """可视化预测结果"""
        if self.data is None:
            raise ValueError("没有历史数据可以可视化")
        
        # 准备历史数据
        historical = self.data.copy()
        historical['date'] = pd.to_datetime(historical['date'])
        historical = historical.sort_values('date')
        
        # 只取最近的历史数据
        recent_historical = historical.iloc[-historical_days:]
        
        # 准备预测数据
        predictions = predictions_df.copy()
        predictions['date'] = pd.to_datetime(predictions['date'])
        
        # 创建图表
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # 图表1: 温度对比
        ax1 = axes[0]
        ax1.plot(recent_historical['date'], recent_historical['temperature'], 
                'b-o', label='Historical Temperature', linewidth=2)
        ax1.plot(predictions['date'], predictions['predicted_temperature'], 
                'r--o', label='Predicted Temperature', linewidth=2)
        ax1.set_title(f'Temperature Forecast for {self.city}', fontsize=16)
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Temperature (°C)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 添加温度值标签
        for i, row in predictions.iterrows():
            ax1.annotate(f"{row['predicted_temperature']}°C", 
                        (row['date'], row['predicted_temperature']),
                        textcoords="offset points", xytext=(0,10), ha='center')
        
        # 图表2: 天气类型
        ax2 = axes[1]
        
        # 为天气类型创建颜色映射
        weather_colors = {
            'Clear': 'yellow',
            'Clouds': 'gray',
            'Rain': 'blue',
            'Snow': 'lightblue',
            'Hot': 'red',
            'Cold': 'lightblue'
        }
        
        # 创建条形图
        bars = ax2.bar(predictions['date'].dt.strftime('%m-%d'), 
                      [1] * len(predictions), 
                      color=[weather_colors.get(w, 'gray') for w in predictions['predicted_weather']])
        
        ax2.set_title('Predicted Weather Conditions', fontsize=16)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Weather', fontsize=12)
        
        # 移除y轴刻度
        ax2.set_yticks([])
        
        # 添加天气类型标签
        for bar, weather, day in zip(bars, predictions['predicted_weather'], predictions['day_of_week']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height/2,
                    f"{weather}\n{day[:3]}", ha='center', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()


def main():
    """主函数：演示天气预测系统的使用"""
    print("=" * 50)
    print("天气预测系统")
    print("=" * 50)
    
    # 初始化预测器
    # 注意：要使用真实数据，请在此处添加您的OpenWeatherMap API密钥
    # api_key = "your_openweathermap_api_key_here"
    api_key = None  # 使用None将生成模拟数据
    
    predictor = WeatherPredictor(api_key=api_key, city="Beijing")
    
    # 获取历史数据
    historical_data = predictor.fetch_historical_data(days=60)
    
    # 显示数据前几行
    print("\n历史数据示例:")
    print(historical_data.head())
    
    # 预处理数据
    X, y = predictor.preprocess_data(historical_data)
    
    # 训练模型
    print("\n" + "=" * 50)
    print("模型训练")
    print("=" * 50)
    metrics = predictor.train_model(X, y)
    
    # 预测未来7天
    print("\n" + "=" * 50)
    print("未来7天天气预测")
    print("=" * 50)
    predictions = predictor.predict_next_days(days=7)
    
    # 显示预测结果
    print("\n预测结果:")
    print(predictions.to_string(index=False))
    
    # 可视化预测结果
    print("\n生成可视化图表...")
    predictor.visualize_predictions(predictions)
    
    # 保存模型
    predictor.save_model('weather_predictor_model.pkl')
    
    print("\n" + "=" * 50)
    print("预测完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
```

## 安装依赖

要运行此工程，您需要