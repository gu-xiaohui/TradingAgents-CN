"""
财经新闻数据采集服务
支持从多个主流财经媒体获取新闻数据
"""

import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


class NewsProvider(ABC):
    """新闻数据源基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    @abstractmethod
    async def fetch_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取新闻列表"""
        pass
    
    @abstractmethod
    async def fetch_stock_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取股票相关新闻"""
        pass
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text


class EastMoneyProvider(NewsProvider):
    """东方财富新闻数据源"""
    
    BASE_URL = "https://www.eastmoney.com"
    NEWS_URL = "https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html"
    STOCK_NEWS_URL = "https://searchapi.eastmoney.com/bussiness/web/QuotationLabelSearch"
    
    def __init__(self):
        super().__init__("eastmoney")
    
    async def fetch_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取财经快讯"""
        try:
            session = await self._get_session()
            
            # 使用东方财富财经新闻 API
            url = f"https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_{limit}_1_.html"
            
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"东方财富请求失败: {response.status}")
                    return []
                
                text = await response.text()
                
            # 解析 JSONP 响应
            import json
            match = re.search(r'ajaxResult\((.*)\)', text)
            if match:
                data = json.loads(match.group(1))
            else:
                # 尝试直接解析 JSON
                try:
                    data = json.loads(text)
                except:
                    logger.error("东方财富响应解析失败")
                    return []
            
            news_list = []
            items = data.get("data", []) if isinstance(data.get("data"), list) else []
            
            for item in items[:limit]:
                if not item:
                    continue
                news = {
                    "title": item.get("title", ""),
                    "summary": item.get("digest", "") or item.get("content", ""),
                    "content": item.get("digest", "") or item.get("content", ""),
                    "url": item.get("url", "") or f"https://finance.eastmoney.com/a/{item.get('code', '')}.html",
                    "source": "eastmoney",
                    "source_name": "东方财富",
                    "publish_time": self._parse_time(item.get("showTime", "") or item.get("pubtime", "")),
                    "category": item.get("type", "财经"),
                    "importance": "high" if "重要" in item.get("title", "") else "normal",
                    "symbols": self._extract_symbols(item.get("title", "") + " " + (item.get("digest", "") or "")),
                    "fetched_at": datetime.utcnow()
                }
                news_list.append(news)
            
            logger.info(f"📰 东方财富获取到 {len(news_list)} 条新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"东方财富新闻获取失败: {e}")
            return []
    
    async def fetch_stock_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取股票相关新闻"""
        try:
            session = await self._get_session()
            
            # 使用东方财富股票新闻 API
            code = symbol
            if symbol.startswith("6"):
                secid = f"1.{symbol}"
            else:
                secid = f"0.{symbol}"
            
            url = f"https://np-anotice-stock.eastmoney.com/api/security/ann?cb=jQuery&sr=-1&page_size={limit}&page_index=1&ann_type=SHA,SZA&client_source=web&f_node=0&s_node=0&secid={secid}"
            
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                
                text = await response.text()
                # 解析 JSONP
                import json
                match = re.search(r'jQuery\((.*)\)', text)
                if match:
                    data = json.loads(match.group(1))
                else:
                    return []
            
            news_list = []
            items = data.get("data", {}).get("list", [])
            
            for item in items[:limit]:
                news = {
                    "title": item.get("title", ""),
                    "summary": item.get("title", ""),
                    "content": "",
                    "url": f"https://data.eastmoney.com/notices/detail/{item.get('art_code', '')}.html",
                    "source": "eastmoney",
                    "source_name": "东方财富",
                    "publish_time": self._parse_time(item.get("notice_date", "")),
                    "category": "个股新闻",
                    "importance": "normal",
                    "symbols": [symbol],
                    "fetched_at": datetime.utcnow()
                }
                news_list.append(news)
            
            return news_list
            
        except Exception as e:
            logger.error(f"获取股票 {symbol} 新闻失败: {e}")
            return []
    
    def _parse_time(self, time_str: str) -> datetime:
        """解析时间字符串"""
        if not time_str:
            return datetime.utcnow()
        
        try:
            # 尝试多种格式
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y%m%d%H%M%S",
                "%Y-%m-%d",
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(time_str, fmt)
                except:
                    continue
        except:
            pass
        
        return datetime.utcnow()
    
    def _extract_symbols(self, text: str) -> List[str]:
        """从文本中提取股票代码"""
        symbols = []
        # 匹配 6 位数字股票代码
        matches = re.findall(r'\b(6\d{5}|0\d{5}|3\d{5}|688\d{3})\b', text)
        symbols.extend(matches)
        return list(set(symbols))


class SinaFinanceProvider(NewsProvider):
    """新浪财经新闻数据源"""
    
    BASE_URL = "https://finance.sina.com.cn"
    NEWS_URL = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page=1"
    
    def __init__(self):
        super().__init__("sina")
    
    async def fetch_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取财经新闻"""
        try:
            session = await self._get_session()
            
            url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num={limit}&page=1&r={datetime.now().timestamp()}"
            
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
            
            news_list = []
            items = data.get("result", {}).get("data", [])
            
            for item in items[:limit]:
                news = {
                    "title": item.get("title", ""),
                    "summary": item.get("intro", ""),
                    "content": item.get("intro", ""),
                    "url": item.get("url", ""),
                    "source": "sina",
                    "source_name": "新浪财经",
                    "publish_time": datetime.fromtimestamp(int(item.get("ctime", 0))),
                    "category": item.get("channel", {}).get("cname", "财经"),
                    "importance": "normal",
                    "symbols": self._extract_symbols(item.get("title", "") + item.get("intro", "")),
                    "fetched_at": datetime.utcnow()
                }
                news_list.append(news)
            
            logger.info(f"📰 新浪财经获取到 {len(news_list)} 条新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"新浪财经新闻获取失败: {e}")
            return []
    
    async def fetch_stock_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取股票相关新闻"""
        # 新浪的股票新闻 API 较复杂，这里使用通用新闻搜索
        return []
    
    def _extract_symbols(self, text: str) -> List[str]:
        """从文本中提取股票代码"""
        symbols = []
        matches = re.findall(r'\b(6\d{5}|0\d{5}|3\d{5}|688\d{3})\b', text)
        symbols.extend(matches)
        return list(set(symbols))


class TencentFinanceProvider(NewsProvider):
    """腾讯财经新闻数据源"""
    
    BASE_URL = "https://finance.qq.com"
    
    def __init__(self):
        super().__init__("tencent")
    
    async def fetch_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取财经新闻"""
        try:
            session = await self._get_session()
            
            url = f"https://i.match.qq.com/ninja/NewsInter/read?num={limit}&chlid=news_news_financial"
            
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
            
            news_list = []
            items = data.get("data", [])
            
            for item in items[:limit]:
                news = {
                    "title": item.get("title", ""),
                    "summary": item.get("intro", ""),
                    "content": item.get("intro", ""),
                    "url": item.get("url", ""),
                    "source": "tencent",
                    "source_name": "腾讯财经",
                    "publish_time": datetime.fromtimestamp(int(item.get("timestamp", 0))),
                    "category": "财经",
                    "importance": "normal",
                    "symbols": self._extract_symbols(item.get("title", "") + item.get("intro", "")),
                    "fetched_at": datetime.utcnow()
                }
                news_list.append(news)
            
            logger.info(f"📰 腾讯财经获取到 {len(news_list)} 条新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"腾讯财经新闻获取失败: {e}")
            return []
    
    async def fetch_stock_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        return []
    
    def _extract_symbols(self, text: str) -> List[str]:
        symbols = []
        matches = re.findall(r'\b(6\d{5}|0\d{5}|3\d{5}|688\d{3})\b', text)
        symbols.extend(matches)
        return list(set(symbols))


class FinanceNewsAggregator:
    """财经新闻聚合器"""
    
    def __init__(self):
        self.providers: Dict[str, NewsProvider] = {
            "eastmoney": EastMoneyProvider(),
            "sina": SinaFinanceProvider(),
            "tencent": TencentFinanceProvider(),
        }
    
    async def fetch_all_news(self, limit_per_source: int = 20) -> List[Dict[str, Any]]:
        """从所有数据源获取新闻"""
        all_news = []
        
        tasks = [
            provider.fetch_news(limit_per_source)
            for provider in self.providers.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"新闻获取异常: {result}")
        
        # 按时间排序，去重
        seen_titles = set()
        unique_news = []
        for news in sorted(all_news, key=lambda x: x.get("publish_time", datetime.min), reverse=True):
            title = news.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news
    
    async def fetch_stock_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取股票相关新闻"""
        all_news = []
        
        tasks = [
            provider.fetch_stock_news(symbol, limit)
            for provider in self.providers.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
        
        # 去重排序
        seen_titles = set()
        unique_news = []
        for news in sorted(all_news, key=lambda x: x.get("publish_time", datetime.min), reverse=True):
            title = news.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news[:limit]
    
    async def close(self):
        """关闭所有连接"""
        for provider in self.providers.values():
            await provider.close()


# 单例实例
_aggregator: Optional[FinanceNewsAggregator] = None


async def get_news_aggregator() -> FinanceNewsAggregator:
    """获取新闻聚合器实例"""
    global _aggregator
    if _aggregator is None:
        _aggregator = FinanceNewsAggregator()
    return _aggregator
