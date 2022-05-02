import json
import sys

import nonebot
from nonebot import get_bot
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot.log import logger
from nonebot.params import CommandArg

TOOLS = nonebot.get_driver().config.tools_path
sys.path.append(str(TOOLS))
from permission import checker, error
from http_ import http
from file import read, write
from config import Config


def checknumber(number):
    return number.isdecimal()


def group_exist(group):
    info = json.loads(read(TOOLS+"/webhook.json"))
    for i in info:
        if i["group"] == group:
            return True
    return False
    
def group_and_repo_exist(group, repo):
    info = json.loads(read(TOOLS+"/webhook.json"))
    for i in info:
        if i["group"] == group:
            for q in i["repo"]:
                if q == repo:
                    return True
    return False

github_repo = on_command("ghrepo",aliases={"github_repo"}, priority=5)

@github_repo.handle()
async def _(event: Event, args: Message = CommandArg()):
    repo = args.extract_plain_text()
    status_code = http.get_status("https://github.com/"+repo)
    if status_code != 200:
        await github_repo.finish("仓库获取失败，请检查后重试哦~")
    else:
        img = ms.image("https://opengraph.githubassets.com/c9f4179f4d560950b2355c82aa2b7750bffd945744f9b8ea3f93cc24779745a0/"+repo)
        await github_repo.finish(img)

wa = on_command("webhookadd",aliases={"wa"},priority=5)

@wa.handle()
async def _(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await wa.finish(error(10))
    cmd = args.extract_plain_text()
    args = cmd.split(" ")
    if len(args)>2:
        await wa.finish("唔……你的参数有多余的哦~")
    if len(args)<2:
        await wa.finish("唔……你好像缺了一些参数哦~")
    group = args[0]
    repo = args[1]
    if repo.find("/") == -1:
        await wa.finish("这不是有效的Repo名，正确的格式应为{作者/组织}/{项目名称}")
    if checknumber(group) == False:
        await wa.finish("这不是有效的QQ群号！")
    repo_status = await http.get_status("https://github.com/"+repo)
    if repo_status != 200:
        await wa.finish("Repo不存在哦~")
    if group_and_repo_exist(group, repo):
        await wa.finish("Repo已经添加过了哦~")
    if group_exist(group):
        info = json.loads(read(TOOLS+"/webhook.json"))
        for i in info:
            if i["group"] == group:
                i["repo"].append(repo)
        write(TOOLS+"/webhook.json", json.dumps(info))
        await wa.finish("绑定成功！")
    else:
        new = {"group": group, "repo": [repo]}
        info = json.loads(read(TOOLS+"/webhook.json"))
        info.append(new)
        write(TOOLS+"/webhook.json", json.dumps(info))
        await wa.finish("绑定成功！")
    
        
wr = on_command("webhookremove",aliases={"wr"},priority=5)

@wr.handle()
async def _(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await wr.finish(error(10))
    cmd = args.extract_plain_text()
    args = cmd.split(" ")
    if len(args)>2:
        await wr.finish("唔……你的参数有多余的哦~")
    if len(args)<2:
        await wr.finish("唔……你好像缺了一些参数哦~")
    group = args[0]
    repo = args[1]
    if repo.find("/") == -1 and repo != "-a":
        await wr.finish("这不是有效的Repo名，正确的格式应为{作者/组织}/{项目名称}")
    if checknumber(group) == False:
        await wr.finish("这不是有效的QQ群号啦！")
    if group_exist(group) == False:
        await wr.finish("唔……这个群尚未绑定任何Repo~")
    if group_and_repo_exist(group, repo) == False:
        await wr.finish("唔……这个群没有绑定这个仓库哦~")
    info = json.loads(read(TOOLS+"/webhook.json"))
    if repo == "-a":
        for i in info:
            if i["group"] == group:
                info.remove(i)
                write(TOOLS+"/webhook.json", json.dumps(info))
                await wr.finish("解绑成功！")
    else:
        for i in info:
            if i["group"] == group:
                for b in i["repo"]:
                    if b == repo:
                        if len(i["repo"]) == 1:
                            info.remove(i)
                            write(TOOLS+"/webhook.json", json.dumps(info))
                            await wr.finish("解绑成功！")
                        else:
                            i["repo"].remove(b)
                            write(TOOLS+"/webhook.json", json.dumps(info))
                            await wr.finish("解绑成功！")
    
from fastapi import Request, FastAPI
from .parse import main
app: FastAPI = nonebot.get_app()

@app.post(Config.web_path)
async def recWebHook(req: Request):
    body = await req.json()
    repo = body["repository"]["full_name"]
    event = req.headers.get("X-GitHub-Event")
    try:
        message = "[GitHub] " + getattr(main,event)(body)
    except:
        msg = f"Event {event} has not been supported."
        return {"status":"500","message":msg}
    bots: list = Config.bot
    for i in bots:
        bot = get_bot(i)
        await sendNbMessage(bot, message, repo)
    return {"status":200}

async def sendNbMessage(bot: Bot, message, repo):
    group_id_list = json.loads(read(TOOLS+"/webhook.json"))
    for i in group_id_list:
        for m in i["repo"]:
            if m == repo:
                group = i["group"]
                response = await bot.call_api("send_group_msg", group_id=int(group), message=message)
                logger.info(response)