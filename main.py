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

		splitterRes = QSplitter()
		splitterRes.setOrientation(Qt.Horizontal)

		hboxParam = QHBoxLayout()
		hboxResultats = QHBoxLayout()
		vboxGlobal = QVBoxLayout()


		hboxParam.addWidget(labelVille)
		hboxParam.addWidget(textEditVille)
		hboxParam.addWidget(labelJour)
		hboxParam.addWidget(calendarJour)
		hboxParam.addWidget(buttonValiderParam)

		hboxResultats.addWidget(splitterRes)
 
		vboxGlobal.addLayout(hboxParam)
		vboxGlobal.addLayout(hboxResultats)


		self.setLayout(vboxGlobal)
		
		buttonValiderParam.clicked.connect(lambda: self.validerParam(textEditVille.text(), calendarJour.date()))
		textEditVille.returnPressed.connect(lambda: self.validerParam(textEditVille.text(), calendarJour.date()))

		self.setWindowTitle('Super Cinemon 2000 ExtraPlus')
		
		self.show()


	def validerParam(self, ville, jour):
		if ville != '':
			self.cleanSplitter()
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
				dicoHoraires = dict()
				dicoCodeFilm = dict()

				scrollAreaSeance = QScrollArea()
				groupBoxSeances = QGroupBox()
				vboxSeances = QVBoxLayout()

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
				self.layout().itemAt(1).itemAt(0).widget().insertWidget(0,scrollAreaSeance)

			elif codeRetour == 200:
				errorMessageBox = QMessageBox()
				errorMessageBox.critical(self,'Erreur', 'Erreur : connexion impossible', 'Allociné ne répond pas correctement. \nCauses possibles : \nProtocole de connexion à l\'API modifié \nSite temporairement inaccessible \nSite définitivement inaccessible (pas de pot)')

			elif codeRetour == 300:
				errorMessageBox = QMessageBox()
				errorMessageBox.warning(self,'Pas de salle', "Il n'y a pas de salle de cinema référencées à " + ville)

			elif codeRetour == 400:
				errorMessageBox = QMessageBox()
				errorMessageBox.warning(self,'Ville non référencée', "La ville " + ville + u" n'est pas référencée, êtes-vous certain de l'orthographe ?")


	def infoFilm(self, code):

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
		posterPixmap = QPixmap('/tmp/poster.jpg')
		posterPixmap = posterPixmap.scaledToWidth(255)
		posterLabel.setPixmap(posterPixmap)
		lienAllocineLabel = QLabel("<a href="+url+">Lien Allociné</a>")
		lienAllocineLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		lienAllocineLabel.setOpenExternalLinks(True)

		synopsisLabel = QLabel(synopsis)
		synopsisLabel.setWordWrap(True)


		self.cleanSplitter(onlyInfos=True)

		scrollAreaInfos = QScrollArea()
		groupBoxInfos = QGroupBox()
		vboxInfos = QVBoxLayout()

		vboxSynopsis = QVBoxLayout()
		vboxSideAffiche = QVBoxLayout()
		hboxAffiche = QHBoxLayout()

		vboxSideAffiche.addWidget(dureeLabel)
		vboxSideAffiche.addWidget(realLabel)
		vboxSideAffiche.addWidget(anneeLabel)
		vboxSideAffiche.addWidget(paysLabel)
		hboxAffiche.addLayout(vboxSideAffiche)
		hboxAffiche.addWidget(posterLabel)
		vboxSynopsis.addWidget(synopsisLabel)
		vboxSynopsis.addWidget(lienAllocineLabel)

		vboxInfos.addLayout(hboxAffiche)
		vboxInfos.addLayout(vboxSynopsis)

		groupBoxInfos.setLayout(vboxInfos)
		scrollAreaInfos.setWidget(groupBoxInfos)

		self.layout().itemAt(1).itemAt(0).widget().insertWidget(1,scrollAreaInfos)

	def create_connect(self, film):
		return lambda: self.infoFilm(film)

	def cleanSplitter(self, onlyInfos = False):
		for i in reversed(range(self.layout().itemAt(1).itemAt(0).widget().count())):
			if i==0:
				if not onlyInfos:
					if self.layout().itemAt(1).itemAt(0).widget().widget(i):
						self.layout().itemAt(1).itemAt(0).widget().widget(i).setParent(None)
			else:
				if self.layout().itemAt(1).itemAt(0).widget().widget(i):
					self.layout().itemAt(1).itemAt(0).widget().widget(i).setParent(None)


monApp=QApplication(sys.argv)
fenetre=Principale()
monApp.exec_()