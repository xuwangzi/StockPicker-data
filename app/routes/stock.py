# app/routes/stock.py
import datetime

from app import app, db
from app.models.stock import Stock
from app.models.stockPicker import StockPicker
import tushare as ts
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from app.conditions.threeRedLargeVolume5 import checkThreeRedLargeVolume
from app.conditions.essentialConditions import get_essential_conditions


@app.route('/stock')  # GET
def get_stocks():
    return 'Hello, World!'


@app.route('/stock/getRealTimeList')
def real_list():  # put application's code here
    ts.set_token('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    df = ts.realtime_list()
    return df.to_json(orient="records", force_ascii=False)


@app.route('/stock/getRealTimeInfo')
def real_info():  # put application's code here
    stock_num = request.values.get("stockNum")  # Query
    ts.set_token('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    df = ts.realtime_tick(ts_code=stock_num, src='dc')

    if df.empty:
        return '[]'
    else:
        return df.to_json(orient="records", force_ascii=False)


@app.route('/stock/getRealTimeQuote')
def real_quote():  # put application's code here
    stock_num = request.values.get("stockNum")
    ts.set_token('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    df = ts.realtime_quote(ts_code=stock_num, src='dc')

    if df.empty:
        return '[]'
    else:
        return df.to_json(orient="records", force_ascii=False)



# 建库（已有的表不会重新构建）
with app.app_context():
    db.create_all()

# 选股算法
def select_stock():
    # # 传回前端参数
    # stockTable = []
    # stockTableDict = {}

    # stock数据库中无论是否有stockpicker表，都删除
    db.session.query(StockPicker).delete()
    db.session.commit()

    # 获取所有 Stock 对象
    stocks = (db.session
              .query(Stock.stockId, Stock.stockNum, Stock.stockName)
              .filter()
              .order_by(Stock.stockNum).all()
              )
    data=[]
    # 筛选股票
    for stock in stocks:
        # 选出K线最高点A
        # 选出K线最低点
        # 选出BC
        essential_conditions = get_essential_conditions(stock.stockNum)



        if len(essential_conditions) != 0:  # 必要条件
            # # 不必要条件
            # non_essential_conditions = get_non_essential_conditions(stock.stockNum)

            data.append(StockPicker(stockId=stock.stockId,stockName=stock.stockName,stockNum=stock.stockNum,
                                    highestDate=essential_conditions[0],
                                    lowestDate=essential_conditions[1],
                                    subLowestDateB = essential_conditions[2],
                                    subLowestDateC = essential_conditions[3],
                                    countSubLow = essential_conditions[4]
                                    ))

    db.session.add_all(data)
    db.session.commit()

    return "成功更新stockpicker"

# 测试接口，实际部署时不使用，服务器自动定时更新
@app.route('/stock/select')
def getindex():
    return select_stock()

# 服务器定时更新
scheduler = BackgroundScheduler() # 定义每天晚上8点30执行的任务

@scheduler.scheduled_job('cron', hour=3, minute=0, second=0)
def getdemo():
    select_stock()

# 定时更新 启动
scheduler.start()
