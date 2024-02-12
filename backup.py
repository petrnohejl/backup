#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Pouzite prikazy:
# "C:\Program Files (x86)\WinRAR\Rar.exe" a -t -id[c] -hpmypassword D:\test.rar D:\test - pridat a otestovat, bez rar copyright hlavicky
# "C:\Program Files (x86)\WinRAR\Rar.exe" t D:\test.rar - otestovat archiv


import os
import subprocess
import shlex
import shutil
import string
import time
import re
import getpass


# KONFIGURACE
BACKUP_LIST = "backuplist.txt"
OUTPUT_DIRECTORY = os.path.join("W:\\", "BACKUP")
WIN_RAR_PATH = os.path.join("C:\\", "Program Files", "WinRAR", "Rar.exe")


# BACKUP
class Backup():
	def __init__(self, password):
		# vytvoreni vystupniho adresare
		self.checkDirectory(OUTPUT_DIRECTORY)

		# nahrani seznamu nazvu adresaru
		backupList = self.loadBackupList(BACKUP_LIST)

		# zalohovani
		self.backup(backupList, password)


	"""
	Vytvoreni archivu pro vsechny adresare v seznamu.
	"""
	def backup(self, backupList, password):
		# datum
		date = time.strftime("%y_%m_%d", time.gmtime())

		# seznam textovych souboru s reporty
		reports = []

		# archivovani
		for dir in backupList:
			# vygenerovani nazvu archivu
			filename = self.generateName(dir, date)
			filenamefull = os.path.join(OUTPUT_DIRECTORY, filename)

			# sestaveni prikazu pro pridani do archivu
			program = '"' + WIN_RAR_PATH + '"'
			if password == "":
				passwordcommand = ""
			else:
				passwordcommand = "-hp" + password
			parametres = ' a -t -id[c] ' + passwordcommand + ' "' + filenamefull + '" "' + dir + '"'
			#parametres = ' t "' + filenamefull + '"'
			command = program + parametres
			args = shlex.split(command)
			print(self.hidePassword(command, password))

			# spusteni prikazu
			#os.system(command)
			timebefore = time.time()
			process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)

			# vystup do souboru
			reportFilename = "_" + filename + ".txt"
			reportFilenamefull = os.path.join(OUTPUT_DIRECTORY, reportFilename)
			reports.append(reportFilenamefull)
			file = open(reportFilenamefull, "w")
			file.write("--------------------------------------------------------------------------------" + "\n")
			file.write(self.hidePassword(command, password) + "\n")
			file.write("\n")

			# zpracovani vystupu
			for rawLine in iter(process.stdout.readline, b''):
				line = rawLine.decode("cp1250").rstrip()
				print(line)
				
				regexp = re.compile("^Adding .+OK$|^Testing .+OK$|^Updating .+OK$|^$")
				if not regexp.search(line):
					file.write(line + "\n")

			# statistiky
			file.write("\n")
			filesize = self.getSize(filenamefull)
			timetotal = self.getTime(time.time() - timebefore)
			file.write("Archive size: " + filesize + "\n")
			file.write("Archiving time: " + timetotal + "\n")
			file.write("--------------------------------------------------------------------------------" + "\n")
			file.close

		# souhrn vsech vysledku do souboru
		file = open(os.path.join(OUTPUT_DIRECTORY, date + "_BACKUP_REPORT.txt"), "a")
		for report in reports:
			fileRead = open(report, "r")
			shutil.copyfileobj(fileRead, file)
			fileRead.close()
		file.close()


	"""
	Overeni existence adresare a pripadne vytvoreni.
	"""
	def checkDirectory(self, directory):
		if not os.path.exists(directory):
			os.mkdir(directory)


	"""
	Nacteni seznamu adresaru z textoveho souboru.
	"""
	def loadBackupList(self, filename):
		file = open(filename, "r")
		backupList = []
		for line in file.readlines():
			path = line.strip()
			if os.path.exists(path):
				backupList.append(path)
		file.close
		return backupList


	"""
	Vygenerovani nazvu archivu.
	"""
	def generateName(self, directory, date):
		filename1 = os.path.split(directory)
		if len(filename1) > 1:
			filename2 = os.path.split(filename1[0])[1]
			if filename2 != "":
				filename2 = filename2 + "_"
		else:
			filename2 = ""
		filenameDir = filename2 + filename1[1]

		# nazev souboru
		filename = date + "_" + filenameDir + ".rar"
		return filename


	"""
	Velikost archivu.
	"""
	def getSize(self, filename):
		filesize = os.path.getsize(filename)
		if filesize >= 1073741824:
			return str(round(filesize/1073741824.0, 2)) + " GB"
		elif filesize >= 1048576:
			return str(round(filesize/1048576.0, 2)) + " MB"
		elif filesize >= 1024:
			return str(round(filesize/1024.0, 2)) + " kB"
		else:
			return str(filesize) + " B"


	"""
	Cas archivace.
	"""
	def getTime(self, seconds):
		return time.strftime("%H:%M:%S", time.gmtime(seconds))


	"""
	Skryti hesla.
	"""
	def hidePassword(self, command, password):
		cutpassword = password[1:]
		stars = len(cutpassword) * "*"
		return command.replace(cutpassword, stars)


# MAIN
if __name__ == "__main__":
	password1 = getpass.getpass("Enter password for RAR archives (empty for no password): ")
	if password1.strip() == "":
		Backup("")
	else:
		password2 = getpass.getpass("Enter password again: ")
		if password1 == password2: Backup(password1.strip())
		else: print("Passwords are different. Try again.")
