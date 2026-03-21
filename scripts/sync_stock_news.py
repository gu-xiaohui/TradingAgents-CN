"""
股票新闻批量同步脚本
为数据库中的每只股票抓取相关新闻并入库
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from pymongo import MongoClient
from app.services.finance_news_service import get_finance_news_service
from app.core.database import get_mongo_db
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def sync_all_stock_news(batch_size: int = 50, delay: float = 0.5):
    """为所有股票同步新闻"""
    
    # 获取数据库连接
    client = MongoClient("mongodb://localhost:27017/")
    db = client["tradingagents"]
    
    # 获取所有股票
    stocks = list(db.stock_basic_info.find({}, {"code": 1, "name": 1}))
    total = len(stocks)
    
    print(f"\n{'='*60}")
    print(f"开始同步股票新闻")
    print(f"总股票数: {total}")
    print(f"批次大小: {batch_size}")
    print(f"{'='*60}\n")
    
    # 获取服务
    service = await get_finance_news_service()
    await service.ensure_indexes()
    
    # 统计
    total_saved = 0
    total_failed = 0
    failed_stocks = []
    
    # 批量处理
    for i, stock in enumerate(stocks):
        code = stock.get("code", "")
        name = stock.get("name", "")
        
        try:
            # 获取并保存新闻
            result = await service.fetch_and_save_stock_news(code, limit=10)
            saved = result.get("saved", 0)
            total_saved += saved
            
            # 进度显示
            progress = (i + 1) / total * 100
            print(f"[{i+1}/{total}] ({progress:.1f}%) {code} {name}: 保存 {saved} 条新闻")
            
            # 延迟，避免请求过快
            if delay > 0:
                await asyncio.sleep(delay)
                
        except Exception as e:
            total_failed += 1
            failed_stocks.append(code)
            logger.error(f"❌ {code} {name} 新闻同步失败: {e}")
    
    # 输出统计
    print(f"\n{'='*60}")
    print(f"同步完成!")
    print(f"  成功: {total - total_failed} 只股票")
    print(f"  失败: {total_failed} 只股票")
    print(f"  总保存新闻: {total_saved} 条")
    if failed_stocks:
        print(f"  失败股票: {failed_stocks[:10]}...")
    print(f"{'='*60}\n")
    
    # 获取最终统计
    stats = await service.get_stats()
    print(f"数据库统计:")
    print(f"  总新闻数: {stats.get('total', 0)}")
    print(f"  各来源: {stats.get('by_source', {})}")
    
    client.close()


async def sync_popular_stocks():
    """只同步热门股票（可自定义列表）"""
    
    popular_stocks = [
        ("600519", "贵州茅台"),
        ("000858", "五粮液"),
        ("601318", "中国平安"),
        ("000001", "平安银行"),
        ("600036", "招商银行"),
        ("601398", "工商银行"),
        ("000333", "美的集团"),
        ("600000", "浦发银行"),
        ("601166", "兴业银行"),
        ("600276", "恒瑞医药"),
        ("002594", "比亚迪"),
        ("300750", "宁德时代"),
        ("000002", "万科A"),
        ("002415", "海康威视"),
        ("600900", "长江电力"),
    ]
    
    print(f"\n同步热门股票新闻: {len(popular_stocks)} 只\n")
    
    service = await get_finance_news_service()
    await service.ensure_indexes()
    
    for code, name in popular_stocks:
        try:
            result = await service.fetch_and_save_stock_news(code, limit=15)
            print(f"✅ {code} {name}: 保存 {result.get('saved', 0)} 条新闻")
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"❌ {code} {name}: {e}")
    
    stats = await service.get_stats()
    print(f"\n总新闻数: {stats.get('total', 0)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="股票新闻同步")
    parser.add_argument("--all", action="store_true", help="同步所有股票")
    parser.add_argument("--popular", action="store_true", help="只同步热门股票")
    parser.add_argument("--batch-size", type=int, default=50, help="批次大小")
    parser.add_argument("--delay", type=float, default=0.3, help="请求延迟(秒)")
    
    args = parser.parse_args()
    
    if args.popular:
        asyncio.run(sync_popular_stocks())
    elif args.all:
        asyncio.run(sync_all_stock_news(args.batch_size, args.delay))
    else:
        # 默认同步热门股票
        asyncio.run(sync_popular_stocks())
