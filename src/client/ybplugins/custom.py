'''
自定义功能：

在这里可以编写自定义的功能，
编写完毕后记得 git commit，

这个模块只是为了快速编写小功能，如果想编写完整插件可以使用：
https://github.com/richardchien/python-aiocqhttp
或者
https://github.com/richardchien/nonebot

关于PR：
如果基于此文件的PR，请在此目录下新建一个`.py`文件，并修改类名
然后在`yobot.py`中添加`import`（这一步可以交给仓库管理者做）
'''

import asyncio
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Union

from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart


class Custom:
    Passive = True
    Active = False
    Request = False
    horse = {'霞': '[CQ:emoji,id=128269]', '佩可': '[CQ:emoji,id=127833]', '吉塔': '[CQ:emoji,id=127928]',
             '凯留': '[CQ:emoji,id=128049]', '初音': '[CQ:emoji,id=11088]', '镜华': '[CQ:emoji,id=10000056]',
             '纺希': '[CQ:emoji,id=9986]', '栞': '[CQ:emoji,id=128567]', '美美': '[CQ:emoji,id=128048]',
             '可可萝': '[CQ:emoji,id=128052]', '香织': '[CQ:emoji,id=128054]', '真琴': '[CQ:emoji,id=128058]',
             '优衣': '[CQ:emoji,id=127800]', '伊莉亚': '[CQ:emoji,id=128137]'}
    num = 15
    dis = [25, 25, 25, 25, 25]
    running = False
    com = {}
    executor = ThreadPoolExecutor(max_workers=3)

    def __init__(self,
                 glo_setting: Dict[str, Any],
                 scheduler: AsyncIOScheduler,
                 app: Quart,
                 bot_api: Api,
                 *args, **kwargs):
        """
        初始化，只在启动时执行一次

        参数：
            glo_setting 包含所有设置项，具体见default_config.json
            bot_api 是调用机器人API的接口，具体见<https://python-aiocqhttp.cqp.moe/>
            scheduler 是与机器人一同启动的AsyncIOScheduler实例
            app 是机器人后台Quart服务器实例
        """
        # 注意：这个类加载时，asyncio事件循环尚未启动，且bot_api没有连接
        # 此时不要调用bot_api
        # 此时没有running_loop，不要直接使用await，请使用asyncio.ensure_future并指定loop=asyncio.get_event_loop()

        # 如果需要启用，请注释掉下面一行
        # return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        self.api = bot_api
        # 注册定时任务，详见apscheduler文档
        # @scheduler.scheduled_job('cron', hour=8)
        # async def good_morning():
        #     await self.api.send_group_msg(group_id=123456, message='早上好')

        # # 注册web路由，详见flask与quart文档
        # @app.route('/is-bot-running', methods=['GET'])
        # async def check_bot():
        #     return 'yes, bot is running'

    def showhorse(self):
        s = ""
        horse_cp = {'霞': '[CQ:emoji,id=128269]', '佩可': '[CQ:emoji,id=127833]', '吉塔': '[CQ:emoji,id=127928]',
                    '凯留': '[CQ:emoji,id=128049]', '初音': '[CQ:emoji,id=11088]', '镜华': '[CQ:emoji,id=10000056]',
                    '纺希': '[CQ:emoji,id=9986]', '栞': '[CQ:emoji,id=128567]', '美美': '[CQ:emoji,id=128048]',
                    '可可萝': '[CQ:emoji,id=128052]', '香织': '[CQ:emoji,id=128054]', '真琴': '[CQ:emoji,id=128058]',
                    '优衣': '[CQ:emoji,id=127800]', '伊莉亚': '[CQ:emoji,id=128137]'}
        self.com.clear()
        for i in range(0, 5):
            a = random.sample(horse_cp.keys(), 1)  # 随机一个字典中的key，第二个参数为限制个数
            b = a[0]
            del horse_cp[b]
            self.com[b] = self.horse[b]
            s += str(i + 1) + '号:' + b + ',' + '图标为' + self.horse[b]
            if i < 4:
                s += '\n'
        return s

    def run(self):
        return

    async def competition(self, group_id):
        await self.api.send_group_msg(group_id=group_id, message='兰德索尔赛跑即将开始！下面为您介绍参赛选手：')
        await self.api.send_group_msg(group_id=group_id, message=self.showhorse())
        # while self.running is True:
        #
        #     return

    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        """
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        """
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        # return

        cmd = ctx['raw_message']
        if cmd == '你好':
            # 调用api发送消息，详见cqhttp文档
            await self.api.send_private_msg(user_id=ctx['sender']['user_id'], message='收到问好')
            reply = None
            # 返回字符串：发送消息并阻止后续插件
        elif cmd == '赛跑开始' and 'group_id' in ctx and self.running is False:
            # t1 = threading.Thread(target=self.competition, args=(ctx['group_id'],))
            # t1.start()
            future = self.executor.submit( self.competition, ctx['group_id'])
            reply = None
        elif self.running is True:
            return "赛跑中"
        else:
            reply = None
        return True

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        # return False
