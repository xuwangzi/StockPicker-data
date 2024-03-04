from datetime import timedelta

from app.models.stockDayInfo import createStockDayInfoTable


def averageBonding(keyKDay, stockNum) -> bool:
    # 使用动态创建的模型类
    StockDayInfo = createStockDayInfoTable('stockdayinfo_' + stockNum)
    # 找出关键k线日前30天的日k数据
    thirtyDaysInfo = StockDayInfo.query.filter(StockDayInfo.date > keyKDay.date - timedelta(days=30), StockDayInfo.date <= keyKDay.date).all()
    dayCount = 0
    # 遍历这30天，找四条均线差异值小于10%的
    for i in range(len(thirtyDaysInfo)):
        if averagedif(thirtyDaysInfo[i]):
            dayCount += 1
    return dayCount>3

def averagedif(dayInfo):
    if dayInfo.ma5 == 0 or dayInfo.ma10 == 0 or dayInfo.ma20 == 0 or dayInfo.ma30 == 0:
        return False
    if abs(dayInfo.ma5 - dayInfo.ma10)/dayInfo.ma10 < 0.1 and abs(dayInfo.ma5 - dayInfo.ma60)/dayInfo.ma60 < 0.1 and abs(dayInfo.ma5 - dayInfo.ma120)/dayInfo.ma120 < 0.1 and abs(dayInfo.ma10 - dayInfo.ma60)/dayInfo.ma60 < 0.1 and abs(dayInfo.ma10 - dayInfo.ma120)/dayInfo.ma120 < 0.1 and abs(dayInfo.ma60 - dayInfo.ma120)/dayInfo.ma120 < 0.1:
        return True
    else:
        return False