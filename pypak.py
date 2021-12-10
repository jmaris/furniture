#!/usr/bin/env python 
import subprocess
import pickle

class PyPak_Package:
    def __init__(self, packageString):
        pkgarray=packageString.decode('UTF-8').replace('\xa0','').split('\t')
        self.title=pkgarray[0]
        self.description=pkgarray[1]
        self.id=pkgarray[2]
        self.version=pkgarray[3]
        self.repository=pkgarray[4]
        self.runtime=pkgarray[5]
        self.size={"installed":pkgarray[6], "download":pkgarray[7]}
        self.branch=pkgarray[8]
        
    def install(self):
        try:
            print("Installing "+self.title)
            print("running command: flatpak --noninteractive -y install "+self.repository+" "+self.id+'//'+self.branch)
            subprocess.check_output(['flatpak', '--noninteractive', '-y', 'install', self.repository, self.id+'//'+self.branch])
            print("Install Successful")
        except:
            print("Error")
    def uninstall(self):
        try:
            print("Unnstalling "+self.title)
            print("running command: flatpak --noninteractive -y remove "+self.id+'//'+self.branch)
            subprocess.check_output(['flatpak', '--noninteractive', '-y', 'remove', self.id+'//'+self.branch])
            print("Uninistall Successful")
        except:
            print("Error")
        
class PyPak:
    def __init__(self, database):
        self.database=database
        try:
            with open(database, 'rb+') as pickle_file:
                self.db=pickle.load(pickle_file)
        except:
            print("Error reading database, refreshing...")
            self.db=""
            self.reload_database()
            with open(database, 'wb+') as pickle_file:
                pickle.dump(self.db, pickle_file)
                
    def update(self):
        rawdb=subprocess.check_output(['flatpak', 'remote-ls', '--columns=name:f,description:f,application:f,version:f,origin:f,runtime:f,installed-size:f,download-size:f,branch:f']).splitlines()
        newdb=[]
        for package in rawdb:
            newdb.append(PyPak_Package(package))
        self.db=newdb
        with open(self.database, 'wb+') as pickle_file:
            pickle.dump(self.db, pickle_file)
            print("Database Updated")
        
    def search(self,query,searchdescription=False):
        if searchdescription==True:
            return [package for package in self.db if query in package.title or query in package.description] #modify this to make it also search description
        else:
            return [package for package in self.db if query in package.title]
