import asyncio
import os
import platform
import argparse
from loguru import logger
from dotenv import load_dotenv

from api.xianyu_websocket import XianyuLive
from agents.expert_agents import XianyuReplyBot
from core.context_manager import ChatContextManager
from utils.xianyu_utils import get_login_cookies, load_cookies, trans_cookies, cookies_dict_to_str, save_manual_cookies

# 检测操作系统类型
IS_WINDOWS = platform.system() == 'Windows'

async def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='闲鱼机器人')
    parser.add_argument('--login', action='store_true', help='强制使用浏览器获取闲鱼登录凭证（会删除已保存的cookies）')
    parser.add_argument('--manual-cookies', type=str, help='手动输入cookies字符串（格式: key1=value1; key2=value2）')
    args = parser.parse_args()
    
    # 加载环境变量
    load_dotenv()
    
    # 如果指定了强制登录选项，删除已保存的cookies并重新获取
    if args.login:
        import os
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        cookies_path = os.path.join(data_dir, 'xianyu_cookies.json')
        if os.path.exists(cookies_path):
            try:
                os.remove(cookies_path)
                logger.info("已删除旧的cookies文件")
            except Exception as e:
                logger.warning(f"删除旧cookies文件失败: {e}")
        
        logger.info("准备使用浏览器获取闲鱼登录凭证")
        cookies_data = await get_login_cookies()
        if not cookies_data:
            logger.error("获取登录凭证失败")
            return
        logger.info("成功获取登录凭证，继续启动机器人")
    
    # 如果指定了手动输入cookies，保存到文件
    if args.manual_cookies:
        logger.info("使用手动输入的cookies...")
        if save_manual_cookies(args.manual_cookies):
            logger.info("手动cookies保存成功")
        else:
            logger.error("手动cookies保存失败，请检查格式")
            return
    
    # 尝试从文件加载cookies
    cookies_data = load_cookies()
    cookies_str = None
    
    if cookies_data and "cookies" in cookies_data:
        cookies_dict = cookies_data["cookies"]
        cookies_str = cookies_dict_to_str(cookies_dict)
        logger.info("成功从文件加载登录凭证")
    
    # 如果没有有效的cookies，提示用户输入
    if not cookies_str:
        logger.error("未找到有效的闲鱼cookies，请使用以下方式之一提供：")
        logger.error("1. 手动输入cookies: python run.py --manual-cookies '你的cookies'")
        logger.error("2. 浏览器登录获取: python run.py --login")
        return
    
    # 初始化回复机器人
    bot = XianyuReplyBot()
    
    # 初始化websocket连接
    xianyu_live = XianyuLive(cookies_str, bot)
    
    # 启动主循环
    await xianyu_live.main()

if __name__ == "__main__":
    try:
        # 在Windows上设置默认事件循环策略，解决asyncio兼容性问题
        if IS_WINDOWS:
            # Windows平台使用SelectorEventLoop避免ProactorEventLoop的问题
            # 解决Windows上常见的"Event loop is closed"错误
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            logger.info("Windows平台: 设置了WindowsSelectorEventLoopPolicy")
            
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")