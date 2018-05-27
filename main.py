# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMessageBox, QScrollArea, QGroupBox, QComboBox, QDateEdit, QCalendarWidget, QWidget, QApplication, QStackedLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QDate
from api import *


class Principale(QWidget):
	def __init__(self):
		super(Principale, self).__init__()
		self.setUI()
	
	def setUI(self):

		labelVille = QLabel("Ville : ")
		labelJour = QLabel("Jour : ")
		textEditVille = QLineEdit()
		calendarJour = QDateEdit()
		calendarJour.setCalendarPopup(True)
		calendarJour.setDate(QDate.currentDate())
		buttonValiderParam = QPushButton("Valider")

		hboxParam = QHBoxLayout()
		vboxGlobal = QVBoxLayout()

		hboxParam.addWidget(labelVille)
		hboxParam.addWidget(textEditVille)
		hboxParam.addWidget(labelJour)
		hboxParam.addWidget(calendarJour)
		hboxParam.addWidget(buttonValiderParam)

		vboxGlobal.addLayout(hboxParam)


		self.setLayout(vboxGlobal)
		
		buttonValiderParam.clicked.connect(lambda: self.validerParam(textEditVille.text(), calendarJour.date()))

		self.setWindowTitle('Super Cinemon 2000 ExtraPlus')
		
		self.show()

	def validerParam(self, ville, jour):
		year = jour.year()
		month = jour.month()
		day = jour.day()

		if month < 10:
			jourCine = str(year) + '-' + '0' + str(month) + '-' + str(day)

		else:
			jourCine = str(year) + '-' + str(month) + '-' + str(day)
		CP, listeCine, codeRetour = cityDesc(ville)

		if codeRetour == 100:
			cleanLayout(self.layout())
			dicoHoraires = dict()

			for cine in listeCine:
				seanceVille = showtimeInTheater(cine['code'], jourCine)

				if 'movieShowtimes' in seanceVille['theaterShowtimes'][0]:

					for film in seanceVille['theaterShowtimes'][0]['movieShowtimes']:
						# print(film['onShow']['movie']['title'])
						for seance in film['scr']:
							if seance['d'] == jourCine:
								for occurSeance in seance['t']:

									if not (film['onShow']['movie']['title'] in dicoHoraires):
										dicoHoraires[film['onShow']['movie']['title']] = []
										dicoHoraires[film['onShow']['movie']['title']].append(dict())
										dicoHoraires[film['onShow']['movie']['title']][-1]['salle'] = cine['name']
										dicoHoraires[film['onShow']['movie']['title']][-1]['code'] = cine['code']
										dicoHoraires[film['onShow']['movie']['title']][-1]['horaire'] = occurSeance['$']
									else:
										dicoHoraires[film['onShow']['movie']['title']].append(dict())
										dicoHoraires[film['onShow']['movie']['title']][-1]['salle'] = cine['name']
										dicoHoraires[film['onShow']['movie']['title']][-1]['code'] = cine['code']
										dicoHoraires[film['onShow']['movie']['title']][-1]['horaire'] = occurSeance['$']
			
					scrollAreaSeance = QScrollArea()
					groupBoxSeances = QGroupBox()
					vboxSeances = QVBoxLayout()

					for film in dicoHoraires:
						dicoHoraires[film] = sorted(dicoHoraires[film], key=lambda t:t['horaire'])
						groupBoxHoraire = QGroupBox(film)
						vboxHor = QVBoxLayout()
						for hor in dicoHoraires[film]:
							vboxHor.addWidget(QLabel(hor['salle'] + ' : ' + hor['horaire']))
						groupBoxHoraire.setLayout(vboxHor)
						vboxSeances.addWidget(groupBoxHoraire)
					groupBoxSeances.setLayout(vboxSeances)
					scrollAreaSeance.setWidget(groupBoxSeances)
					self.layout().addWidget(scrollAreaSeance)
				else:
					errorLabel = QLabel('Pas de seance a ' + ville + ' le ' + jourCine + '.')
					self.layout().addWidget(errorLabel)

		elif codeRetour == 200:
			cleanLayout(self.layout())
			errorMessageBox = QMessageBox()
			errorMessageBox.critical(self, 'Erreur : connexion impossible', 'Allocine ne repond pas correctement. \nCauses possibles : \nProtocole de connexion à l\'API modifie \nSite temporairement inaccessible \nSite definitivement inaccessible (pas de pot)')

		elif codeRetour == 300:
			cleanLayout(self.layout())
			errorLabel = QLabel("Il n'y a pas de salle de cinema referencees a " + ville)
			self.layout().addWidget(errorLabel)

		elif codeRetour == 400:
			cleanLayout(self.layout())
			errorLabel = QLabel("La ville " + ville + " n'est pas referencee, etes-vous certain de l'orthographe ?")
			self.layout().addWidget(errorLabel)

def cleanLayout(layout):
	for i in reversed(range(layout.count())): 
		widgetToRemove = layout.itemAt( i ).widget()
		if widgetToRemove:
			# remove it from the layout list
			layout.removeWidget( widgetToRemove )
			# remove it from the gui
			widgetToRemove.setParent( None )

monApp=QApplication(sys.argv)
fenetre=Principale()
sys.exit(monApp.exec_())
