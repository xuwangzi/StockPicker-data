# This is a sample Python script.
import pandas
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tushare as ts
import datetime
from matplotlib import pyplot as plt
import pandas as pd
from app.models.stockDayInfo import createStockDayInfoTable
from scipy.signal import savgol_filter


def drawK(data: pandas.Series, window_length, polyorder, dot):
    smooth_data = savgol_filter(data.values, window_length, polyorder)
    if dot: pd.Series(smooth_data).plot(style='k.')
    else: pd.Series(smooth_data).plot()
    plt.show()


def checkThreeRedLargeVolume(Bdate, stockNum):
    # 使用动态创建的模型类
    StockDayInfo = createStockDayInfoTable('stockdayinfo_'+stockNum)
    # 执行查询
    afterBDayInfo = StockDayInfo.query.filter(StockDayInfo.date >= Bdate).all()
    # 找B之后的三连阳至今
    for i in range(len(afterBDayInfo)-3):
        if afterBDayInfo[i].change>0 and afterBDayInfo[i+1].change>0 and afterBDayInfo[i+2].change>0:
            # 找到三连阳
            # 前后十天找量能放大,max防数组越界
            for j in range(max(i-10, 0), i+12):
                if afterBDayInfo[j].volume > afterBDayInfo[j].ma120 and afterBDayInfo[j].volume > afterBDayInfo[j-1].volume*2 and afterBDayInfo[j].close > afterBDayInfo[j].open:  # TODO 爆出天量
                    # 找到量能放大
                    # 判断从量能放大日开始，至少80%的日交易量都维持在120日交易量均线以上（涨停日不算）
                    countMore120 = 0
                    for k in range(j,len(afterBDayInfo)):
                        if afterBDayInfo[k].volume > afterBDayInfo[k].ma120 and afterBDayInfo[k].pctChange<10: # 涨停日判断
                            countMore120+= 1
                    if countMore120/(len(afterBDayInfo)-j) > 0.8:
                        return True # TODO 三连阳与量能放大返回数据格式
    return False



def threeRed(ts_code, start_date, end_date):

    return ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[120])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 查三连阳和量能放大
    stockNum = "000635.SZ"
    Bdate = datetime.date(2022, 10, 15)
    checkThreeRedLargeVolume(Bdate, stockNum)
    # pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    # dfList = threeRed("000635.SZ").values.tolist()
    # print(dfList)

