from shenzhen_weather_data_pre import weather_data,max_mean,min_mean
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np

# 最高气温数据可视化：折线图
plt.plot(weather_data['date'].dt.strftime("%d"), weather_data['max_temperature'],label="当日预测最高温")
plt.plot(weather_data['date'].dt.strftime("%d"), weather_data['hmax'],label="当日历史最高温")
plt.axhline(y=max_mean,linestyle='--',color='r',label="本月预测平均气温")
plt.xlabel('Date')
plt.ylabel('maxTemperature')
plt.title('Max temperature Change over Time')
# 指定中文字体文件
font = FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf')
plt.legend(prop=font)
plt.show()

# 最低气温数据可视化：日历
begin = weather_data['date'].head(1).iloc[0]
end = weather_data['date'].tail(1).iloc[0]
# print(begin)
# print(end)

index=weather_data.index[0]

data = [
    [str(begin + datetime.timedelta(days=i)), weather_data.loc[index+i,'min_temperature']]
    for i in range((end - begin).days + 1)
]
# print(data)

c = (
    Calendar()
    .add(
        "",
        data,
        calendar_opts=opts.CalendarOpts(
            pos_left="20%",
            pos_right='50%',
            range_=[begin,end],
            daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
            monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Calendar-近30天深圳天气最低气温变化"),
        visualmap_opts=opts.VisualMapOpts(
            max_=weather_data['min_temperature'].max(),
            min_=weather_data['min_temperature'].min(),
            orient="horizontal",
            is_piecewise=True,
            pos_top="230px",
            pos_left="100px"
        ),
    )
    .render("min_temperature_calendar.html")
)

# 湿度数据可视化：立体散点图
#数据处理
humidity=[s.replace("%","") for s in weather_data['hgl']]
humidity=np.array(humidity).astype(int)
print(type(humidity[0]))
date = weather_data['date'].dt.strftime("%d")
days = np.arange(1, weather_data.index[-1]+1)
# 创建立体散点图
fig = go.Figure(
    go.Scatter3d(
        x=days,
        y=humidity,
        z=date,
        mode='markers',
        marker=dict(
            size=10,
            color=humidity,
            colorscale='RdYlBu_r',
            opacity=0.8,
            colorbar=dict(title=dict(text='Humidity'))
        ),
        hovertemplate='Day: %{x}<br>Humidity: %{y}%<br>Date: %{z}<extra></extra>',
        showlegend=False
    )
)
# 设置图表布局
fig.update_layout(
    title=dict(text="30-day Humidity"),
    scene=dict(
        xaxis_title=dict(text='Days'),
        yaxis_title=dict(text='Humidity (%)'),
        zaxis_title=dict(text='Date'),
        aspectratio=dict(x=1, y=1, z=1),
        camera_eye=dict(x=-1.25, y=1.25, z=1.25),
    )
)
# 显示图表
fig.show()