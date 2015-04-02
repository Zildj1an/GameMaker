import msvcrt, os, sys, ctypes
try:
  import yaml
except ImportError:
  print("No tienes yaml. Descargalo aqui (el zip): -> http://pyyaml.org/wiki/PyYAML")
  print("Para instalarlo, descomprimelo y ejecuta:")
  print("setup.py install")
try:
  from colorama import init, Fore, Back, Style
except ImportError:
  print("No tienes colorama. Descargalo aqui: -> https://github.com/tartley/colorama")
  print("Para instalarlo, descomprimelo y ejecuta:")
  print("setup.py install")

init()
#FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BKGCOLOR = Fore.GREEN
print(BKGCOLOR)
if os.name != 'nt':
  print("Only for windows")
  exit();
class _CursorInfo(ctypes.Structure):
  _fields_ = [("size", ctypes.c_int),
    ("visible", ctypes.c_byte)]
def hide_cursor():
  if os.name == 'nt':
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
  elif os.name == 'posix':
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
def endGame():
  with open('saved.yml', 'w') as yaml_file:
    yaml_file.write(yaml.dump(games, default_flow_style=False))
  exit()
def getRequirementName(requirement, amount, inv=False):
  if (inv == True):
    tmp = requirement['syntaxDisplay']['inv']
  elif (amount == 1):
    tmp = requirement['syntaxDisplay']['s']
  else:
    tmp = requirement['syntaxDisplay']['p']
  return tmp.replace("$N", ("% *d" % (3,amount)))
def requirements(reqAsked, reqGot):
  for currentReq in reqAsked:#currentReq->reqAsked[currentReq]
    if (reqAsked[currentReq] > reqGot[currentReq]['amount']):
      return False, "You don't have " + getRequirementName(games['games'][currentGame]['requirements'][currentReq],reqAsked[currentReq]) + "!"
    print("To do that you need "+getRequirementName(games['games'][currentGame]['requirements'][currentReq],reqAsked[currentReq])+".\nWould you like to use it? (y/else)")
    if not (msvcrt.getch().decode("utf-8") == 'y'):
      return False, "You didn't use " + getRequirementName(games['games'][currentGame]['requirements'][currentReq],reqAsked[currentReq]) + "!"
  for currentReq in reqAsked:
    if (reqGot[currentReq]['use']):
      reqGot[currentReq]['amount'] = reqGot[currentReq]['amount'] - reqAsked[currentReq]
  return True, ""
def showReqs():
  l = 2
  msg = 'Inventory:'
  print(('\033[%d;%dH' +Fore.CYAN+ msg) % (l,99-len(msg)))
  l = l+2
  for currentRequirement in games['games'][currentGame]['requirements']:
    if ('show' in games['games'][currentGame]['requirements'][currentRequirement]):
      if (games['games'][currentGame]['requirements'][currentRequirement]['show']):
        msg = getRequirementName(games['games'][currentGame]['requirements'][currentRequirement], games['games'][currentGame]['requirements'][currentRequirement]['amount'], True)
        print(('\033[%d;%dH' +Fore.YELLOW+ msg) % (l,99-len(msg)))
        l = l+1
  print(BKGCOLOR)
hide_cursor()
os.system('mode con cols=100 lines=40')
os.system('cls')
if os.path.isfile('saved.yml'):
  f = open('saved.yml')
  print("Loading saved games...")
elif os.path.isfile('games.yml'):
  f = open('games.yml')
  print("Loading games...")
else:
  print("No files found :(")
  exit()
games = yaml.safe_load(f)
f.close()
print("Games:")
for game in games['games']:
  print("  -"+game)
print("  ->exit")
currentGame = input("Enter the game name: ")
while not (currentGame in games['games']):
   if (currentGame == "exit"):
      exit()
   currentGame = input("Enter the game name: ")
os.system('cls')
print("Welcome to: " + games['games'][currentGame]['name']+"\nDescription: " + games['games'][currentGame]['description']+"\nPress any key to start the game...")
msvcrt.getch()
currentRoom = games['games'][currentGame]['startingRoom']
previousRoom = ""
os.system('cls')
while True:
  os.system('cls')
  #if ("action" in games['games'][currentGame]['rooms'][currentRoom]):
  option = ''
  requirementsMet = False
  while not (option in games['games'][currentGame]['rooms'][currentRoom]['options']):
    print(games['games'][currentGame]['rooms'][currentRoom]['arrivalText'])
    for option in games['games'][currentGame]['rooms'][currentRoom]['options']:
      print(option+") "+games['games'][currentGame]['rooms'][currentRoom]['options'][option]['text'])
    print("\n\n\n")
    showReqs()
    option = msvcrt.getch().decode("utf-8")
    if (option == '0'):
      endGame()
    os.system('cls')
  if ('required' in games['games'][currentGame]['rooms'][currentRoom]['options'][option]):
    requirementsMet, requirementsMessage = requirements(games['games'][currentGame]['rooms'][currentRoom]['options'][option]['required'], games['games'][currentGame]['requirements'])
  else:
    requirementsMet = True
  if (requirementsMet):
    if ("action" in games['games'][currentGame]['rooms'][currentRoom]['options'][option]):
      if not (games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['repeatTimes'] == 0):
        games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['repeatTimes'] -= 1
        print(games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['text'])
        if ("items" in games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']):
          for currentItem in games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['items']:
            games['games'][currentGame]['requirements'][currentItem]['amount'] = games['games'][currentGame]['requirements'][currentItem]['amount'] + games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['items'][currentItem]
            if (games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['items'][currentItem] < 0):
              tmp = "Lost"
            else:
              tmp = "Received"
            print(" ->"+tmp+" "+getRequirementName(games['games'][currentGame]['requirements'][currentItem], games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['items'][currentItem])+"!!!")
        print("Press any key to continue...")
        msvcrt.getch()
      if ("win" in games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']):
        print(games['games'][currentGame]['rooms'][currentRoom]['options'][option]['action']['win']['text'])
        print("\n\n\nEnd of game...\n\nPress any key to continue...")
        msvcrt.getch()
        endGame()
    if ("nextRoom" in games['games'][currentGame]['rooms'][currentRoom]['options'][option]):
      previousRoom = currentRoom
      currentRoom = games['games'][currentGame]['rooms'][currentRoom]['options'][option]['nextRoom']
      games['games'][currentGame]['startingRoom'] = currentRoom
  else:
    print(requirementsMessage+"\n Press any key to continue...")
    msvcrt.getch()
endGame()


