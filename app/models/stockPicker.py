# app/models/stock.py

from app import db

class StockPicker(db.Model):
    __tablename__ = 'StockPicker'
    stockId=db.Column(db.Integer, primary_key=True,autoincrement=True)
    stockName=db.Column(db.String(200))
    stockNum=db.Column(db.String(200))
    highestDate=db.Column(db.Date)
    lowestDate=db.Column(db.Date)
    subLowestDateB = db.Column(db.Date)
    subLowestDateC = db.Column(db.Date)
    countSubLow = db.Column(db.Integer)
