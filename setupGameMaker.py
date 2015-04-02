import urllib.request, zipfile, os, subprocess, sys, shutil

def downloadFile(url, fileName):
  response = urllib.request.urlopen(url)
  
  output = open(fileName,'wb')
  output.write(response.read())
  output.close()
def zipExtract(file, extension):
  with zipfile.ZipFile(file+"."+extension, "r") as z:
      z.extractall(os.getcwd()+"/")
dir = "GameMaker"
if not os.path.exists(dir):
  os.makedirs(dir)
os.chdir(os.getcwd()+"/"+dir+"/")

try:
  import colorama
  print ("Ya tienes colorama")
except ImportError:
  libsDir = "libs"
  if not os.path.exists(dir):
    os.makedirs(dir)
  os.chdir(os.getcwd()+"/"+libsDir+"/")
  print("Obteniendo libreria: colorama")
  downloadFile("https://github.com/tartley/colorama/archive/master.zip", "colorama.zip")
  print("Extrayendo libreria: colorama")
  zipExtract("colorama", "zip")
  print("Instalando libreria: colorama")
  os.chdir(rPath+"/colorama-master/")
  os.system('setup.py install>nul')
  os.chdir("../../")

try:
  import yaml
  print ("Ya tienes yaml")
except ImportError:
  libsDir = "libs"
  if not os.path.exists(dir):
    os.makedirs(dir)
  os.chdir(os.getcwd()+"/"+libsDir+"/")
  print("Obteniendo libreria: yaml")
  downloadFile("http://pyyaml.org/download/pyyaml/PyYAML-3.11.zip", "yaml.zip")
  print("Extrayendo libreria: yaml")
  zipExtract("yaml", "zip")
  print("Instalando libreria: yaml")
  os.chdir(rPath+"/PyYAML-3.11/")
  os.system('setup.py install>nul')
  os.chdir("../../")
libsDir = "libs"
if os.path.exists(dir):
  shutil.rmtree(dir)
appFolder = os.getenv('APPDATA').replace("\\", "/")+"/.GameMaker"
launcherText = "import os,sys\nos.chdir(\""+appFolder+"\")\nos.system(\""+appFolder+"/GameMaker.py\")"
with open('launcher.py', 'w') as the_file:
  the_file.write(launcherText)

if not os.path.exists(appFolder):
  os.makedirs(appFolder)
os.chdir(appFolder)
print("Obteniendo GameMaker.py")
downloadFile("http://devpgsv.hol.es/AS/GameMaker/GameMaker.py", "GameMaker.py")
print("Obteniendo games.yaml")
downloadFile("http://devpgsv.hol.es/AS/GameMaker/games.yml", "games.yml")

print("\n\nYa!!! :) Entra en la carpeta GameMaker, y ejecuta launcher.py")
input("")