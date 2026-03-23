"""
闲鱼机器人启动脚本
简化启动流程，自动加载配置
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录和src到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# 切换到项目目录，确保相对路径正确
os.chdir(project_root)

from main import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 机器人已停止")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()
