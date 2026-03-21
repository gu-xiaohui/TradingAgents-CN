"""
财经新闻 API 路由
提供新闻获取、查询、同步等接口
"""

from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.routers.auth_db import get_current_user
from app.core.response import ok
from app.services.finance_news_service import get_finance_news_service, FinanceNewsIngestionService

router = APIRouter(prefix="/api/finance-news", tags=["财经新闻"])
import logging
logger = logging.getLogger(__name__)


class NewsSyncRequest(BaseModel):
    """新闻同步请求"""
    limit_per_source: int = Field(default=30, description="每个数据源获取数量")
    symbol: Optional[str] = Field(None, description="股票代码，为空则获取市场新闻")


@router.get("/fetch", response_model=dict)
async def fetch_news(
    limit_per_source: int = Query(30, description="每个数据源获取数量"),
    current_user: dict = Depends(get_current_user)
):
    """
    立即获取最新财经新闻并入库
    
    从东方财富、新浪财经、腾讯财经等数据源获取新闻
    """
    try:
        service = await get_finance_news_service()
        result = await service.fetch_and_save_news(limit_per_source)
        return ok(data=result, message=f"获取并保存 {result.get('saved', 0)} 条新闻")
    except Exception as e:
        logger.error(f"获取新闻失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取新闻失败: {str(e)}")


@router.get("/fetch/{symbol}", response_model=dict)
async def fetch_stock_news(
    symbol: str,
    limit: int = Query(20, description="获取数量"),
    current_user: dict = Depends(get_current_user)
):
    """
    获取指定股票的相关新闻
    
    Args:
        symbol: 股票代码
        limit: 获取数量
    """
    try:
        service = await get_finance_news_service()
        result = await service.fetch_and_save_stock_news(symbol, limit)
        return ok(data=result, message=f"获取股票 {symbol} 新闻 {result.get('saved', 0)} 条")
    except Exception as e:
        logger.error(f"获取股票新闻失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取股票新闻失败: {str(e)}")


@router.get("/query", response_model=dict)
async def query_news(
    symbol: Optional[str] = Query(None, description="股票代码"),
    source: Optional[str] = Query(None, description="数据源 (eastmoney/sina/tencent)"),
    hours_back: int = Query(24, description="回溯小时数"),
    limit: int = Query(50, description="返回数量"),
    skip: int = Query(0, description="跳过数量"),
    current_user: dict = Depends(get_current_user)
):
    """
    查询已入库的财经新闻
    
    支持按股票代码、数据源、时间范围筛选
    """
    try:
        service = await get_finance_news_service()
        news_list = await service.query_news(
            symbol=symbol,
            source=source,
            hours_back=hours_back,
            limit=limit,
            skip=skip
        )
        return ok(data=news_list, message=f"查询到 {len(news_list)} 条新闻")
    except Exception as e:
        logger.error(f"查询新闻失败: {e}")
        raise HTTPException(status_code=500, detail=f"查询新闻失败: {str(e)}")


@router.get("/stats", response_model=dict)
async def get_news_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    获取新闻数据统计
    
    返回总数、各数据源数量、最新更新时间等
    """
    try:
        service = await get_finance_news_service()
        stats = await service.get_stats()
        return ok(data=stats, message="获取统计信息成功")
    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")


@router.post("/sync", response_model=dict)
async def sync_news(
    request: NewsSyncRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    后台同步新闻数据
    
    将在后台执行新闻获取和入库，适合定时任务调用
    """
    try:
        service = await get_finance_news_service()
        
        async def sync_task():
            if request.symbol:
                await service.fetch_and_save_stock_news(request.symbol, 20)
            else:
                await service.fetch_and_save_news(request.limit_per_source)
        
        background_tasks.add_task(sync_task)
        
        return ok(message="新闻同步任务已启动")
    except Exception as e:
        logger.error(f"启动同步失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动同步失败: {str(e)}")
