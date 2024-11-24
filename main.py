flag_not_support = False
try:
    from util.plugin_dev.api.v1.bot import Context, AstrMessageEvent, CommandResult
    from util.plugin_dev.api.v1.config import *
    from util.plugin_dev.api.v1.types import Image, Plain
except ImportError:
    flag_not_support = True
    print("导入接口失败。请升级到 AstrBot 最新版本。")
from addons.plugins.astrbot_plugin_qqAD.config import *

'''
注意以格式 XXXPlugin 或 Main 来修改插件名。
提示：把此模板仓库 fork 之后 clone 到机器人文件夹下的 addons/plugins/ 目录下，然后用 Pycharm/VSC 等工具打开可获更棒的编程体验（自动补全等）
'''
class Main:
    """
    AstrBot 会传递 context 给插件。
    
    - context.register_commands: 注册指令
    - context.register_task: 注册任务
    - context.message_handler: 消息处理器(平台类插件用)
    """
    def __init__(self, context: Context) -> None:
        self.context = context
        self.context.register_commands('qqAD','.*', 'q群发送广告', 1, self.send_ad, use_regex=True)
        self.count = []
        self.groups = []

    """
    指令处理函数。
    
    - 需要接收两个参数：message: AstrMessageEvent, context: Context
    - 返回 CommandResult 对象
    """

    #插件实现的主函数
    async def send_ad(self, message: AstrMessageEvent, context: Context):
        await self.load_groups(message)
        get_msg = message.message_str
        group_id = message.session_id
        await self.check_msg(get_msg, group_id)
        for i, count in enumerate(self.count):
            if count >= delay:
                await self.send_msg(message, self.groups[i])
                self.count[i] = 0
                break
        return None
            
    #加载群聊
    async def load_groups(self,message: AstrMessageEvent):
        if message.session_id not in self.groups:
            print('加载群聊',message.session_id,)
            self.groups.append(message.session_id)
            self.count.append(0)
            print(self.groups,'/n',self.count)


        
    #检查消息中是否包含关键词,并记数
    async def check_msg(self, get_msg, group_id):
        for keyword in keywords:
            if keyword in get_msg:
                id = self.groups.index(group_id)
                print(id)
                self.count[id] += 1
                break
    
    #主动发送信息的封装
    async def send_msg(self, message: AstrMessageEvent, group_id):
        platforms = self.context.platforms
        platform = None
        for p in platforms:
            if p.platform_name == 'aiocqhttp':
                platform = p
                break
        if platform:
            inst = message.platform.platform_instance
            try:
                await inst.send_msg({"group_id": group_id}, CommandResult(message_chain=[Plain(txt), 
                                                                                    Image.fromFileSystem(img_path)]).use_t2i(False))
                print(f'发送成功，当前groupid为{group_id}\n')
            except Exception as e:
                print(f'发送失败，当前groupid为{group_id}\n',e)

        



