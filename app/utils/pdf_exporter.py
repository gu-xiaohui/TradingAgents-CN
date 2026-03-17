"""
PDF 导出工具 - 生成专业美观的分析报告 PDF
遵循 UI/UX Pro Max 设计规范
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# SVG 图标 (Heroicons 风格)
ICONS = {
    'chart': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>',
    'currency': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    'trending-up': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" /></svg>',
    'trending-down': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.51l-5.511-3.181" /></svg>',
    'pause': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" /></svg>',
    'warning': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>',
    'document': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>',
    'shield': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>',
    'calendar': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" /></svg>',
    'user': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>',
    'check': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    'arrow-up': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" /></svg>',
    'newspaper': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" /></svg>',
    'light-bulb': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" /></svg>',
    'target': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" /></svg>',
    'scale': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75" /></svg>',
    'bolt': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" /></svg>',
    'building': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" /></svg>',
}

# PDF HTML 模板 - 专业版
PDF_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{stock_name} ({stock_symbol}) 分析报告</title>
    <style>
        :root {{
            --primary: #3B82F6;
            --primary-dark: #1D4ED8;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --gray-50: #F9FAFB;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-300: #D1D5DB;
            --gray-400: #9CA3AF;
            --gray-500: #6B7280;
            --gray-600: #4B5563;
            --gray-700: #374151;
            --gray-800: #1F2937;
            --gray-900: #111827;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            color: var(--gray-800);
            background: #ffffff;
            font-size: 10pt;
        }}
        
        /* 页面设置 */
        @page {{
            size: A4;
            margin: 12mm 15mm;
        }}
        
        /* ========== 封面页 ========== */
        .cover {{
            height: 260mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            margin: -12mm -15mm;
            padding: 25mm;
            position: relative;
            overflow: hidden;
        }}
        
        .cover::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.3;
        }}
        
        .cover-logo {{
            width: 72px;
            height: 72px;
            background: rgba(255,255,255,0.15);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 28px;
            position: relative;
            backdrop-filter: blur(10px);
        }}
        
        .cover-logo svg {{
            width: 40px;
            height: 40px;
            stroke: white;
        }}
        
        .cover-title {{
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: 1px;
            position: relative;
        }}
        
        .cover-subtitle {{
            font-size: 11pt;
            opacity: 0.85;
            margin-bottom: 40px;
            font-weight: 400;
            letter-spacing: 0.5px;
        }}
        
        .cover-stock {{
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 20px 50px;
            border-radius: 12px;
            margin-bottom: 25px;
            position: relative;
            backdrop-filter: blur(10px);
        }}
        
        .cover-stock-name {{
            font-size: 22pt;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        
        .cover-stock-code {{
            font-size: 12pt;
            opacity: 0.8;
            font-family: "SF Mono", "Fira Code", "Consolas", monospace;
            letter-spacing: 1px;
        }}
        
        .cover-recommendation {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            padding: 12px 28px;
            border-radius: 50px;
            font-size: 13pt;
            font-weight: 600;
            position: relative;
        }}
        
        .cover-recommendation svg {{
            width: 20px;
            height: 20px;
        }}
        
        .rec-buy {{ 
            background: rgba(16, 185, 129, 0.25); 
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}
        .rec-sell {{ 
            background: rgba(239, 68, 68, 0.25); 
            border: 1px solid rgba(239, 68, 68, 0.4);
        }}
        .rec-hold {{ 
            background: rgba(245, 158, 11, 0.25); 
            border: 1px solid rgba(245, 158, 11, 0.4);
        }}
        
        .cover-meta {{
            font-size: 9pt;
            opacity: 0.7;
            margin-top: 50px;
            line-height: 1.8;
            position: relative;
        }}
        
        /* ========== 内容区域 ========== */
        .content {{
            padding-top: 8mm;
        }}
        
        /* 头部信息栏 */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--gray-200);
            margin-bottom: 16px;
        }}
        
        .header-left h1 {{
            font-size: 16pt;
            color: var(--gray-900);
            margin-bottom: 4px;
            font-weight: 700;
        }}
        
        .header-left .stock-code {{
            font-size: 10pt;
            color: var(--gray-500);
            font-family: "SF Mono", monospace;
        }}
        
        .header-right {{
            text-align: right;
            font-size: 9pt;
            color: var(--gray-500);
        }}
        
        .header-right .meta-item {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 6px;
            margin-bottom: 3px;
        }}
        
        .header-right .meta-item svg {{
            width: 14px;
            height: 14px;
            stroke: var(--gray-400);
        }}
        
        /* 关键指标卡片 */
        .metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }}
        
        .metric-card {{
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }}
        
        .metric-card .icon {{
            width: 32px;
            height: 32px;
            margin: 0 auto 8px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .metric-card .icon svg {{
            width: 18px;
            height: 18px;
        }}
        
        .metric-card .icon.blue {{ background: #DBEAFE; }}
        .metric-card .icon.blue svg {{ stroke: var(--primary); }}
        .metric-card .icon.green {{ background: #D1FAE5; }}
        .metric-card .icon.green svg {{ stroke: var(--success); }}
        .metric-card .icon.yellow {{ background: #FEF3C7; }}
        .metric-card .icon.yellow svg {{ stroke: var(--warning); }}
        .metric-card .icon.red {{ background: #FEE2E2; }}
        .metric-card .icon.red svg {{ stroke: var(--danger); }}
        
        .metric-card .label {{
            font-size: 8pt;
            color: var(--gray-500);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }}
        
        .metric-card .value {{
            font-size: 14pt;
            font-weight: 700;
            color: var(--gray-900);
        }}
        
        .metric-card .value.buy {{ color: var(--success); }}
        .metric-card .value.sell {{ color: var(--danger); }}
        .metric-card .value.hold {{ color: var(--warning); }}
        
        .metric-card .sub {{
            font-size: 8pt;
            color: var(--gray-500);
            margin-top: 2px;
        }}
        
        /* 风险等级指示器 */
        .risk-indicator {{
            display: flex;
            gap: 4px;
            justify-content: center;
            margin-top: 8px;
        }}
        
        .risk-indicator .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--gray-200);
        }}
        
        .risk-indicator .dot.active.level-1 {{ background: var(--success); }}
        .risk-indicator .dot.active.level-2 {{ background: #84CC16; }}
        .risk-indicator .dot.active.level-3 {{ background: var(--warning); }}
        .risk-indicator .dot.active.level-4 {{ background: #F97316; }}
        .risk-indicator .dot.active.level-5 {{ background: var(--danger); }}
        
        /* 置信度进度条 */
        .confidence-bar {{
            width: 100%;
            height: 6px;
            background: var(--gray-200);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }}
        
        .confidence-bar .fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.3s;
        }}
        
        .confidence-bar .fill.high {{ background: var(--success); }}
        .confidence-bar .fill.medium {{ background: var(--primary); }}
        .confidence-bar .fill.low {{ background: var(--warning); }}
        
        /* 警告提示框 */
        .warning-box {{
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border: 1px solid #FCD34D;
            border-left: 4px solid var(--warning);
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }}
        
        .warning-box .icon {{
            flex-shrink: 0;
            width: 24px;
            height: 24px;
        }}
        
        .warning-box .icon svg {{
            width: 24px;
            height: 24px;
            stroke: var(--warning);
        }}
        
        .warning-box .content {{
            flex: 1;
        }}
        
        .warning-box h4 {{
            color: #92400E;
            font-size: 10pt;
            margin-bottom: 4px;
            font-weight: 600;
        }}
        
        .warning-box ul {{
            color: #78350F;
            font-size: 8pt;
            margin-left: 14px;
        }}
        
        .warning-box li {{
            margin-bottom: 2px;
        }}
        
        /* 摘要区 */
        .summary {{
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border: 1px solid #BFDBFE;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        
        .summary-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .summary-header .icon {{
            width: 28px;
            height: 28px;
            background: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .summary-header .icon svg {{
            width: 16px;
            height: 16px;
            stroke: var(--primary);
        }}
        
        .summary-header h3 {{
            font-size: 11pt;
            color: var(--gray-800);
            font-weight: 600;
        }}
        
        .summary p {{
            font-size: 9pt;
            color: var(--gray-700);
            line-height: 1.7;
        }}
        
        /* 报告模块 */
        .section {{
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--gray-200);
            margin-bottom: 12px;
        }}
        
        .section-icon {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .section-icon svg {{
            width: 16px;
            height: 16px;
        }}
        
        .section-icon.blue {{ background: #DBEAFE; }}
        .section-icon.blue svg {{ stroke: var(--primary); }}
        .section-icon.green {{ background: #D1FAE5; }}
        .section-icon.green svg {{ stroke: var(--success); }}
        .section-icon.purple {{ background: #EDE9FE; }}
        .section-icon.purple svg {{ stroke: #7C3AED; }}
        .section-icon.orange {{ background: #FEF3C7; }}
        .section-icon.orange svg {{ stroke: var(--warning); }}
        .section-icon.red {{ background: #FEE2E2; }}
        .section-icon.red svg {{ stroke: var(--danger); }}
        .section-icon.gray {{ background: var(--gray-100); }}
        .section-icon.gray svg {{ stroke: var(--gray-500); }}
        
        .section-title {{
            font-size: 12pt;
            font-weight: 600;
            color: var(--gray-800);
        }}
        
        .section-content {{
            font-size: 9pt;
            color: var(--gray-600);
            line-height: 1.7;
        }}
        
        .section-content h1 {{
            font-size: 11pt;
            color: var(--gray-800);
            margin: 12px 0 8px;
            font-weight: 600;
        }}
        
        .section-content h2 {{
            font-size: 10pt;
            color: var(--gray-700);
            margin: 10px 0 6px;
            font-weight: 600;
        }}
        
        .section-content h3 {{
            font-size: 9pt;
            color: var(--gray-600);
            margin: 8px 0 4px;
            font-weight: 500;
        }}
        
        .section-content p {{
            margin-bottom: 6px;
        }}
        
        .section-content ul, .section-content ol {{
            margin: 6px 0 6px 18px;
        }}
        
        .section-content li {{
            margin-bottom: 3px;
        }}
        
        .section-content strong {{
            color: var(--gray-800);
            font-weight: 600;
        }}
        
        .section-content code {{
            background: var(--gray-100);
            padding: 2px 5px;
            border-radius: 4px;
            font-family: "SF Mono", monospace;
            font-size: 8pt;
            color: var(--danger);
        }}
        
        .section-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 8pt;
        }}
        
        .section-content th {{
            background: var(--gray-50);
            padding: 6px 8px;
            text-align: left;
            border-bottom: 1px solid var(--gray-300);
            font-weight: 600;
            color: var(--gray-700);
        }}
        
        .section-content td {{
            padding: 6px 8px;
            border-bottom: 1px solid var(--gray-200);
        }}
        
        .section-content tr:nth-child(even) {{
            background: var(--gray-50);
        }}
        
        .section-content blockquote {{
            border-left: 3px solid var(--primary);
            padding-left: 10px;
            margin: 8px 0;
            color: var(--gray-500);
            font-style: italic;
        }}
        
        .section-content hr {{
            border: none;
            border-top: 1px solid var(--gray-200);
            margin: 12px 0;
        }}
        
        /* 数据标签 */
        .data-tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 500;
        }}
        
        .data-tag.success {{ background: #D1FAE5; color: #065F46; }}
        .data-tag.warning {{ background: #FEF3C7; color: #92400E; }}
        .data-tag.danger {{ background: #FEE2E2; color: #991B1B; }}
        .data-tag.info {{ background: #DBEAFE; color: #1E40AF; }}
        
        /* 页脚 */
        .footer {{
            margin-top: 25px;
            padding-top: 12px;
            border-top: 1px solid var(--gray-200);
            text-align: center;
            font-size: 7pt;
            color: var(--gray-400);
        }}
        
        .footer-logo {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            margin-bottom: 4px;
        }}
        
        .footer-logo svg {{
            width: 14px;
            height: 14px;
            stroke: var(--gray-400);
        }}
        
        .footer-logo span {{
            font-weight: 500;
            color: var(--gray-500);
        }}
        
        /* 分页 */
        .page-break {{
            page-break-before: always;
        }}
        
        /* 打印优化 */
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <!-- 封面 -->
    <div class="cover">
        <div class="cover-logo">
            {cover_icon}
        </div>
        <div class="cover-title">投资分析报告</div>
        <div class="cover-subtitle">TradingAgents-CN 智能分析系统</div>
        
        <div class="cover-stock">
            <div class="cover-stock-name">{stock_name}</div>
            <div class="cover-stock-code">{stock_symbol}</div>
        </div>
        
        <div class="cover-recommendation {rec_class}">
            {rec_icon}
            <span>{recommendation_short}</span>
        </div>
        
        <div class="cover-meta">
            分析日期：{analysis_date}<br>
            分析模型：{model_info}<br>
            报告生成时间：{generated_time}
        </div>
    </div>
    
    <!-- 正文内容 -->
    <div class="content">
        <!-- 头部 -->
        <div class="header">
            <div class="header-left">
                <h1>{stock_name} 分析报告</h1>
                <div class="stock-code">{stock_symbol} · {market_type}</div>
            </div>
            <div class="header-right">
                <div class="meta-item">
                    {calendar_icon}
                    <span>{analysis_date}</span>
                </div>
                <div class="meta-item">
                    {user_icon}
                    <span>{analysts}</span>
                </div>
            </div>
        </div>
        
        <!-- 关键指标 -->
        <div class="metrics">
            <div class="metric-card">
                <div class="icon {rec_icon_class}">{rec_card_icon}</div>
                <div class="label">投资建议</div>
                <div class="value {rec_class}">{recommendation_short}</div>
                <div class="sub">{target_price}</div>
            </div>
            <div class="metric-card">
                <div class="icon {risk_icon_class}">{risk_card_icon}</div>
                <div class="label">风险评估</div>
                <div class="value">{risk_level}</div>
                <div class="risk-indicator">{risk_indicator}</div>
            </div>
            <div class="metric-card">
                <div class="icon {confidence_icon_class}">{confidence_card_icon}</div>
                <div class="label">置信度</div>
                <div class="value">{confidence_score}%</div>
                <div class="confidence-bar">
                    <div class="fill {confidence_level}" style="width: {confidence_score}%"></div>
                </div>
            </div>
        </div>
        
        <!-- 风险提示 -->
        <div class="warning-box">
            <div class="icon">{warning_icon}</div>
            <div class="content">
                <h4>重要风险提示</h4>
                <ul>
                    <li>本报告由 AI 系统生成，仅供参考，不构成投资建议</li>
                    <li>股票投资存在风险，可能导致本金损失</li>
                    <li>请根据自身风险承受能力独立做出投资决策</li>
                </ul>
            </div>
        </div>
        
        <!-- 执行摘要 -->
        {summary_section}
        
        <!-- 分析报告模块 -->
        {reports_sections}
        
        <!-- 页脚 -->
        <div class="footer">
            <div class="footer-logo">
                {footer_icon}
                <span>TradingAgents-CN</span>
            </div>
            <p>报告 ID: {report_id} · 生成时间: {generated_time}</p>
            <p>本报告由 AI 智能分析系统生成 · 仅供参考</p>
        </div>
    </div>
</body>
</html>
"""

# 模块配置 - 使用 SVG 图标
MODULE_CONFIG = {
    'market_report': {'name': '市场技术分析', 'icon': 'chart', 'color': 'blue'},
    'fundamentals_report': {'name': '基本面分析', 'icon': 'currency', 'color': 'green'},
    'news_report': {'name': '新闻事件分析', 'icon': 'newspaper', 'color': 'orange'},
    'sentiment_report': {'name': '市场情绪分析', 'icon': 'light-bulb', 'color': 'purple'},
    'investment_plan': {'name': '投资计划', 'icon': 'document', 'color': 'blue'},
    'trader_investment_plan': {'name': '交易员计划', 'icon': 'document', 'color': 'blue'},
    'final_trade_decision': {'name': '最终交易决策', 'icon': 'target', 'color': 'green'},
    'bull_researcher': {'name': '多头研究员', 'icon': 'trending-up', 'color': 'green'},
    'bear_researcher': {'name': '空头研究员', 'icon': 'trending-down', 'color': 'red'},
    'research_team_decision': {'name': '研究经理决策', 'icon': 'light-bulb', 'color': 'purple'},
    'risky_analyst': {'name': '激进分析师', 'icon': 'bolt', 'color': 'orange'},
    'safe_analyst': {'name': '保守分析师', 'icon': 'shield', 'color': 'blue'},
    'neutral_analyst': {'name': '中性分析师', 'icon': 'scale', 'color': 'gray'},
    'risk_management_decision': {'name': '投资组合经理', 'icon': 'building', 'color': 'purple'},
}


def get_recommendation_info(recommendation: str) -> tuple:
    """解析投资建议"""
    if not recommendation:
        return '持有', 'hold', '目标价待定', 'yellow', ICONS['pause']
    
    rec_lower = recommendation.lower()
    
    if '买入' in recommendation or 'buy' in rec_lower:
        return '买入', 'buy', '', 'green', ICONS['trending-up']
    elif '卖出' in recommendation or 'sell' in rec_lower:
        return '卖出', 'sell', '', 'red', ICONS['trending-down']
    else:
        return '持有', 'hold', '', 'yellow', ICONS['pause']
    
    # 尝试提取目标价
    import re
    price_match = re.search(r'目标价[：:]\s*(\d+\.?\d*)', recommendation)
    if price_match:
        return rec_info[0], rec_info[1], f"目标价 ¥{price_match.group(1)}", rec_info[3], rec_info[4]
    
    return rec_info[0], rec_info[1], '', rec_info[3], rec_info[4]


def get_risk_indicator(risk_level: str) -> str:
    """生成风险等级指示器"""
    risk_map = {
        '低': 1,
        '中低': 2,
        '中等': 3,
        '中高': 4,
        '高': 5
    }
    
    level = risk_map.get(risk_level, 3)
    
    dots = []
    for i in range(1, 6):
        active = f'active level-{i}' if i <= level else ''
        dots.append(f'<div class="dot {active}"></div>')
    
    return ''.join(dots)


def get_confidence_level(score: int) -> str:
    """根据置信度获取等级"""
    if score >= 70:
        return 'high'
    elif score >= 40:
        return 'medium'
    else:
        return 'low'


def markdown_to_html(content: str) -> str:
    """Markdown 转 HTML"""
    if not content:
        return ''
    
    try:
        import markdown
        return markdown.markdown(content, extensions=['tables', 'fenced_code'])
    except:
        html = content
        html = html.replace('\n\n', '</p><p>')
        html = html.replace('\n', '<br>')
        return f'<p>{html}</p>'


def generate_report_sections(reports: dict) -> str:
    """生成报告模块 HTML"""
    if not reports:
        return '<div class="section"><p>暂无详细报告内容</p></div>'
    
    sections = []
    
    for module_key, content in reports.items():
        if not content:
            continue
            
        config = MODULE_CONFIG.get(module_key, {
            'name': module_key.replace('_', ' ').title(),
            'icon': 'document',
            'color': 'blue'
        })
        
        # 获取图标
        icon_svg = ICONS.get(config['icon'], ICONS['document'])
        
        # 处理内容
        if isinstance(content, str):
            content_html = markdown_to_html(content)
        else:
            content_html = f'<pre>{json.dumps(content, ensure_ascii=False, indent=2)}</pre>'
        
        section = f'''
        <div class="section">
            <div class="section-header">
                <div class="section-icon {config["color"]}">{icon_svg}</div>
                <div class="section-title">{config["name"]}</div>
            </div>
            <div class="section-content">
                {content_html}
            </div>
        </div>
        '''
        sections.append(section)
    
    return '\n'.join(sections)


def generate_pdf_report(report_data: Dict[str, Any]) -> str:
    """生成专业美观的 PDF 报告 HTML"""
    
    # 提取数据
    stock_name = report_data.get('stock_name') or '未知股票'
    stock_symbol = report_data.get('stock_symbol') or report_data.get('stock_code', 'N/A')
    recommendation = report_data.get('recommendation', '')
    confidence_raw = report_data.get('confidence_score', 0)
    confidence_score = int(confidence_raw * 100) if confidence_raw <= 1 else int(confidence_raw)
    risk_level = report_data.get('risk_level', '中等')
    summary = report_data.get('summary', '')
    reports = report_data.get('reports', {})
    model_info = report_data.get('model_info', 'AI Model')
    analysis_date = report_data.get('analysis_date', '') or report_data.get('created_at', '')[:10]
    analysts_list = report_data.get('analysts', [])
    
    # 分析师名称映射
    analyst_names = {
        'market': '市场分析师',
        'fundamentals': '基本面分析师',
        'news': '新闻分析师',
        'sentiment': '情绪分析师'
    }
    analysts = '、'.join([analyst_names.get(a, a) for a in analysts_list]) if analysts_list else 'AI 分析师'
    
    # 市场类型
    if stock_symbol.startswith('688'):
        market_type = '科创板'
    elif stock_symbol.startswith('6'):
        market_type = '上海证券交易所'
    elif stock_symbol.startswith('0') or stock_symbol.startswith('3'):
        market_type = '深圳证券交易所'
    else:
        market_type = 'A股市场'
    
    # 投资建议
    rec_short, rec_class, target_price, rec_icon_class, rec_card_icon = get_recommendation_info(recommendation)
    
    # 封面推荐图标
    rec_cover_icons = {
        'buy': ICONS['trending-up'],
        'sell': ICONS['trending-down'],
        'hold': ICONS['pause']
    }
    rec_icon = rec_cover_icons.get(rec_class, ICONS['pause'])
    
    # 风险图标
    risk_icon_class = 'yellow'
    risk_card_icon = ICONS['shield']
    if risk_level in ['低', '中低']:
        risk_icon_class = 'green'
    elif risk_level in ['高', '中高']:
        risk_icon_class = 'red'
        risk_card_icon = ICONS['warning']
    
    # 置信度图标
    confidence_icon_class = 'blue'
    confidence_card_icon = ICONS['check']
    if confidence_score >= 70:
        confidence_icon_class = 'green'
    elif confidence_score < 40:
        confidence_icon_class = 'yellow'
    
    # 生成摘要部分
    if summary:
        summary_section = f'''
        <div class="summary">
            <div class="summary-header">
                <div class="icon">{ICONS['document']}</div>
                <h3>执行摘要</h3>
            </div>
            <p>{markdown_to_html(summary)}</p>
        </div>
        '''
    else:
        summary_section = ''
    
    # 生成报告模块
    reports_sections = generate_report_sections(reports)
    
    # 填充模板
    html = PDF_TEMPLATE.format(
        stock_name=stock_name,
        stock_symbol=stock_symbol,
        market_type=market_type,
        recommendation_short=rec_short,
        rec_class=rec_class,
        rec_icon=rec_icon,
        rec_card_icon=rec_card_icon,
        rec_icon_class=rec_icon_class,
        target_price=target_price,
        risk_level=risk_level,
        risk_indicator=get_risk_indicator(risk_level),
        risk_icon_class=risk_icon_class,
        risk_card_icon=risk_card_icon,
        confidence_score=confidence_score,
        confidence_level=get_confidence_level(confidence_score),
        confidence_icon_class=confidence_icon_class,
        confidence_card_icon=confidence_card_icon,
        model_info=model_info,
        analysis_date=analysis_date,
        generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        analysts=analysts,
        cover_icon=ICONS['chart'],
        calendar_icon=ICONS['calendar'],
        user_icon=ICONS['user'],
        warning_icon=ICONS['warning'],
        footer_icon=ICONS['chart'],
        summary_section=summary_section,
        reports_sections=reports_sections,
        report_id=report_data.get('id', 'N/A')
    )
    
    return html


def export_pdf_with_weasyprint(html: str) -> bytes:
    """使用 WeasyPrint 生成 PDF"""
    try:
        from weasyprint import HTML
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            html_path = f.name
        
        pdf_bytes = HTML(filename=html_path).write_pdf()
        os.unlink(html_path)
        
        return pdf_bytes
    except Exception as e:
        logger.error(f"PDF 生成失败: {e}")
        raise


def export_pdf_report(report_data: Dict[str, Any]) -> bytes:
    """导出 PDF 报告的主入口"""
    html = generate_pdf_report(report_data)
    return export_pdf_with_weasyprint(html)


def export_html_report(report_data: Dict[str, Any]) -> str:
    """导出 HTML 报告（可用于浏览器打印）"""
    return generate_pdf_report(report_data)


class PDFExporter:
    @staticmethod
    def generate_pdf(report_data: Dict[str, Any]) -> bytes:
        return export_pdf_report(report_data)
    
    @staticmethod
    def generate_html(report_data: Dict[str, Any]) -> str:
        return export_html_report(report_data)

pdf_exporter = PDFExporter()
