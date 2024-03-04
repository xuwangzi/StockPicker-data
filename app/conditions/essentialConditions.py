from decimal import Decimal

from app import db
from app.models.stockDayInfo import createStockDayInfoTable
from datetime import datetime, timedelta

import pandas as pd
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt

def smoothK(data: pd.Series, window_length, polyorder, dot):
    # savgol_filter 滤波器
    smooth_data = savgol_filter(data.values, window_length, polyorder) # todo 滤波效果不佳
    index = data.index
    # 返回panda.Series
    smooth_K = pd.Series(smooth_data, index=index)

    return smooth_K


def get_essential_conditions(stockNum):
    # 获取当前日期
    current_date = datetime.now()
    # 计算三年前的日期
    three_years_ago = current_date - timedelta(days=3 * 365)

    # 使用动态创建的模型类
    StockDayInfo = createStockDayInfoTable('stockdayinfo_'+stockNum)
    # 执行查询
    days = (db.session.query(StockDayInfo)
        .filter(StockDayInfo.date >= three_years_ago)
        .order_by(StockDayInfo.date).all()
        )
    # 数据不足
    if days is None or len(days) < 90: return []

    # 构造 panda.Series
    closes = [] # 收盘价
    dates = []
    for day in days:
        closes.append(day.close)
        dates.append(day.date)
    days_series = pd.Series(closes, index=dates)
    # 数据平滑除噪 savgol_filter
    days_series = smoothK(data=days_series, window_length=23, polyorder=3, dot=True)

    # 条件一：找到近三年的 高峰 和 最低点A
    high_day = 0
    low_day = 0
    # 找到近三年的最高点
    for i in range(len(days_series)):
        if days_series[i] > days_series[high_day]:
            high_day = i
    # 找到近三年的最低点
    for i in range(len(days_series)):
        if days_series[i] < days_series[low_day]:
            low_day = i
    # 跌幅
    decline = 0.5
    if days_series[high_day] * decline > days_series[low_day]:
        # # test
        # print(stockNum, "的最高点的日期：", days_series.keys()[high_day].strftime("%Y-%m-%d"))
        # print(stockNum, "的最低点（A）的日期：", days_series.keys()[low_day].strftime("%Y-%m-%d"))

        # 条件二：次低点
        sub_low_days = []
        count_sublow = 0
        # 极小值
        for i in range(low_day + 1, len(days_series) - 2):
            if days_series[i] < days_series[i-1] and days_series[i] < days_series[i+1]:
                sub_low_days.append(i)
                count_sublow += 1
        if count_sublow == 0:
            return []
        # 次低点逐步抬高
        last_day = sub_low_days[0]
        for day in sub_low_days:
            if days_series[day] < days_series[last_day]:
                sub_low_days.remove(day)
                count_sublow -= 1
            else:
                last_day = day
        # # test
        # for day in sub_low_days:
        #     print(stockNum, "的次低点的日期：", days_series.keys()[day].strftime("%Y-%m-%d"),
        #           " | ", days_series[day-1], " | ", days_series[day], " | ", days_series[day+1])
        # 次低点数量<2
        if count_sublow < 2:
            return []

        # 条件三：A点到C点的盘整时间不少于60个交易日
        if days_series.keys()[sub_low_days[count_sublow - 1]] - days_series.keys()[low_day] <= timedelta(days=90):
            return []

        # series to date
        high_date = days_series.keys()[high_day]
        low_date = days_series.keys()[low_day]
        sub_low_b_date = days_series.keys()[sub_low_days[0]]
        sub_low_c_date = days_series.keys()[sub_low_days[count_sublow - 1]]

        # 画图
        days_series.plot(style='k.')
        plt.show()

        return [high_date,low_date,sub_low_b_date,sub_low_c_date,count_sublow]

    return []


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    essential_conditions = get_essential_conditions('600189.SH')
    print(essential_conditions)
