# app/models/stock.py

from app import db

class Stock(db.Model):
    stockId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=True)
    amplitude = db.Column(db.Float, nullable=True)
    close = db.Column(db.Float, nullable=True)
    flowMarketValue = db.Column(db.Float, nullable=True)
    high = db.Column(db.Float, nullable=True)
    listingDate = db.Column(db.String(255), nullable=True)
    low = db.Column(db.Float, nullable=True)
    open = db.Column(db.Float, nullable=True)
    preClose = db.Column(db.Float, nullable=True)
    stockName = db.Column(db.String(255), nullable=True)
    stockNum = db.Column(db.String(255), nullable=True)
    totalFlowShares = db.Column(db.Float, nullable=True)
    totalMarketValue = db.Column(db.Float, nullable=True)
    totalShares = db.Column(db.Float, nullable=True)
    turnOverrate = db.Column(db.Float, nullable=True)
    upDownPrices = db.Column(db.Float, nullable=True)
    upDownRange = db.Column(db.Float, nullable=True)
    upDownRange3 = db.Column(db.Float, nullable=True)
    upDownRange5 = db.Column(db.Float, nullable=True)
    updateDate = db.Column(db.String(255), nullable=True)
    volume = db.Column(db.Float, nullable=True)
    def __repr__(self):
        return f'<Stock {self.symbol}>'

