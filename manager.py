import discord
import json
import asyncio
import os
import openpyxl
import time

with open("users.json", "r") as json_f:
    json_datas = json.load(json_f)
print(json_datas)

f = open('users.json', 'w')
with open("users.json", "w") as json_f:
    json.dump(json_datas,json_f,indent="    ")

client = discord.Client()

@client.event
async def on_ready():

    print("=========================")
    print("다음으로 로그인 합니다 : ")
    print(client.user.name)
    print("로그인 성공!")
    game = discord.Game("관리 도우미")
    print("=========================")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    lvlist=[0,20,40,90,160,250,720,490,640,810,2000,1210,1440,1690,3920,2250,2560,2890,6480,3610,8000]
    chsCh=client.get_channel(703055017359179908)
    upgCh=client.get_channel(703064424583528599)
    xpget = 0
    if message.author.bot:
        return None

    global json_datas
    with open("users.json", "r") as json_f:
        json_datas = json.load(json_f)
    print(json_datas)
    id = str(message.author.id)
    if message.author == client.user:
        return
    if message.channel == chsCh:
        if message.content.split()[0]=="!출첵":
            xpget += 10
            print(json_datas.get(id).get('login'))
            if json_datas.get(id).get('login') == None:
                json_datas.get(id)['login'] = 1
            else:
                json_datas.get(id)['login'] += 1
            if json_datas.get(id).get('lastLogined') == None:
                json_datas.get(id)['lastLogined'] = -1
            if json_datas.get(id).get('lastLogined') == 6:
                if time.localtime().tm_wday == 0:
                    json_datas.get(id)['lastLogined'] = -1
                    if json_datas.get(id)['login'] == 7:
                        await message.channel.send("%s님, 지난 주 출석 체크 7회로 보너스 10 exp가 지급됩니다." % (message.author.mention))
                        xpget += 10
            if json_datas.get(id).get('lastLogined') < time.localtime().tm_wday:
                await message.channel.send("%s님 %s요일 출석 체크 되었습니다. (%d회)" % (message.author.mention,['월','화','수','목','금','토','일'][time.localtime().tm_wday],json_datas.get(id)['login']))
                json_datas.get(id)['lastLogined'] = time.localtime().tm_wday
            else:
                await message.channel.send("%s님, 출석 체크는 하루에 한 번만 가능합니다." % (message.author.mention))
                json_datas.get(id)['lastLogined'] = time.localtime().tm_wday

    if True:
        if json_datas.get(id) == None:
            json_datas[id] = {"xp":0,"lvl":0}
            with open("users.json", "w") as json_f:
                json.dump(json_datas,json_f,indent="    ")
        else:
            authorData = dict(json_datas.get(id))
            authorData['xp'] += 0.1
            authorData['xp'] += xpget
            xp = authorData.get("xp")
            lvl = authorData.get("lvl")
            if lvlist[lvl] < xp:
                authorData['xp'] = 0
                authorData['lvl'] += 1
                await message.channel.send('%s님, 레벨이 오르셨습니다! 축하드려요!\n현재 레벨 : %d '% (message.author.mention,authorData["lvl"]))
            json_datas[id] = authorData
            with open("users.json", "w") as json_f:
                json.dump(json_datas,json_f,indent="    ")


            #해당 라인부터는 레벨 변수에 따른 역할 지급입니다. 건들지 말아주세요

            if authorData['lvl'] == 0:
                role = discord.utils.get(message.guild.roles, name="LV 0 - 여행자")
                await message.author.add_roles(role)
                
            if authorData['lvl'] == 1:
                role = discord.utils.get(message.guild.roles, name="LV 1 - 방문객 I")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 0 - 여행자")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 2:
                role = discord.utils.get(message.guild.roles, name="LV 2 - 방문객 II")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 1 - 방문객 I")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 3:
                role = discord.utils.get(message.guild.roles, name="LV 3 - 방문객 III")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 2 - 방문객 II")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 4:
                role = discord.utils.get(message.guild.roles, name="LV 4 - 방문객 IV")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 3 - 방문객 III")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 5:
                role = discord.utils.get(message.guild.roles, name="LV 5 - 방문객 V")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 4 - 방문객 IV")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 6:
                role = discord.utils.get(message.guild.roles, name="LV 6 - 이용객 I")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 5 - 방문객 V")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 7:
                role = discord.utils.get(message.guild.roles, name="LV 7 - 이용객 II")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 6 - 이용객 I")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 8:
                role = discord.utils.get(message.guild.roles, name="LV 8 - 이용객 III")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 7 - 이용객 II")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 9:
                role = discord.utils.get(message.guild.roles, name="LV 9 - 이용객 IV")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 8 - 이용객 III")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 10:
                role = discord.utils.get(message.guild.roles, name="LV 10 - 투숙객 I")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 9 - 이용객 IV")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 11:
                role = discord.utils.get(message.guild.roles, name="LV 11 - 투숙객 II")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 10 - 투숙객 I")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 12:
                role = discord.utils.get(message.guild.roles, name="LV 12 - 투숙객 III")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 11 - 투숙객 II")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 13:
                role = discord.utils.get(message.guild.roles, name="LV 13 - 투숙객 IV")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 12 - 투숙객 III")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 14:
                role = discord.utils.get(message.guild.roles, name="LV 14 - 단골 I")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 13 - 투숙객 IV")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 15:
                role = discord.utils.get(message.guild.roles, name="LV 15 - 단골 II")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 14 - 단골 I")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 16:
                role = discord.utils.get(message.guild.roles, name="LV 16 - 단골 III")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 15 - 단골 II")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 17:
                role = discord.utils.get(message.guild.roles, name="LV 17 - 단골 IV")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 16 - 단골 III")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 18:
                role = discord.utils.get(message.guild.roles, name="LV 18 - 거주자 I")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 17 - 단골 IV")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 19:
                role = discord.utils.get(message.guild.roles, name="LV 19 - 거주자 II")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 18 - 거주자 I")
                await message.author.remove_roles(role)

            if authorData['lvl'] == 20:
                role = discord.utils.get(message.guild.roles, name="LV 20 - 거주자 III")
                await message.author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="LV 19 - 거주자 II")
                await message.author.remove_roles(role)


        #role = discord.utils.get(message.guild.roles, name="지울역할") (이거 역할 구문 외울려고 써놓은거 구문포함X)
        #await message.author.remove_roles(role)
        #role = discord.utils.get(message.guild.roles, name="줄 역할)
        #await message.author.add_roles(role)

            
        if message.content.startswith('!투표'):
            await message.delete()
            qjsgh = 0
            vote = message.content[4:].split("/")
            embed = discord.Embed(title='주제 - [' + vote[0] + ']', color=0x62c1cc)
            for i in range(1, len(vote)):
                qjsgh += 1
                embed.add_field(name=qjsgh, value=vote[i], inline=False)
            choose = await message.channel.send(embed=embed)
            qjsgh = 0
            for i in range(1, len(vote)):
                qjsgh += 1
                if qjsgh == 1:
                    await choose.add_reaction('1️⃣')
                else:
                    if qjsgh == 2:
                        await choose.add_reaction('2️⃣')
                    else:
                        if qjsgh == 3:
                            await choose.add_reaction('3️⃣')
                        else:
                            if qjsgh == 4:
                                await choose.add_reaction('4️⃣')
                            else:    
                                if qjsgh == 5:
                                    await choose.add_reaction('5️⃣')
                                else:    
                                    if qjsgh == 6:
                                        await choose.add_reaction('6️⃣')
                                    else:
                                        if qjsgh == 7:
                                            await choose.add_reaction('7️⃣')
                                        else:
                                            if qjsgh == 8:
                                                await choose.add_reaction('8️⃣')
                                            else:
                                                if qjsgh == 9:
                                                    await choose.add_reaction('9️⃣')
                                                else:    
                                                    if qjsgh == 10:
                                                        await choose.add_reaction('🔟')
                                                    else:
                                                        await choose.add_reaction('🔢')
                                                                                            			
														
        if message.content.startswith('!경고') :
            author = message.guild.get_member(message.mentions[0].id)            
            file = openpyxl.load_workbook('경고.xlsx')
            sheet = file.active
            why = str(message.content[28:])
            i = 1
            while True :
                if sheet["A" + str(i)].value == str(author) :
                    sheet['B' + str(i)].value = int(sheet["B" + str(i)].value) + 1
                    file.save("경고.xlsx")
                    if sheet["B" + str(i)].value == 5:
                        await message.guild.ban(author)
                        await message.channel.send(str(author) + "님은 경고 5회누적으로 서버에서 추방되었습니다!") 
                    if sheet["B" + str(i)].value == 2:
                        await message.channel.send(str(author) + "님, 경고를 2회 받았습니다. 5회 누적시 서버에서 차단되오니 유의하여 주시기 바랍니다.")
                        sheet["c" + str(i)].value = why
                    if sheet["B" + str(i)].value == 3:
                        await message.channel.send(str(author) + "님, 경고를 3회 받았습니다. 5회 누적시 서버에서 차단되오니 유의하여 주시기 바랍니다.")
                        sheet["c" + str(i)].value = why
                    if sheet["B" + str(i)].value == 4:
                        await message.channel.send(str(author) + "님, 경고를 4회 받았습니다. 재차 경고 누적 시 서버에서 차단되오니 유의하여 주시기 바랍니다.")
                        sheet["c" + str(i)].value = why
                    break
                
                if sheet["A" + str(i)].value == None:
                    sheet["A" + str(i)].value = str(author)
                    sheet["B" + str(i)].value = 1
                    sheet["c" + str(i)].value = why
                    file.save("경고.xlsx")
                    await message.channel.send(str(author) + "님, 경고를 1회 받았습니다. 5회 누적시 서버에서 차단되오니 유의하여 주시기 바랍니다.")
                    break
                i += 1

        #role = discord.utils.get(message.guild.roles, name="지울역할") (이거 역할 구문 외울려고 써놓은거 구문포함X)
        #await message.author.remove_roles(role)
        #role = discord.utils.get(message.guild.roles, name="줄 역할)
        #await message.author.add_roles(role)

        if message.content.startswith("!뮤트"):
            author = message.guild.get_member(message.mentions[0].id)
            role = discord.utils.get(message.guild.roles, name="뮤트")
            await author .add_roles(role)

        if message.content.startswith("!언뮤트"):
            author = message.guild.get_member(message.mentions[0].id)
            role = discord.utils.get(message.
            guild.roles, name="뮤트")
            await author .remove_roles(role)


     


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
