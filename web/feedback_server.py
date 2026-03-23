"""
反馈管理Web服务器
提供可视化界面查看对话和标记结果
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))
os.chdir(project_root)

import sqlite3
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from core.learning_engine import LearningEngine

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

DB_PATH = "data/chat_history.db"


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """主页"""
    return render_template('feedback.html')


@app.route('/api/conversations')
def get_conversations():
    """获取最近对话列表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT DISTINCT m.user_id, m.item_id, 
               MAX(m.timestamp) as last_time,
               COUNT(*) as msg_count,
               (SELECT content FROM messages 
                WHERE user_id = m.user_id AND item_id = m.item_id 
                ORDER BY timestamp DESC LIMIT 1) as last_message
        FROM messages m
        GROUP BY m.user_id, m.item_id
        ORDER BY last_time DESC
        LIMIT 50
        ''')
        
        conversations = []
        for row in cursor.fetchall():
            user_id = row['user_id']
            item_id = row['item_id']
            
            # 查询是否已标记
            cursor.execute('''
            SELECT outcome FROM conversation_outcomes
            WHERE user_id = ? AND item_id = ?
            ORDER BY created_at DESC LIMIT 1
            ''', (user_id, item_id))
            
            outcome_row = cursor.fetchone()
            outcome = outcome_row['outcome'] if outcome_row else None
            
            conversations.append({
                'user_id': user_id,
                'item_id': item_id,
                'last_time': row['last_time'],
                'msg_count': row['msg_count'],
                'last_message': row['last_message'][:100] + '...' if row['last_message'] and len(row['last_message']) > 100 else row['last_message'],
                'outcome': outcome
            })
        
        return jsonify({'success': True, 'data': conversations})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()


@app.route('/api/conversation/<user_id>/<item_id>')
def get_conversation_detail(user_id, item_id):
    """获取对话详情"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT role, content, timestamp
        FROM messages
        WHERE user_id = ? AND item_id = ?
        ORDER BY timestamp ASC
        ''', (user_id, item_id))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'role': row['role'],
                'content': row['content'],
                'timestamp': row['timestamp']
            })
        
        # 获取议价次数
        cursor.execute('''
        SELECT count FROM bargain_counts
        WHERE user_id = ? AND item_id = ?
        ''', (user_id, item_id))
        
        row = cursor.fetchone()
        bargain_count = row['count'] if row else 0
        
        return jsonify({
            'success': True,
            'data': {
                'messages': messages,
                'bargain_count': bargain_count,
                'user_id': user_id,
                'item_id': item_id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()


@app.route('/api/record_outcome', methods=['POST'])
def record_outcome():
    """记录对话结果"""
    try:
        data = request.json
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        outcome = data.get('outcome')
        final_price = data.get('final_price')
        original_price = data.get('original_price')
        
        if not all([user_id, item_id, outcome]):
            return jsonify({'success': False, 'error': '缺少必要参数'})
        
        learning = LearningEngine()
        
        # 获取消息数量
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM messages
        WHERE user_id = ? AND item_id = ?
        ''', (user_id, item_id))
        msg_count = cursor.fetchone()[0]
        conn.close()
        
        learning.record_conversation_outcome(
            user_id, item_id, outcome, final_price, original_price, msg_count
        )
        
        # 学习用户偏好
        preferences = learning.learn_user_preferences(user_id)
        
        return jsonify({
            'success': True,
            'message': '记录成功',
            'preferences': preferences
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/stats')
def get_stats():
    """获取统计报告"""
    try:
        learning = LearningEngine()
        report = learning.generate_weekly_report()
        
        # 获取更详细的统计
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 总对话数
        cursor.execute('SELECT COUNT(DISTINCT user_id || item_id) FROM messages')
        total_conversations = cursor.fetchone()[0]
        
        # 总消息数
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]
        
        # 成交统计
        cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN outcome = 'deal' THEN 1 ELSE 0 END) as deals,
            AVG(CASE WHEN outcome = 'deal' THEN final_price END) as avg_price,
            AVG(CASE WHEN outcome = 'deal' THEN (original_price - final_price) / original_price END) as avg_discount
        FROM conversation_outcomes
        ''')
        
        row = cursor.fetchone()
        outcome_stats = {
            'total_recorded': row[0] or 0,
            'deals': row[1] or 0,
            'avg_price': round(row[2], 2) if row[2] else 0,
            'avg_discount': round(row[3] * 100, 1) if row[3] else 0
        }
        
        # 最近7天趋势
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute('''
        SELECT date(timestamp) as day, COUNT(*) as count
        FROM messages
        WHERE timestamp > ?
        GROUP BY date(timestamp)
        ORDER BY day
        ''', (week_ago,))
        
        daily_trend = [{'day': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'weekly_report': report,
                'total_conversations': total_conversations,
                'total_messages': total_messages,
                'outcome_stats': outcome_stats,
                'daily_trend': daily_trend
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/user_preferences/<user_id>')
def get_user_preferences(user_id):
    """获取用户偏好"""
    try:
        learning = LearningEngine()
        preferences = learning.learn_user_preferences(user_id)
        
        return jsonify({
            'success': True,
            'data': preferences
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 XianyuBot 反馈管理后台")
    print("=" * 60)
    print("访问地址: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
