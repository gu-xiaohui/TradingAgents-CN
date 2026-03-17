"""
股票排行榜 API
"""
from fastapi import APIRouter, Query
from typing import Optional
from pymongo import MongoClient
from datetime import datetime

router = APIRouter(prefix="/api/screening", tags=["股票筛选"])

# MongoDB 连接
client = MongoClient('mongodb://localhost:27017/')
db = client['tradingagents']


@router.get("/rankings")
async def get_rankings(
    type: str = Query("gainers", description="类型: gainers(涨幅榜), losers(跌幅榜), volume(成交额榜)"),
    limit: int = Query(50, description="返回数量")
):
    """获取股票排行榜"""
    try:
        # 获取最新日期
        latest = db['market_quotes'].find_one(sort=[('trade_date', -1)])
        if not latest:
            return {
                "success": False,
                "message": "没有行情数据，请先同步数据"
            }
        
        latest_date = latest.get('trade_date')
        
        # 排序方式
        if type == "gainers":
            sort_field = "pct_chg"
            sort_order = -1
        elif type == "losers":
            sort_field = "pct_chg"
            sort_order = 1
        elif type == "volume":
            sort_field = "amount"
            sort_order = -1
        else:
            sort_field = "pct_chg"
            sort_order = -1
        
        # 查询数据
        stocks = list(db['market_quotes'].find(
            {'trade_date': latest_date},
            {'_id': 0}
        ).sort(sort_field, sort_order).limit(limit))
        
        # 获取股票名称
        stock_codes = [s.get('code') or s.get('symbol') for s in stocks]
        stock_info = {}
        for info in db['stock_basic_info'].find({'code': {'$in': stock_codes}}, {'_id': 0, 'code': 1, 'name': 1}):
            stock_info[info.get('code')] = info.get('name', '')
        
        # 组装结果
        result_list = []
        for stock in stocks:
            code = stock.get('code') or stock.get('symbol', '')
            result_list.append({
                'code': code,
                'name': stock_info.get(code, ''),
                'close': float(stock.get('close', 0) or 0),
                'pct_chg': float(stock.get('pct_chg', 0) or 0),
                'amount': float(stock.get('amount', 0) or 0),
            })
        
        # 统计数据
        total = db['market_quotes'].count_documents({'trade_date': latest_date})
        up_count = db['market_quotes'].count_documents({'trade_date': latest_date, 'pct_chg': {'$gt': 0}})
        down_count = db['market_quotes'].count_documents({'trade_date': latest_date, 'pct_chg': {'$lt': 0}})
        flat_count = db['market_quotes'].count_documents({'trade_date': latest_date, 'pct_chg': 0})
        
        # 格式化日期
        date_str = latest_date
        if isinstance(latest_date, str) and len(latest_date) == 8:
            date_str = f"{latest_date[:4]}-{latest_date[4:6]}-{latest_date[6:8]}"
        
        return {
            "success": True,
            "data": {
                "list": result_list,
                "date": date_str,
                "stats": {
                    "total": total,
                    "upCount": up_count,
                    "downCount": down_count,
                    "flatCount": flat_count
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"获取数据失败: {str(e)}"
        }
