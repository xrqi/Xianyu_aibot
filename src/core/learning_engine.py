"""
AI学习引擎模块
负责收集对话反馈，分析回复效果，持续优化回复策略
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger


class LearningEngine:
    """
    AI学习引擎
    
    功能：
    1. 收集对话结果反馈（成交/未成交/继续聊）
    2. 分析不同回复策略的效果
    3. 自动优化提示词和回复策略
    4. 学习用户偏好和商品特征
    """
    
    def __init__(self, db_path: str = "data/chat_history.db"):
        self.db_path = db_path
        self._init_learning_tables()
        
    def _init_learning_tables(self):
        """初始化学习相关的数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 对话结果反馈表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            conversation_id TEXT,
            outcome TEXT,  -- 'deal', 'no_deal', 'ongoing', 'unresponsive'
            final_price REAL,
            original_price REAL,
            message_count INTEGER,
            user_satisfaction INTEGER,  -- 1-5星，如果有反馈
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 回复效果评估表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reply_effectiveness (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            reply_type TEXT,  -- 'price', 'tech', 'default'
            reply_content TEXT,
            user_response TEXT,
            response_time_seconds INTEGER,
            is_positive BOOLEAN,  -- 用户是否积极回应
            leading_to_deal BOOLEAN,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 用户偏好学习表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            preferred_tone TEXT,  -- 'formal', 'casual', 'enthusiastic'
            price_sensitivity TEXT,  -- 'high', 'medium', 'low'
            response_speed_preference TEXT,  -- 'immediate', 'patient'
            common_concerns TEXT,  -- JSON array
            successful_strategies TEXT,  -- JSON array
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 商品销售策略效果表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_strategies (
            item_id TEXT PRIMARY KEY,
            category TEXT,
            optimal_price_range TEXT,  -- JSON {"min": x, "max": y}
            best_selling_points TEXT,  -- JSON array
            common_objections TEXT,  -- JSON array
            successful_replies TEXT,  -- JSON array of templates
            conversion_rate REAL DEFAULT 0,
            total_conversations INTEGER DEFAULT 0,
            successful_deals INTEGER DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("学习引擎数据库表初始化完成")
    
    def record_conversation_outcome(self, user_id: str, item_id: str, 
                                   outcome: str, final_price: float = None,
                                   original_price: float = None, 
                                   message_count: int = 0):
        """记录对话结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO conversation_outcomes 
            (user_id, item_id, outcome, final_price, original_price, message_count)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, item_id, outcome, final_price, original_price, message_count))
            
            conn.commit()
            logger.info(f"记录对话结果: user={user_id}, outcome={outcome}")
        except Exception as e:
            logger.error(f"记录对话结果失败: {e}")
        finally:
            conn.close()
    
    def record_reply_effectiveness(self, user_id: str, item_id: str,
                                  reply_type: str, reply_content: str,
                                  user_response: str = None,
                                  response_time: int = 0,
                                  is_positive: bool = None):
        """记录回复效果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 判断用户回应是否积极
            if is_positive is None and user_response:
                is_positive = self._analyze_positive_response(user_response)
            
            cursor.execute('''
            INSERT INTO reply_effectiveness 
            (user_id, item_id, reply_type, reply_content, user_response,
             response_time_seconds, is_positive)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, item_id, reply_type, reply_content, 
                  user_response, response_time, is_positive))
            
            conn.commit()
        except Exception as e:
            logger.error(f"记录回复效果失败: {e}")
        finally:
            conn.close()
    
    def _analyze_positive_response(self, user_response: str) -> bool:
        """分析用户回应是否积极"""
        positive_keywords = ['好的', '可以', '行', '没问题', '满意', '喜欢', 
                           '要了', '拍下', '下单', '成交', 'ok', '好的呢']
        negative_keywords = ['不要', '算了', '太贵', '再看看', '考虑一下', 
                           '不满意', '不好', '不行']
        
        response_lower = user_response.lower()
        
        positive_score = sum(1 for kw in positive_keywords if kw in response_lower)
        negative_score = sum(1 for kw in negative_keywords if kw in response_lower)
        
        return positive_score > negative_score
    
    def learn_user_preferences(self, user_id: str) -> Dict:
        """学习用户偏好"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 分析用户的回复模式
            cursor.execute('''
            SELECT reply_type, is_positive, COUNT(*) as count
            FROM reply_effectiveness
            WHERE user_id = ?
            GROUP BY reply_type, is_positive
            ''', (user_id,))
            
            results = cursor.fetchall()
            
            # 分析哪种回复类型最有效
            type_effectiveness = {}
            for reply_type, is_positive, count in results:
                if reply_type not in type_effectiveness:
                    type_effectiveness[reply_type] = {'positive': 0, 'total': 0}
                type_effectiveness[reply_type]['total'] += count
                if is_positive:
                    type_effectiveness[reply_type]['positive'] += count
            
            # 计算每种回复类型的成功率
            best_type = None
            best_rate = 0
            for rtype, stats in type_effectiveness.items():
                rate = stats['positive'] / stats['total'] if stats['total'] > 0 else 0
                if rate > best_rate:
                    best_rate = rate
                    best_type = rtype
            
            # 分析价格敏感度
            cursor.execute('''
            SELECT outcome, COUNT(*) as count
            FROM conversation_outcomes
            WHERE user_id = ?
            GROUP BY outcome
            ''', (user_id,))
            
            outcomes = {row[0]: row[1] for row in cursor.fetchall()}
            total = sum(outcomes.values())
            deal_rate = outcomes.get('deal', 0) / total if total > 0 else 0
            
            price_sensitivity = 'high' if deal_rate < 0.3 else 'low' if deal_rate > 0.7 else 'medium'
            
            # 保存学习结果
            preferences = {
                'preferred_reply_type': best_type,
                'price_sensitivity': price_sensitivity,
                'success_rate': deal_rate,
                'total_interactions': total
            }
            
            cursor.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (user_id, price_sensitivity, successful_strategies, last_updated)
            VALUES (?, ?, ?, ?)
            ''', (user_id, price_sensitivity, json.dumps(preferences), datetime.now()))
            
            conn.commit()
            return preferences
            
        except Exception as e:
            logger.error(f"学习用户偏好失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_optimized_prompt_additions(self, user_id: str, item_id: str) -> str:
        """获取针对特定用户和商品的优化提示词补充"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        additions = []
        
        try:
            # 获取用户偏好
            cursor.execute('''
            SELECT price_sensitivity, successful_strategies
            FROM user_preferences
            WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                price_sensitivity = row[0]
                if price_sensitivity == 'high':
                    additions.append("该用户对价格敏感，可以适当强调性价比和优惠。")
                elif price_sensitivity == 'low':
                    additions.append("该用户不太在意价格，可以强调商品品质和价值。")
            
            # 获取商品策略
            cursor.execute('''
            SELECT best_selling_points, common_objections, successful_replies
            FROM item_strategies
            WHERE item_id = ?
            ''', (item_id,))
            
            row = cursor.fetchone()
            if row:
                selling_points = json.loads(row[0]) if row[0] else []
                objections = json.loads(row[1]) if row[1] else []
                
                if selling_points:
                    additions.append(f"该商品的最佳卖点: {', '.join(selling_points[:3])}")
                if objections:
                    additions.append(f"常见顾虑及应对: {', '.join(objections[:2])}")
            
        except Exception as e:
            logger.error(f"获取优化提示词失败: {e}")
        finally:
            conn.close()
        
        return "\n".join(additions) if additions else ""
    
    def analyze_successful_patterns(self, limit: int = 100) -> List[Dict]:
        """分析成功的对话模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 找出导致成交的回复
            cursor.execute('''
            SELECT r.reply_type, r.reply_content, r.user_response,
                   o.final_price, o.original_price
            FROM reply_effectiveness r
            JOIN conversation_outcomes o ON r.user_id = o.user_id AND r.item_id = o.item_id
            WHERE o.outcome = 'deal'
            ORDER BY o.created_at DESC
            LIMIT ?
            ''', (limit,))
            
            successful_patterns = []
            for row in cursor.fetchall():
                successful_patterns.append({
                    'reply_type': row[0],
                    'reply_content': row[1],
                    'user_response': row[2],
                    'discount_rate': (row[3] / row[4]) if row[4] and row[4] > 0 else 1.0
                })
            
            return successful_patterns
            
        except Exception as e:
            logger.error(f"分析成功模式失败: {e}")
            return []
        finally:
            conn.close()
    
    def generate_weekly_report(self) -> Dict:
        """生成每周学习报告"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 统计本周数据
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            
            cursor.execute('''
            SELECT 
                COUNT(*) as total_conversations,
                SUM(CASE WHEN outcome = 'deal' THEN 1 ELSE 0 END) as deals,
                AVG(CASE WHEN outcome = 'deal' THEN 
                    (original_price - final_price) / original_price ELSE NULL END) as avg_discount
            FROM conversation_outcomes
            WHERE created_at > ?
            ''', (week_ago,))
            
            row = cursor.fetchone()
            report = {
                'total_conversations': row[0] or 0,
                'successful_deals': row[1] or 0,
                'conversion_rate': (row[1] / row[0]) if row[0] > 0 else 0,
                'average_discount': row[2] or 0,
                'period': 'last_7_days'
            }
            
            return report
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return {}
        finally:
            conn.close()
