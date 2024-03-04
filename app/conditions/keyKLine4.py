from app.models.stockDayInfo import createStockDayInfoTable


def checkKeyKLine(Bdate, stockNum):
    # 使用动态创建的模型类
    StockDayInfo = createStockDayInfoTable('stockdayinfo_' + stockNum)
    # 执行查询，切片取B前一日至今
    index = 0
    afterBDayInfo = StockDayInfo.query.all()
    for index, dayInfo in afterBDayInfo:
        if dayInfo.date >= Bdate:
            break
    afterBDayInfo = afterBDayInfo[max(0, index - 1):]
    # 找B之后的关键k线至今
    for i in range(1, len(afterBDayInfo)):
        # 日内最高点能达到7%以上涨幅，收盘至少有5%以上涨幅，阳线
        if (afterBDayInfo[i].high-afterBDayInfo[i].preClose)/afterBDayInfo[i].preClose > 0.07 and (afterBDayInfo[i].close-afterBDayInfo[i].preClose)/afterBDayInfo[i].preClose > 0.05 and afterBDayInfo[i].close > afterBDayInfo[i].open:
            # 如果是涨停板或一字板，可以不放量，
            if afterBDayInfo[i].pctChange > 10 or isOneWordBoard(afterBDayInfo[i]):
                return True
            # 否则要放量。放量是指当日交易量超过前一日交易量
            elif afterBDayInfo[i].volume > afterBDayInfo[i-1].volume:
                return True
            else: return False
            # TODO 关键k线返回数据格式

def isOneWordBoard(stockDayInfo):
    if stockDayInfo.open == stockDayInfo.close and stockDayInfo.close == stockDayInfo.high and stockDayInfo.high == stockDayInfo.low:
        return True
    else:
        return False