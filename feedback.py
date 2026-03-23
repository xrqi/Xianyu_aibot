"""
对话反馈工具
用于手动标记对话结果，帮助AI学习优化
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))
os.chdir(project_root)

import sqlite3
from datetime import datetime
from core.learning_engine import LearningEngine
from loguru import logger


def list_recent_conversations(limit=10):
    """列出最近的对话"""
    conn = sqlite3.connect("data/chat_history.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT DISTINCT user_id, item_id, 
               MAX(timestamp) as last_time,
               COUNT(*) as msg_count
        FROM messages
        GROUP BY user_id, item_id
        ORDER BY last_time DESC
        LIMIT ?
        ''', (limit,))
        
        conversations = cursor.fetchall()
        
        print("\n" + "="*80)
        print(f"最近的 {len(conversations)} 个对话:")
        print("="*80)
        
        for i, (user_id, item_id, last_time, msg_count) in enumerate(conversations, 1):
            print(f"\n{i}. 用户: {user_id}")
            print(f"   商品: {item_id}")
            print(f"   最后消息: {last_time}")
            print(f"   消息数: {msg_count}")
        
        return conversations
        
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return []
    finally:
        conn.close()


def record_outcome(user_id, item_id, outcome, final_price=None, original_price=None):
    """记录对话结果"""
    learning = LearningEngine()
    
    try:
        learning.record_conversation_outcome(
            user_id, item_id, outcome, final_price, original_price
        )
        
        # 学习用户偏好
        preferences = learning.learn_user_preferences(user_id)
        
        print(f"\n✅ 已记录结果: {outcome}")
        if preferences:
            print(f"📊 用户价格敏感度: {preferences.get('price_sensitivity', '未知')}")
            print(f"📈 成交率: {preferences.get('success_rate', 0):.1%}")
        
    except Exception as e:
        logger.error(f"记录失败: {e}")


def show_stats():
    """显示学习统计"""
    learning = LearningEngine()
    
    try:
        report = learning.generate_weekly_report()
        
        print("\n" + "="*80)
        print("📊 本周学习报告")
        print("="*80)
        print(f"总对话数: {report.get('total_conversations', 0)}")
        print(f"成交数: {report.get('successful_deals', 0)}")
        print(f"转化率: {report.get('conversion_rate', 0):.1%}")
        print(f"平均折扣: {report.get('average_discount', 0):.1%}")
        
    except Exception as e:
        logger.error(f"生成报告失败: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
使用方法:
  python feedback.py list              # 列出最近对话
  python feedback.py stats             # 查看学习统计
  python feedback.py record <用户ID> <商品ID> <结果> [成交价] [原价]
  
结果选项: deal(成交), no_deal(未成交), ongoing(进行中)

示例:
  python feedback.py record 123456 item789 deal 80 100
        """)
        return
    
    command = sys.argv[1]
    
    if command == "list":
        conversations = list_recent_conversations()
        
        if conversations and len(sys.argv) > 2 and sys.argv[2] == "--feedback":
            # 交互式反馈
            try:
                choice = int(input("\n选择要标记的对话编号 (0退出): "))
                if 1 <= choice <= len(conversations):
                    user_id, item_id, _, _ = conversations[choice-1]
                    
                    print("\n结果选项:")
                    print("1. deal - 成交")
                    print("2. no_deal - 未成交")
                    print("3. ongoing - 进行中")
                    
                    outcome_choice = input("选择结果 (1-3): ")
                    outcomes = {"1": "deal", "2": "no_deal", "3": "ongoing"}
                    outcome = outcomes.get(outcome_choice, "ongoing")
                    
                    final_price = None
                    original_price = None
                    if outcome == "deal":
                        try:
                            final_price = float(input("成交价: "))
                            original_price = float(input("原价: "))
                        except:
                            pass
                    
                    record_outcome(user_id, item_id, outcome, final_price, original_price)
            except ValueError:
                print("请输入有效的数字")
    
    elif command == "stats":
        show_stats()
    
    elif command == "record" and len(sys.argv) >= 5:
        user_id = sys.argv[2]
        item_id = sys.argv[3]
        outcome = sys.argv[4]
        final_price = float(sys.argv[5]) if len(sys.argv) > 5 else None
        original_price = float(sys.argv[6]) if len(sys.argv) > 6 else None
        
        record_outcome(user_id, item_id, outcome, final_price, original_price)
    
    else:
        print("未知命令，使用 'python feedback.py' 查看帮助")


if __name__ == "__main__":
    main()
