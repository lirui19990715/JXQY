import sys
import nonebot
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg, Arg
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.typing import T_State
TOOLS = nonebot.get_driver().config.tools_path
sys.path.append(TOOLS)
from .jx3 import *
from utils import checknumber
from .skilldatalib import getAllSkillsInfo, getSingleSkill, getSingleTalent
from .achievement import getAchievementFinishMethod
from .adventure import getAdventure, getAchievementsIcon
from .pet import get_pet
from .task import getTask, getTaskChain

horse = on_command("jx3_horse",aliases={"马"},priority=5)
@horse.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await horse.finish(await horse_flush_place(args.extract_plain_text()))
    else:
        await horse.finish("没有输入任何马的名称哦，没办法帮你找啦。")

server = on_command("jx3_server",aliases={"服务器"},priority=5)
@server.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await server.finish(await server_status(args.extract_plain_text()))
    else:
        await server.finish("没有输入任何服务器名称哦，没办法帮你找啦。")

macro = on_command("jx3_macro",aliases={"宏"},priority=5)
@macro.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await macro.finish(await macro_(args.extract_plain_text()))
    else:
        await macro.finish("没有输入任何心法名称哦，没办法帮你找啦。")

daily = on_command("jx3_daily",aliases={"日常","周常"},priority=5)
@daily.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await daily.finish(await daily_(args.extract_plain_text()))
    else:
        await daily.finish("没有输入任何服务器名称哦，自动切换至电信一区-长安城。\n"+await daily_("长安城"))
        
exam = on_command("jx3_exam",aliases={"科举"},priority=5)
@exam.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await exam.finish(await exam_(args.extract_plain_text()))
    else:
        await exam.finish("没有提供科举的问题，没办法解答啦。")
        
matrix = on_command("jx3_matrix",aliases={"阵眼"},priority=5)
@matrix.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await matrix.finish(await matrix_(args.extract_plain_text()))
    else:
        await matrix.finish("没有输入任何心法名称哦，没办法帮你找啦。")
        
equip = on_command("jx3_equip",aliases={"装备"},priority=5)
@equip.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await equip.finish(await equip_(args.extract_plain_text()))
    else:
        await equip.finish("没有输入任何心法名称哦，没办法帮你找啦。")
        
require = on_command("jx3_require",aliases={"奇遇信息"},priority=5)
@require.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await require.finish(await require_(args.extract_plain_text()))
    else:
        await require.finish("没有输入任何奇遇名称，没办法帮你找啦，输入时也请不要输入宠物奇遇哦~")
        
news = on_command("jx3_news",aliases={"新闻"},priority=5)
@news.handle()
async def _():
    await require.finish(await news_())
    
random_ = on_command("jx3_random",aliases={"骚话"},priority=5)
@random_.handle()
async def _():
    await random_.finish("来自“万花谷”频道：\n"+await random__())
    
heighten = on_command("jx3_heighten",aliases={"小药"},priority=5)
@heighten.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await heighten.finish(await heighten_(args.extract_plain_text()))
    else:
        await heighten.finish("没有输入任何心法名称哦，没办法帮你找啦。")

price = on_command("jx3_price",aliases={"物价"},priority=5)
@price.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await price.finish(await price_(args.extract_plain_text()))
    else:
        await price.finish("没有输入任何外观名称哦，没办法帮你找啦。")

demon = on_command("jx3_demon",aliases={"金价"},priority=5)
@demon.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text():
        await demon.finish(await demon_(args.extract_plain_text()))
    else:
        await demon.finish("没有输入任何服务器名称哦，没办法帮你找啦。")

kungfu = on_command("jx3_kungfu",aliases={"心法"},priority=5)
@kungfu.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    kungfu_ = args.extract_plain_text()
    node = await getAllSkillsInfo(kungfu_)
    if node == False:
        await kungfu.finish("此心法不存在哦，请检查后重试~")
    await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = node)

skill = on_command("jx3_skill",aliases={"技能"},priority=5)
@skill.handle()
async def _(args: Message = CommandArg()):
    info = args.extract_plain_text().split(" ")
    if len(info) != 2:
        await skill.finish("信息不正确哦，只能有2个参数，请检查后重试~")
    else:
        kungfu = info[0]
        skill_ = info[1]
    msg = await getSingleSkill(kungfu, skill_)
    if msg == False:
        await skill.finish("此心法不存在哦，请检查后重试~")
    await skill.finish(msg)

adventure = on_command("jx3_achievement",aliases={"奇遇"},priority=5)
@adventure.handle()
async def _(args: Message = CommandArg()):
    adventure_name = args.extract_plain_text()
    if adventure_name == False:
        await adventure.finish("没有输入奇遇名称，没办法帮你找啦！")
    else:
        msg = await getAchievementFinishMethod(adventure_name)
        await adventure.finish(msg)

talent = on_command("jx3_talent",aliases={"奇穴"},priority=5)
@talent.handle()
async def _(args: Message = CommandArg()):
    data = args.extract_plain_text()
    data = data.split(" ")
    if len(data) != 2:
        await talent.finish("信息不正确哦，只能有2个参数，请检查后重试~")
    else:
        kungfu = data[0]
        talent_ = data[1]
        msg = await getSingleTalent(kungfu, talent_)
        await talent.finish(msg)

pet_ = on_command("get_pet", aliases={"宠物"}, priority=5)
@pet_.handle()
async def _(state: T_State, args: Message = CommandArg()):
    data = args.extract_plain_text()
    info = await get_pet(data)
    if info["status"] == 404:
        await pet_.finish("唔……没有找到你要的宠物，请检查后重试~")
    elif info["status"] == 201:
        from nonebot.log import logger
        logger.info(info)
        result = info["result"]
        state["result"] = result
        desc = info["desc"]
        state["desc"] = desc
        clue = info["clue"]
        state["clue"] = clue
        url = info["url"]
        state["url"] = url
        msg = ""
        for i in range(len(result)):
            msg = msg + f"\n{i}.{result[i]}"
        msg = msg[1:]
        await pet_.send(msg)

@pet_.got("num", prompt="发送序号以搜索，发送其他内容则取消搜索。")
async def __(state: T_State, num: Message = Arg()):
    num = num.extract_plain_text()
    if checknumber(num):
        result = state["result"]
        desc = state["desc"]
        clue = state["clue"]
        url = state["url"]
        name = result[int(num)]
        desc = desc[int(num)] 
        clue = clue[int(num)]
        url = url[int(num)]
        msg = f"查询到「{name}」：\n{url}\n{clue}\n{desc}"
        await pet_.finish(msg)
    else:
        await pet_.finish("唔……输入的不是数字哦，取消搜索。")

adventure_ = on_command("jx3_adventure", aliases={"成就"}, priority=5)# 别骂了，想不出其他变量名了
@adventure_.handle()
async def _(state: T_State, args: Message = CommandArg()):
    achievement_name = args.extract_plain_text()
    data = await getAdventure(achievement_name)
    if data["status"] == 404:
        await adventure_.finish("没有找到任何相关成就哦，请检查后重试~")
    elif data["status"] == 200:
        achievement_list = data["achievements"]
        icon_list = data["icon"]
        subAchievements = data["subAchievements"]
        id_list = data["id"]
        simpleDesc = data["simpDesc"]
        fullDesc = data["Desc"]
        point = data["point"]
        map = data["map"]
        state["map"] = map
        state["point"] = point
        state["achievement_list"] = achievement_list
        state["icon_list"] = icon_list
        state["id_list"] = id_list
        state["simpleDesc"] = simpleDesc
        state["fullDesc"] = fullDesc
        state["subAchievements"] = subAchievements
        msg = ""
        for i in range(len(achievement_list)):
            msg = msg + f"{i}." + achievement_list[i] + "\n"
        msg = msg[:-1]
        await adventure_.send(msg)
        return

@adventure_.got("num", prompt = "发送序号以搜索，发送其他内容则取消搜索。")
async def _(state: T_State, num: Message = Arg()):
    num = num.extract_plain_text()
    if checknumber(num):
        num = int(num)
        map = state["map"][num]
        achievement = state["achievement_list"][num]
        icon = state["icon_list"][num]
        id = state["id_list"][num]
        simpleDesc = state["simpleDesc"][num]
        point = state["point"][num]
        fullDesc = state["fullDesc"][num]
        subAchievement = state["subAchievements"][num]
        msg = f"查询到「{achievement}」：\n" + await getAchievementsIcon(icon) + f"\nhttps://www.jx3box.com/cj/view/{id}\n{simpleDesc}\n{fullDesc}\n地图：{map}\n资历：{point}点\n附属成就：{subAchievement}"
        await adventure_.finish(msg)
    else:
        await adventure_.finish("唔……输入的不是数字哦，取消搜索。")

task_ = on_command("jx3_task", aliases={"任务"}, priority=5)
@task_.handle()
async def _(state: T_State, args: Message = CommandArg()):
    task__ = args.extract_plain_text()
    data = await getTask(task__)
    if data["status"] == 404:
        await task_.finish("未找到该任务，请检查后重试~")
    map = data["map"]
    id = data["id"]
    task___ = data["task"]
    target = data["target"]
    level = data["level"]
    state["map"] = map
    state["id"] = id
    state["task"] = task___
    state["target"] = target
    state["level"] = level
    msg = ""
    for i in range(len(map)):
        msg = msg + f"{i}.{map[i]}：{task___[i]}\n"
    msg = msg[:-1]
    await task_.send(msg)
    return

@task_.got("num", prompt="发送序号以搜索，发送其他内容则取消搜索。")
async def _(state: T_State, num: Message = Arg()):
    num = num.extract_plain_text()
    if checknumber(num):
        num = int(num)
        map = state["map"][num]
        id = state["id"][num]
        task__ = state["task"][num]
        target = state["target"][num]
        level = state["level"][num]
        msg = f"查询到「{task__}」：\nhttps://www.jx3box.com/quest/view/{id}\n开始等级：{level}\n地图：{map}\n任务目标：{target}"
        chain = await getTaskChain(id)
        msg = msg + f"\n任务链：{chain}"
        await task_.finish(msg)
    else:
        await task_.finish("唔……输入的不是数字哦，取消搜索。")

from nonebot.internal.driver.model import Request
from websockets.legacy.client import WebSocketClientProtocol
from nonebot.drivers.websockets import WebSocket
import websockets

class JX3API_RECV():
    def __init__(self):
        self.wss_url = "wss://socket.nicemoe.cn"
    async def _(self):
        async with websockets.connect(self.wss_url) as websocket:
            while True:
				tmp = await websocket.recv()
                print(tmp)