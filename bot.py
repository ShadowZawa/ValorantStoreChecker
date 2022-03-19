from discord.ext import commands 
from discord.ext.commands import bot
import json, os, requests, re
import discord
import json
from os.path import exists


from Draw import generate_image
from Auth import Auth
bot = commands.Bot(command_prefix="-")

with open('items.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    
@bot.command()
async def version(ctx):
    await ctx.send(f"目前版本為 1.0")
@bot.command()
async def hi(ctx):
    await ctx.send(f"hi~ <@{ctx.author.id}>")
@bot.command()
async def login(ctx, username:str, password:str):
    try:
        print("username: " + username)
        print("password: " + password)
        Auth.username = username
        Auth.password = password
        au = Auth.authenticate(Auth)
        access_token = au[0]
        user_id = au[1]
        entitlements_token = au[2]


        #await ctx.send(f"access_token: " + access_token)
        print('Access Token: ' + access_token)
        await ctx.send(f"綁定成功")
    except NameError:
        await ctx.send(f"密碼或使用者名稱錯誤 請確認後再試一次")
    except KeyError:
        await ctx.send(f"密碼或使用者名稱錯誤 請確認後再試一次")
    finally:
        dcid = str(ctx.author.id)
        fileName = "users/" + dcid + ".json"
        with open(fileName,"w") as file:
            data = {
                "discord_name": ctx.author.name,
                "discord_id": ctx.author.id,
                "user_id": user_id, 
                "username": username, 
                "password": password
                }
            json.dump(data, file) 
        print(f"access token: " + access_token)
        print(f"entitlements token: " + entitlements_token)
        print(f"user id: " + user_id)
        #entitlements_token = r.json()['entitlements_token']
       # print('Entitlements Token: ' + entitlements_token)

        
    #await ctx.send(f"entitlements token: " + entitlements_token)
    #await ctx.send(f"user id:" + user_id)
@bot.command()
async def wallet(ctx):
    dcid = str(ctx.author.id)
    if (os.path.exists("users/" + dcid + ".json") == False):
        await ctx.send(f"你尚未綁定Riot帳號 請私訊我 -login 帳號 密碼")
    else:
        await ctx.send(f"正在取得錢包 資料...")
        url = "https://pd.ap.a.pvp.net/store/v1/wallet/368e77a9-9c3e-5d30-a376-b6ed02332041"
        with open("users/" + dcid + ".json") as f:
            pdata = json.load(f)
        Auth.username = pdata['username']
        Auth.password = pdata['password']
        au = Auth.authenticate(Auth)
        access_token = au[0]
        user_id = au[1]
        entitlements_token = au[2]        
        print(f"access token: " + access_token)
        print(f"entitlements token: " + entitlements_token)
        print(f"user id: " + user_id)
        payload = ""
        headers = {
            "X-Riot-Entitlements-JWT": entitlements_token,
            "Authorization": "Bearer " + access_token
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print(response.text)
        data = response.json()
        c1 = data['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
        c2 = data['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']

        print("特務幣: " + str(c1))
        print("輻能點: " + str(c2))
        embed=discord.Embed(title="錢包", url="https://cdn.discordapp.com/attachments/896664897046315008/946396645002727424/9LAUtPMJxhqx8H2KAv-oipyMnAwFErAUyhUwsz-aNiM.jpg", descripetion="嘿...就是你的錢包uwu", color = discord.Colour.red())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/896664897046315008/946396645002727424/9LAUtPMJxhqx8H2KAv-oipyMnAwFErAUyhUwsz-aNiM.jpg")
        embed.add_field(name="特務幣: ", value=str(c1), inline=False)
        embed.add_field(name="輻能點: ", value=str(c2), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def store(ctx):
    dcid = str(ctx.author.id)
    if (os.path.exists("users/" + dcid + ".json") == False):
        await ctx.send(f"你尚未綁定Riot帳號 請私訊我 -login 帳號 密碼")
    else:
        await ctx.send(f"正在取得商店資料...")
        with open("users/" + dcid + ".json") as f:
            pdata = json.load(f)
        Auth.username = pdata['username']
        Auth.password = pdata['password']
        au = Auth.authenticate(Auth)
        access_token = au[0]
        user_id = au[1]
        entitlements_token = au[2]        
        print(f"access token: " + access_token)
        print(f"entitlements token: " + entitlements_token)
        print(f"user id: " + user_id)
        
        url = "https://pd.ap.a.pvp.net/store/v2/storefront/" + user_id
        payload = ""
        headers = {
            "X-Riot-Entitlements-JWT": entitlements_token,
            "Authorization": "Bearer " + access_token
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        skins = response.json()
        print(response.text)
        datas = skins['SkinsPanelLayout']['SingleItemOffers']
        count = 0
        icon = {}
        name = {}
        for weaponSkinUuid in datas:
            Uuid = weaponSkinUuid


            params = { 'language': 'zh-TW' }
            req = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{Uuid}', params = params)
            data = req.json()
            print(data['data']['displayName'])

            paramsen = { 'language': 'en-US' }
            reqen = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{Uuid}', params = paramsen)
            dataen = reqen.json()
            print(dataen['data']['displayName'])
            
            icon[count] = data['data']['displayIcon']
            name[count] = data['data']['displayName']+ " (" + dataen['data']['displayName'] + ")"
            count = count + 1
            #embed.set_image(url=icon + "")
            #embed.add_field(name=data['data']['displayName']+ " (" + dataen['data']['displayName'] + ")", value=" (" + dataen['data']['displayName'] + ")", inline=False)
        img = generate_image(name, icon)
        embed=discord.Embed(title="今日商店列表", url="https://cdn.discordapp.com/attachments/896664897046315008/946396645002727424/9LAUtPMJxhqx8H2KAv-oipyMnAwFErAUyhUwsz-aNiM.jpg", descripetion="嘿...就是你今天的槍皮uwu", color = discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/896664897046315008/946396645002727424/9LAUtPMJxhqx8H2KAv-oipyMnAwFErAUyhUwsz-aNiM.jpg")
        embed.set_image(url='attachment://store-offers.png')   
        #embed.set_footer(text="歡迎斗內")

        await ctx.send(embed=embed, file=img)

@bot.event
async def on_ready():
    print("Enable Bot!")
    
bot.run(data['token']) 
