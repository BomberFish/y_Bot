#! /usr/bin/python3
import discord
from fractions import Fraction
import json
import math

class Command:
    def __init__(self, command, cmdhelp, argnum):
        self.command = command
        self.cmdhelp = cmdhelp
        self.argnum = argnum

class Y_Bot_Exception(Exception):
    pass

cmd_list = [Command("ping", "pong", 0), Command("pong", "ping", 0), Command("conv", "calculate a linear equation", 2), Command("help", "gives you help", 0), Command("morse", "Convert morse to text and vice-versa", 1), Command("echo", "Echoes text to you", 1), Command("be-a-robot", "uhhhh", 0), Command("uncringe", "Obliterate Cringe", 0), Command("scale", "Create an equal-tempered or pythagorean scale", 2)]
# SEP 11 2021 @ 19:09:30
# the_list_of_commands = [Command("ping", "pong", 0), Command("pong", "ping", 0), Command("conv", "calculate a linear equation", 2), Command("help", "gives you help", 0), Command("pin", "test the automatic abbreviations", 0), Command("morse", "convert morse to text and vice-versa", 1)]

def parse_command(command, allow_abbreviations=True):
    pairlist = cmd_list[:]
    if allow_abbreviations:
        i = 0
        while i < len(command.command):
            j = 0
            while j < len(pairlist):
                if (len(pairlist[j].command) > i and pairlist[j].command[i] != command.command[i]) or len(pairlist[j].command) <= i:
                    del pairlist[j]
                    j -= 1
                j += 1
            i += 1
            
        if len(pairlist) == 1:
            return pairlist[0]
        elif len(pairlist) == 0:
            raise Y_Bot_Exception(f"Command not found: {command.command}")
        else:
            for x in pairlist:
                if x.command == command.command:
                    return x
            raise Y_Bot_Exception(f"Ambiguous command \"{command.command}\"", f"possibilities are: {', '.join([x.command for x in pairlist])}")

async def do_command(command, message, the_rest_of_the_command):
    if command.command == "ping":
        await message.channel.send("pong")
    elif command.command == "pong":
        await message.channel.send("ping")
    elif command.command == "conv":
        the_rest_of_the_command = the_rest_of_the_command.split()
        if len(the_rest_of_the_command) < command.argnum:
            raise Y_Bot_Exception(f"Not enough arguments provided for command: {command.command}")
        the_strings_in_the_rest_of_the_command_that_actually_matter = the_rest_of_the_command[:min(len(the_rest_of_the_command), 3)]
        the_three_ratios = [Fraction(x) for x in the_strings_in_the_rest_of_the_command_that_actually_matter]
        if len(the_rest_of_the_command) == 2:
            the_three_ratios.append(Fraction())
        if len(the_rest_of_the_command) == 4:
            should_it_be_a_float = True
        else:
            should_it_be_a_float = False;
        the_linear_equation = the_three_ratios[0] * the_three_ratios[1] + the_three_ratios[2]
        await message.channel.send(str(the_linear_equation) if not should_it_be_a_float else str(float(the_linear_equation)))
    elif command.command == "help":
        pairlist = cmd_list[:]
        await message.channel.send(embed=discord.Embed(title=f"Commands are:", color=0x57f287, description={', '.join([x.command for x in pairlist])}))
    elif command.command == "":
        await message.channel.send(embed=discord.Embed(title=f"Error", color=0xed4245, description="You didn't pass any commands to me!"))
    elif command.command == "uncringe":
        await message.channel.send("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    elif command.command == "morse":
        the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
        for x in the_rest_of_the_command:
            for y in x:
                if y == "":
                    raise Y_Bot_Exception(f"Found empty word")
        the_message_to_send = ""
        morse = {".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9"}
        for x in the_rest_of_the_command:
            for y in x:
                the_message_to_send += morse[y] if y in morse else y
            the_message_to_send += " "
        await message.channel.send(the_message_to_send)
    elif command.command == "scale":
         the_rest_of_the_command = the_rest_of_the_command.split()
         if len(the_rest_of_the_command) < command.the_number_of_arguments_the_command_takes:
             raise Y_Bot_Exception(f"Not enough arguments provided for command: {command.command}")
         if the_rest_of_the_command[0] == "et":
             embed = discord.Embed(title=f"{the_rest_of_the_command[1]}-tone equal-tempered scale made on the pitch {the_rest_of_the_command[2]}", color=0x57f287)
             for x in range(int(the_rest_of_the_command[1])):
                 if (x % 25 == 1) and (x != 1):
                     await message.channel.send(embed=embed)
                     embed = discord.Embed(title=f"{the_rest_of_the_command[1]}-tone equal-tempered scale made on the pitch {the_rest_of_the_command[2]} (continued)", color=0x57f287)
                 embed.add_field(name=f"Tone {x}:", value=f"{(2**Fraction(x/int(the_rest_of_the_command[1])))*Fraction(the_rest_of_the_command[2])}", inline=False)
             await message.channel.send(embed=embed)
         elif the_rest_of_the_command[0] == "pythagorean":
             ratios = []
             embed = discord.Embed(title=f"Pythagorean scale made on the pitch {the_rest_of_the_command[1]}", color=0x57f287)
             for x in range(6):
                 ratios.append(((Fraction(3,2) ** x) * Fraction(the_rest_of_the_command[1])) / 2 ** (math.floor(math.log2((Fraction(3,2) ** x) * Fraction(the_rest_of_the_command[1])))))
             for x in range(1, 7):
                 ratios.append(Fraction((Fraction(2,3) ** x) * Fraction(the_rest_of_the_command[1]), 2 ** Fraction(math.floor(math.log2((Fraction(2,3) ** x) * Fraction(the_rest_of_the_command[1]))))))
             [embed.add_field(name=f"Tone {sorted(ratios).index(x)}:", value=f"{x}", inline=False) for x in sorted(ratios)]
             await message.channel.send(embed=embed)
    elif command.command == "echo":
        the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
        thing_to_echo = json.dumps(the_rest_of_the_command, separators=(',', ':'))
        #print(thing_to_echo)
        await message.channel.send(thing_to_echo)
    # elif command.command == "add":
    #     the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
    #     the_other_thing_to_add = [x.split(" ") for x in the_rest_of_the_command.split("/")]
    #     print(the_rest_of_the_command)
    #     await message.channel.send(the_rest_of_the_command)
    elif command.command == "be-a-robot":
        raise Y_Bot_Exception(f"Resistance is Futile.")

class Y_Bot(discord.Client):
    async def on_ready(self):
        print(f"Succesfully logged in as {self.user}!")
    async def on_message(self, message):
        
        if message.content[0:3] == "yb;":
            the_command_without_start = message.content[3:].split()[0] if len(message.content[3:]) != 0 else ""
            the_rest_of_the_command = ' '.join(message.content[3:].split()[1:]) if len(message.content[3:].split()) > 1 else ""
            #print(the_command_without_start)
            try:
                await do_command(parse_command(Command(the_command_without_start, "", -1)), message, the_rest_of_the_command)
            except Y_Bot_Exception as y:
                embed = discord.Embed(title=y.args[0], description="You made an error" if len(y.args) == 1 else y.args[1], color=0xed4245)
                await message.channel.send(embed=embed)

y_Bot = Y_Bot()
with open("auth") as auth:
    token = auth.read()[:-1]
    y_Bot.run(token)
