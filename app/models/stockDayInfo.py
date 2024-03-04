# app/models/stock.py

from app import db


def createStockDayInfoTable(tableName):

    class StockDayInfo(db.Model):

        __tablename__ = tableName
        __table_args__ = {'extend_existing': True}
        # 如果数据库中已经存在一个与模型类对应的表，SQLAlchemy 不会尝试重新创建这个表，而是扩展这个已存在的表。
        # 也就是说，它只会添加新的列，而不会删除或修改现有的列。
        dayInfoId = db.Column(db.BigInteger, primary_key=True, nullable=True)
        date = db.Column(db.Date, nullable=True)
        stockId = db.Column(db.BigInteger, nullable=True)
        stockCode = db.Column(db.String(50), nullable=True)
        open = db.Column(db.Float(10, 3), nullable=True)
        high = db.Column(db.Float(10, 3), nullable=True)
        low = db.Column(db.Float(10, 3), nullable=True)
        close = db.Column(db.Float(10, 3), nullable=True)
        preClose = db.Column(db.Float(10, 3), nullable=True)
        volume = db.Column(db.Float(15, 0), nullable=True)
        amount = db.Column(db.Float(15, 5), nullable=True)
        ma5 = db.Column(db.Float(15, 5), nullable=True)
        ma10 = db.Column(db.Float(15, 5), nullable=True)
        ma20 = db.Column(db.Float(15, 5), nullable=True)
        ma30 = db.Column(db.Float(15, 5), nullable=True)
        ma60 = db.Column(db.Float(15, 5), nullable=True)
        ma120 = db.Column(db.Float(15, 5), nullable=True)
        ma200 = db.Column(db.Float(15, 5), nullable=True)
        ma250 = db.Column(db.Float(15, 5), nullable=True)
        volume120 = db.Column(db.Float(15, 0), nullable=True)
        k = db.Column(db.Float(15, 5), nullable=True)
        d = db.Column(db.Float(15, 5), nullable=True)
        j = db.Column(db.Float(15, 5), nullable=True)
        dif = db.Column(db.Float(15, 5), nullable=True)
        dea = db.Column(db.Float(15, 5), nullable=True)
        macd = db.Column(db.Float(15, 5), nullable=True)
        rsi6 = db.Column(db.Float(15, 5), nullable=True)
        rsi12 = db.Column(db.Float(15, 5), nullable=True)
        rsi24 = db.Column(db.Float(15, 5), nullable=True)
        wr6 = db.Column(db.Float(15, 5), nullable=True)
        wr10 = db.Column(db.Float(15, 5), nullable=True)

        change = db.Column(db.Float(15, 5), nullable=True)

    return StockDayInfo
