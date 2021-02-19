import os

def getRootDir():
  return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def appendDirToRootDir(path):
  return os.path.join(getRootDir(),path,'')

def appendFileToRootDir(file):
  return os.path.join(getRootDir(),file)

def appendDirToDir(dir, path):
  return os.path.join(dir,path,'')

def appendFileToDir(dir, file):
  return os.path.join(dir,file)