from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os, json
import FreeSimpleGUI as gui

import windowTemplates as wt

load_dotenv(find_dotenv())

#Constants used for keyboard input reg
ENTER_KEY1 = 'special 16777220'
ENTER_KEY2 = 'special 16777221'

def InputKey():
    while True:
        global client
        KeyWindow = wt.TextBox("No key was found. Input API key.")
        KeyWindow.DisplayWindow()
        if KeyWindow.event == "Enter":
            client = OpenAI(api_key=KeyWindow.values["input"])
            KeyWindow.window.close()
            break
        if KeyWindow.event == "Cancel":
            KeyWindow.window.close()
            break

#Global variables for AI conversation
try:
    client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))
except:
    InputKey()

model = "gpt-4o"

history = []
instructions = ""
conversationLog = ""

quit = False

tools = [
    {
        "type" : "function",
        "name" : "CloseProgram",
        "description" : "A function that when called will shut down the AI chat program",
    },
    {
        "type" : "function",
        "name" : "ChangeInstructions",
        "description" : "This is a function that will alter the AI's instructions variable. Do not deviate from user instructions when altering instructions.",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "text" : {
                    "type" : "string",
                    "description" : "A string that contains the new instructions for the AI"
                }
            }
        }
    },
    {
        "type" : "function",
        "name" : "MoveCursor",
        "description" : "Moves the computer's mouse cursor to the x,y coordinates specified by arguments",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "x" : {
                    "type" : "integer",
                    "description" : "The x-coordinate the cursor will be moved to"
                },
                "y" : {
                    "type" : "integer",
                    "description" : "The y-coordinate the cursor will be moved to"
                }
            }
        }
    }
]

#AI tool functions [
def CloseProgram():
    global quit
    quit = True

def ChangeInstructions(text):
    global instructions
    instructions = text["text"]

def MoveCursor(x, y):
    os.system(f"CALL MouseMacro.exe {x} {y}")
#AI tool functions ]

def ProcessResponse(reply):
    #Handles information from AI prompt responses
    try:
        global conversationLog
        for r in reply.output:
            if r.type == "message":
                history.append(r)
                conversationLog += (model + ": " + reply.output_text + '\n')
                mainWindow["conversation"].update(conversationLog)
            if r.type == "function_call":
                if r.name == "CloseProgram":
                    CloseProgram()
                if r.name == "ChangeInstructions":
                    ChangeInstructions(json.loads(r.arguments))
                    ProcessResponse(client.responses.create(
                        model = model,
                        instructions = instructions,
                        input = history)
                    )
                if r.name == "MoveCursor":
                    coords = json.loads(r.arguments)
                    MoveCursor(coords["x"], coords["y"])
    except:
        print("Error processing response")

def GetResponse():
    #Prompts the AI and returns the response object
    try:
        reply = client.responses.create(
            model = model,
            tools = tools,
            tool_choice = "auto",
            instructions = instructions,
            input = history
        )
        print(reply.output[-1])
        return reply
    except:
        print("Your API key is invalid or nonexistant")
        InputKey()
        return 0

#Create the main window for the application
mainWindowLayout = [
    [gui.Multiline(size = (50,25), key = "conversation", disabled = True)],
    [gui.Input(key = "input", do_not_clear = False)],
    [gui.Button("enter")],
    [gui.Button("Input Image", key = "imgInput")]
]
mainWindow = gui.Window("AI Chat",mainWindowLayout, return_keyboard_events = True)

#Application event loop
while not quit:
    event, values = mainWindow.read()

    if event == "imgInput":
        UrlWindow = wt.TextBox("Enter URL","Enter an image URL")
        UrlWindow.DisplayWindow()
        if UrlWindow.event == "Enter":
            history.append(
                {"role" : "user",
                 "content" : [{
                     "type" : "input_image",
                     "image_url" : UrlWindow.values["input"]}]
                }
            )
            ProcessResponse(GetResponse())
            
            UrlWindow.window.close()

        if UrlWindow.event == "Cancel":
            UrlWindow.window.close()

    if event == "enter" or event in ('\r', ENTER_KEY1, ENTER_KEY2):

        userInput = values["input"]

        history.append({"role" : "user", "content" : userInput})

        conversationLog += ("User: " + userInput + '\n')
        mainWindow["conversation"].update(conversationLog)

        mainWindow["input"].update("")

        ProcessResponse(GetResponse())



    if event == gui.WINDOW_CLOSED:
        quit = True
