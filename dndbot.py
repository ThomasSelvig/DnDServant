# This code doesn't scale well but I can't be bothered to fix that
# To customize possible dices, just edit the "dices" dictionary at line 21

import discord, asyncio, json, string, re
from random import randint

TOKEN = "I will give this to you if you ask nicely"
client = discord.Client()

with open("responses.json") as fs:
	responses = json.loads(fs.read())

#dices = {
#	"D20": 20,
#	"D12": 12,
#	"D10": 10,
#	"D8": 8,
#	"D6": 6,
#	"D4": 4
#}
dices = {
	"D1": 1,
	"D2": 2,
	"D3": 3,
	"D4": 4,
	"D5": 5,
	"D6": 6,
	"D7": 7,
	"D8": 8,
	"D9": 9,
	"D10": 10,
	"D11": 11,
	"D12": 12,
	"D13": 13,
	"D14": 14,
	"D15": 15,
	"D16": 16,
	"D17": 17,
	"D18": 18,
	"D19": 19,
	"D20": 20
}

def rstripNonChars(s):
	#    "abc, "   ->   "abc"
	for i in range(1, len(s)):
		if s[-i].lower() in string.ascii_lowercase or s[-i] in string.digits:
			return s[:len(s)-(i-1)]

@client.event
async def on_message(message):
	# for the bot to not reply to itself
	if message.author == client.user:
		return None

	if re.match(r"r[0-9][dD][0-9]", message.content) or re.match(r"r[dD][0-9]", message.content):
		params = list(map(rstripNonChars, message.content.split(" ")))
		#print(params)
		throw = []

		for param in params:
			amount = 1

			if param[0] == "r":
				if param[1] in string.digits and param[2:].upper() in dices:
					# append f.e: "D20" (not "20")
					for _ in range(int(param[1])):
						throw.append(param[2:].upper())

				elif param[1:].upper() in dices:
					# append f.e: "D20" (not "20")
					throw.append(param[1:].upper())

		if len(throw) > 0:
			if randint(1, 30) == 1:
				msg = "Nei, vil ikke."
				print(f"\nShat on the kids in {message.channel.guild.name}")
			else:
				total = 0
				average = 0.0
				msg = ">>> " + responses[randint(0, len(responses)-1)].capitalize() + "!\n\n"

				for dice in throw:
					average += dices[dice] / 2 + 0.5
					val = randint(1, dices[dice])
					total += val
					msg += dice + " -->\t" + str(val) + "\n"

				if len(throw) > 1:
					avgRating = int(total * 100 // average - 100)
					msg += "\n" + str(abs(avgRating)) + "% " + ("Below" if avgRating < 0 else "Above") + " average!"
					msg += "\nSum: \t" + str(total) + "\t\t"

				print(f"\n[{message.channel.guild.name}:{message.channel.name}] {message.author.mention} {message.author.name}: {message.content}")
				print(f"Did {len(throw)} roll"+ "s" if len(throw) > 1 else "")
			
			await message.channel.send(msg)
		else:
			return None


@client.event
async def on_ready():
	print("Username: ", end = "")
	print(client.user.name)
	print("UserID: ", end = "")
	print(client.user.id)

client.run(TOKEN)
