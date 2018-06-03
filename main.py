# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QSplitter, QMessageBox, QScrollArea, QGroupBox, QComboBox, QDateEdit, QCalendarWidget, QWidget, QApplication, QStackedLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
import api


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
		hboxResultats = QHBoxLayout()
		vboxGlobal = QVBoxLayout()

		splitterRes = QSplitter()
		splitterRes.setOrientation(Qt.Horizontal)

		hboxParam.addWidget(labelVille)
		hboxParam.addWidget(textEditVille)
		hboxParam.addWidget(labelJour)
		hboxParam.addWidget(calendarJour)
		hboxParam.addWidget(buttonValiderParam)
 
		vboxGlobal.addLayout(hboxParam)
		# vboxGlobal.addLayout(hboxResultats)
		vboxGlobal.addWidget(splitterRes)


		self.setLayout(vboxGlobal)
		
		buttonValiderParam.clicked.connect(lambda: self.validerParam(textEditVille.text(), calendarJour.date()))

		self.setWindowTitle('Super Cinemon 2000 ExtraPlus')
		
		self.show()


	def validerParam(self, ville, jour):
		year = jour.year()
		month = jour.month()
		day = jour.day()

		if month < 10:
			strMonth = '0' + str(month)
		else:
			strMonth = str(month)
		if day < 10:
			strDay = '0' + str(day)
		else:
			strDay = str(day)
		jourCine = str(year) + '-' + strMonth + '-' + strDay
		CP, listeCine, codeRetour = api.cityDesc(ville)

		if codeRetour == 100:
			cleanLayout(self.layout())
			dicoHoraires = dict()
			dicoCodeFilm = dict()

			scrollAreaSeance = QScrollArea()
			groupBoxSeances = QGroupBox()
			vboxSeances = QVBoxLayout()

			# print(listeCine)


			for cine in listeCine:
				seanceVille = api.showtimeInTheater(cine['code'], jourCine)

				if 'movieShowtimes' in seanceVille['theaterShowtimes'][0]:

					for film in seanceVille['theaterShowtimes'][0]['movieShowtimes']:
						for seance in film['scr']:
							if seance['d'] == jourCine:
								for occurSeance in seance['t']:

									if not (film['onShow']['movie']['title'] in dicoHoraires):
										dicoHoraires[film['onShow']['movie']['title']] = []
										dicoHoraires[film['onShow']['movie']['title']].append(dict())
										dicoHoraires[film['onShow']['movie']['title']][-1]['salle'] = cine['name']
										dicoHoraires[film['onShow']['movie']['title']][-1]['code'] = cine['code']
										dicoHoraires[film['onShow']['movie']['title']][-1]['horaire'] = occurSeance['$']
										dicoCodeFilm[film['onShow']['movie']['title']] = film['onShow']['movie']['code']
									else:
										dicoHoraires[film['onShow']['movie']['title']].append(dict())
										dicoHoraires[film['onShow']['movie']['title']][-1]['salle'] = cine['name']
										dicoHoraires[film['onShow']['movie']['title']][-1]['code'] = cine['code']
										dicoHoraires[film['onShow']['movie']['title']][-1]['horaire'] = occurSeance['$']
						
			
					
			for film in dicoHoraires:
				dicoHoraires[film] = sorted(dicoHoraires[film], key=lambda t:t['horaire'])
				groupBoxHoraire = QGroupBox(film)
				vboxHor = QVBoxLayout()
				buttonInfoFilm = QPushButton("Informations sur le film")
				vboxHor.addWidget(buttonInfoFilm)
				buttonInfoFilm.clicked.connect(self.create_connect(dicoCodeFilm[film]))
				for hor in dicoHoraires[film]:
					vboxHor.addWidget(QLabel(hor['salle'] + ' : ' + hor['horaire']))
				groupBoxHoraire.setLayout(vboxHor)
				vboxSeances.addWidget(groupBoxHoraire)
					
			groupBoxSeances.setLayout(vboxSeances)
			scrollAreaSeance.setWidget(groupBoxSeances)
			self.layout().itemAt(1).widget().addWidget(scrollAreaSeance)

		elif codeRetour == 200:
			cleanLayout(self.layout())
			errorMessageBox = QMessageBox()
			errorMessageBox.critical(self, 'Erreur : connexion impossible', 'Allocine ne repond pas correctement. \nCauses possibles : \nProtocole de connexion à l\'API modifie \nSite temporairement inaccessible \nSite definitivement inaccessible (pas de pot)')

		elif codeRetour == 300:
			cleanLayout(self.layout())
			errorLabel = QLabel("Il n'y a pas de salle de cinema referencees a " + ville)
			self.layout().itemAt(1).widget().addWidget(errorLabel)

		elif codeRetour == 400:
			cleanLayout(self.layout())
			errorLabel = QLabel("La ville " + ville + " n'est pas referencee, etes-vous certain de l'orthographe ?")
			self.layout().itemAt(1).widget().addWidget(errorLabel)

	def infoFilm(self, code):
		
			# widgetToRemove = self.layout().itemAt(1).widget().itemAt(1)
			# self.layout().itemAt(1).widget().removeWidget( widgetToRemove )
			# widgetToRemove.setParent( None )

		contentFilm = api.infoFilm(code)

		titre = contentFilm['movie']['title']
		duree = contentFilm['movie']['runtime']
		annee = contentFilm['movie']['release']['releaseDate']
		pays = contentFilm['movie']['release']['country']['$']
		realisateur = contentFilm['movie']['castingShort']['directors']
		synopsis = contentFilm['movie']['synopsis']
		casting = contentFilm['movie']['castingShort']['actors']
		urlPoster = contentFilm['movie']['poster']['href']
		api.getImg(urlPoster)

		url = "\"http://www.allocine.fr/film/fichefilm_gen_cfilm=" + str(code) + ".html\""

		realLabel = QLabel("Realisateur : " + realisateur)
		dureeLabel = QLabel("Duree : " + str(duree // 3600) + "h" + str(duree / 60 - (duree//3600)*60))
		anneeLabel = QLabel("Date de sortie : " + annee)
		paysLabel = QLabel("Pays : " + pays)
		posterLabel = QLabel()
		posterPixmap = QPixmap('.poster/poster.jpg')
		posterPixmap = posterPixmap.scaledToWidth(255)
		posterLabel.setPixmap(posterPixmap)
		lienAllocineLabel = QLabel("<a href="+url+">Lien Allocine</a>")
		lienAllocineLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		lienAllocineLabel.setOpenExternalLinks(True)

		synopsisLabel = QLabel(synopsis)
		synopsisLabel.setWordWrap(True)

		
		if self.layout().itemAt(1).widget().count() == 1:

			groupBoxInfo = QGroupBox(titre)
			vboxSynopsis = QVBoxLayout()
			vboxSideAffiche = QVBoxLayout()
			hboxAffiche = QHBoxLayout()
			vboxInfo = QVBoxLayout()

			vboxSideAffiche.addWidget(dureeLabel)
			vboxSideAffiche.addWidget(realLabel)
			vboxSideAffiche.addWidget(anneeLabel)
			vboxSideAffiche.addWidget(paysLabel)
			hboxAffiche.addLayout(vboxSideAffiche)
			hboxAffiche.addWidget(posterLabel)
			vboxSynopsis.addWidget(synopsisLabel)
			vboxSynopsis.addWidget(lienAllocineLabel)

			vboxInfo.addLayout(hboxAffiche)
			vboxInfo.addLayout(vboxSynopsis)

			groupBoxInfo.setLayout(vboxInfo)
			self.layout().itemAt(1).widget().addWidget(groupBoxInfo)
		else:
			cleanLayout(self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().itemAt(0))
			cleanLayout(self.layout().itemAt(1).widget().widget(1).layout().itemAt(0))
			cleanLayout(self.layout().itemAt(1).widget().widget(1).layout().itemAt(1))

			print(self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout())
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().itemAt(0).layout().addWidget(dureeLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().itemAt(0).layout().addWidget(realLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().itemAt(0).layout().addWidget(anneeLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().itemAt(0).layout().addWidget(paysLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(0).layout().addWidget(posterLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(1).layout().addWidget(synopsisLabel)
			self.layout().itemAt(1).widget().widget(1).layout().itemAt(1).layout().addWidget(lienAllocineLabel)


	def create_connect(self, film):
		return lambda: self.infoFilm(film)





def cleanLayout(layout):
	if layout:
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
