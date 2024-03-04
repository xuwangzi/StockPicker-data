from app.models.stockDayInfo import createStockDayInfoTable


def slope(Adate, Bdate, Cdate, stockNum) -> bool:
    # 使用动态创建的模型类
    StockDayInfo = createStockDayInfoTable('stockdayinfo_' + stockNum)

    ADayInfo = StockDayInfo.query.filter(StockDayInfo.date == Adate).first()
    BDayInfo = StockDayInfo.query.filter(StockDayInfo.date == Bdate).first()
    CDayInfo = StockDayInfo.query.filter(StockDayInfo.date == Cdate).first()
    ABx = StockDayInfo.query.filter(StockDayInfo.date > Adate, StockDayInfo.date <= Bdate).all().count()
    BCx = StockDayInfo.query.filter(StockDayInfo.date > Bdate, StockDayInfo.date <= Cdate).all().count()
    # AB线段的斜率小于BC线段的斜率为佳
    return (BDayInfo.close - ADayInfo.close) / ABx < (CDayInfo.close - BDayInfo.close) / BCx




