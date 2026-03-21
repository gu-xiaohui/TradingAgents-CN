"""
财经新闻入库服务
将从各数据源获取的新闻存入数据库
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_mongo_db
from app.services.news_providers.finance_news_provider import get_news_aggregator, FinanceNewsAggregator

logger = logging.getLogger(__name__)


class FinanceNewsIngestionService:
    """财经新闻入库服务"""
    
    def __init__(self, db=None):
        self.db = db
        self.aggregator: Optional[FinanceNewsAggregator] = None
    
    async def _get_db(self):
        if self.db is None:
            # 直接创建 MongoDB 连接
            from motor.motor_asyncio import AsyncIOMotorClient
            client = AsyncIOMotorClient("mongodb://localhost:27017/")
            self.db = client["tradingagents"]
        return self.db
    
    async def _get_aggregator(self) -> FinanceNewsAggregator:
        if self.aggregator is None:
            self.aggregator = await get_news_aggregator()
        return self.aggregator
    
    async def ensure_indexes(self):
        """确保索引存在"""
        db = await self._get_db()
        collection = db["finance_news"]
        
        # 创建索引
        await collection.create_index("url", unique=True, sparse=True)
        await collection.create_index("publish_time", expireAfterSeconds=7*24*3600)  # 7天过期
        await collection.create_index([("source", 1), ("publish_time", -1)])
        await collection.create_index("symbols")
        await collection.create_index([("title", "text"), ("summary", "text")])
        
        logger.info("📰 财经新闻索引已创建")
    
    async def fetch_and_save_news(self, limit_per_source: int = 30) -> Dict[str, Any]:
        """获取并保存新闻"""
        try:
            aggregator = await self._get_aggregator()
            db = await self._get_db()
            collection = db["finance_news"]
            
            # 获取新闻
            news_list = await aggregator.fetch_all_news(limit_per_source)
            
            # 入库
            saved_count = 0
            updated_count = 0
            duplicate_count = 0
            
            for news in news_list:
                try:
                    # 检查是否已存在
                    existing = await collection.find_one({"url": news.get("url")})
                    
                    if existing:
                        # 更新
                        await collection.update_one(
                            {"url": news.get("url")},
                            {"$set": {
                                "title": news.get("title"),
                                "summary": news.get("summary"),
                                "symbols": news.get("symbols", []),
                                "updated_at": datetime.utcnow()
                            }}
                        )
                        updated_count += 1
                    else:
                        # 插入新记录
                        news["created_at"] = datetime.utcnow()
                        news["updated_at"] = datetime.utcnow()
                        await collection.insert_one(news)
                        saved_count += 1
                        
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        duplicate_count += 1
                    else:
                        logger.warning(f"保存新闻失败: {e}")
            
            result = {
                "fetched": len(news_list),
                "saved": saved_count,
                "updated": updated_count,
                "duplicates": duplicate_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"📰 新闻入库完成: 获取 {len(news_list)} 条, 新增 {saved_count} 条, 更新 {updated_count} 条")
            return result
            
        except Exception as e:
            logger.error(f"❌ 新闻入库失败: {e}")
            raise
    
    async def fetch_and_save_stock_news(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """获取并保存股票相关新闻"""
        try:
            aggregator = await self._get_aggregator()
            db = await self._get_db()
            collection = db["finance_news"]
            
            # 获取新闻
            news_list = await aggregator.fetch_stock_news(symbol, limit)
            
            # 入库
            saved_count = 0
            for news in news_list:
                try:
                    news["symbols"] = list(set(news.get("symbols", []) + [symbol]))
                    news["created_at"] = datetime.utcnow()
                    news["updated_at"] = datetime.utcnow()
                    await collection.update_one(
                        {"url": news.get("url")},
                        {"$set": news},
                        upsert=True
                    )
                    saved_count += 1
                except Exception as e:
                    logger.warning(f"保存股票新闻失败: {e}")
            
            return {
                "symbol": symbol,
                "fetched": len(news_list),
                "saved": saved_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 股票新闻入库失败: {e}")
            raise
    
    async def query_news(
        self,
        symbol: Optional[str] = None,
        source: Optional[str] = None,
        hours_back: int = 24,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """查询新闻"""
        try:
            db = await self._get_db()
            collection = db["finance_news"]
            
            # 构建查询条件
            query = {}
            
            if symbol:
                query["symbols"] = symbol
            
            if source:
                query["source"] = source
            
            if hours_back:
                cutoff = datetime.utcnow() - timedelta(hours=hours_back)
                query["publish_time"] = {"$gte": cutoff}
            
            # 查询
            cursor = collection.find(query).sort("publish_time", -1).skip(skip).limit(limit)
            news_list = await cursor.to_list(length=limit)
            
            # 转换 ObjectId
            for news in news_list:
                news["_id"] = str(news.get("_id", ""))
            
            return news_list
            
        except Exception as e:
            logger.error(f"❌ 查询新闻失败: {e}")
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            db = await self._get_db()
            collection = db["finance_news"]
            
            total = await collection.count_documents({})
            
            # 各数据源统计
            source_stats = {}
            for source in ["eastmoney", "sina", "tencent"]:
                count = await collection.count_documents({"source": source})
                source_stats[source] = count
            
            # 最近更新
            latest = await collection.find_one(sort=[("publish_time", -1)])
            latest_time = latest.get("publish_time") if latest else None
            
            return {
                "total": total,
                "by_source": source_stats,
                "latest_news_time": latest_time.isoformat() if latest_time else None
            }
            
        except Exception as e:
            logger.error(f"❌ 获取统计信息失败: {e}")
            return {}


# 单例
_service: Optional[FinanceNewsIngestionService] = None


async def get_finance_news_service() -> FinanceNewsIngestionService:
    """获取服务实例"""
    global _service
    if _service is None:
        _service = FinanceNewsIngestionService()
    return _service
