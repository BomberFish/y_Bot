#! /usr/bin/python3
import discord
from fractions import Fraction

class Command:
    def __init__(self, command, the_help_for_the_command, the_number_of_arguments_the_command_takes):
        self.command = command
        self.the_help_for_the_command = the_help_for_the_command
        self.the_number_of_arguments_the_command_takes = the_number_of_arguments_the_command_takes

class Y_Bot_Exception(Exception):
    pass

the_list_of_commands = [Command("ping", "pong", 0), Command("pong", "ping", 0), Command("conv", "calculate a linear equation", 2), Command("help", "gives you help", 0), Command("morse", "convert morse to text and vice-versa", 1)]
# SEP 11 2021 @ 19:09:30
# the_list_of_commands = [Command("ping", "pong", 0), Command("pong", "ping", 0), Command("conv", "calculate a linear equation", 2), Command("help", "gives you help", 0), Command("pin", "test the automatic abbreviations", 0), Command("morse", "convert morse to text and vice-versa", 1)]

def parse_command(command, allow_abbreviations=True):
    the_list_that_we_pair_down = the_list_of_commands[:]
    if allow_abbreviations:
        i = 0
        while i < len(command.command):
            j = 0
            while j < len(the_list_that_we_pair_down):
                if (len(the_list_that_we_pair_down[j].command) > i and the_list_that_we_pair_down[j].command[i] != command.command[i]) or len(the_list_that_we_pair_down[j].command) <= i:
                    del the_list_that_we_pair_down[j]
                    j -= 1
                j += 1
            i += 1
            
        if len(the_list_that_we_pair_down) == 1:
            return the_list_that_we_pair_down[0]
        elif len(the_list_that_we_pair_down) == 0:
            raise Y_Bot_Exception(f"Command not found: {command.command}")
        else:
            for x in the_list_that_we_pair_down:
                if x.command == command.command:
                    return x
            raise Y_Bot_Exception(f"Ambiguous command \"{command.command}\"", f"possibilities are: {', '.join([x.command for x in the_list_that_we_pair_down])}")

async def do_command(command, message, the_rest_of_the_command):
    if command.command == "ping":
        await message.channel.send("pong")
    elif command.command == "pong":
        await message.channel.send("ping")
    elif command.command == "conv":
        the_rest_of_the_command = the_rest_of_the_command.split()
        if len(the_rest_of_the_command) < command.the_number_of_arguments_the_command_takes:
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
        the_list_that_we_pair_down = the_list_of_commands[:]
        await message.channel.send(embed=discord.Embed(title=f"Commands are:", color=0x00ff88, description={', '.join([x.command for x in the_list_that_we_pair_down])}))
    elif command.command == "":
        await message.channel.send(embed=discord.Embed(title=f"Whoops!", color=0xff0000, description="You didn't pass any commands to me!"))
    # elif command.command == "pin":
    #     await message.channel.send("pon")
    elif command.command == "morse":
        the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
        print(the_rest_of_the_command)
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
    elif command.command == "echo":
        the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
        print(the_rest_of_the_command)
        await message.channel.send(the_rest_of_the_command)
    # elif command.command == "add":
    #     the_rest_of_the_command = [x.split(" ") for x in the_rest_of_the_command.split("/")]
    #     the_other_thing_to_add = [x.split(" ") for x in the_rest_of_the_command.split("/")]
    #     print(the_rest_of_the_command)
    #     await message.channel.send(the_rest_of_the_command)

class Y_Bot(discord.Client):
    async def on_ready(self):
        print(f"Succesfully logged in as {self.user}!")
    async def on_message(self, message):
        
        if message.content[0:3] == "yb;":
            the_command_without_start = message.content[3:].split()[0] if len(message.content[3:]) != 0 else ""
            the_rest_of_the_command = ' '.join(message.content[3:].split()[1:]) if len(message.content[3:].split()) > 1 else ""
            print(the_command_without_start)
            try:
                await do_command(parse_command(Command(the_command_without_start, "", -1)), message, the_rest_of_the_command)
            except Y_Bot_Exception as y:
                embed = discord.Embed(title=y.args[0], description="You made an error" if len(y.args) == 1 else y.args[1], color=0xff0000)
                await message.channel.send(embed=embed)

y_Bot = Y_Bot()
with open("auth") as auth:
    token = auth.read()[:-1]
    y_Bot.run(token)
