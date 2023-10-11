import pandas as pd
import numpy as np
from numpy import ndarray

# 从xls文件中读取数据
weather_data = pd.read_excel('shenzhen_weathers.xls',sheet_name='Sheet1')
# 显示前几行数据
# print(weather_data.head())

# 处理异常值
weather_data['max_temperature'] = weather_data['max'].apply(lambda x: x if x < 50 else None)
weather_data['min_temperature'] = weather_data['min'].apply(lambda x: x if x < 50 else None)

# 删除包含空值的行
weather_data.dropna(inplace=True)

# 日期列处理
weather_data['date'] = pd.to_datetime(weather_data['date'], format='%Y%m%d')
# print(type(weather_data['date']))

# 运用numpy库求数组平均值
def numpy_reduce(s):
    temp = np.array([])
    s = s.fillna(0)
    # 遍历 Series 对象中的每一个元素，如果元素的类型是数值类型，则将其添加到 num_array 中
    for element in s:
        if element == 0:
            continue
        temp = np.append(temp, element)
    return np.mean(temp)

max_mean=numpy_reduce(weather_data['max_temperature'])
min_mean=np.mean(weather_data['min_temperature'])
