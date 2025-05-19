### **Cenu salīdzināšanas skripts (e-veikalos Rimi un Barbora)**
### **Autori**
- 241RDC050 Sofija Sočenko
- 241RDC027 Valērija Kļujeva
- 241RDC043 Artūrs Kaļetkins
### **Piezīmes**
- Nepieciešams instalēts microsoft edge internetpārlūks
- Skripts darbojās gan ar precīziem preču nosaukumiem, gan ar vispārējiem nosaukumiem
- Nepieciešams stabils interneta pieslēgums
### Apraksts
Python skripts, kas salīdzina cenas Rimi un Barbora e-veikalos pie precēm, kas tiek ievadītas terminālī. Programma izvada visu atrasto preču sarakstu un to cenas pieaugošā secībā, un beigās izvada lētāko produktu. 
### **Tehnoloģijas**
	•	Python 3.11+
	•	Selenium (atvēr e-veikalu lapas; skrollē un gaida, kamēr visi produkti ielādējas; nolasa datus no lapām)
	•	WebDriver Manager (automātiski lejupielādē un atjaunina Microsoft Edge draiveri)
	•	Microsoft Edge WebDriver (nodrošina saikni starp Python kodu un Edge pārlūkprogrammu)
	•	Regex (re) (meklē tekstā noteiktus vārdus)
	•	Heap (heapq) (atrod viszemāku vērtību sarakstā)
### **Instalācija**
1. Nokopē projektu:
> https://github.com/Arturs-Kaletkins/rimibarbora1 
2. Instalē nepieciešamās bibliotēkas
- pip install selenium 
- pip install webdriver-manager
3. Pārliecinies, vai tev ir microdoft edge pārlūks
> Ja nav - instalē to.
### **Lietošana**
Ievadi preces nosaukumu: (ievadiet produktu, piemēram, "baltmaize")
### **Funkcionalitāte**
- Atver Rimi un Barbora e-veikalus
- Apiet logus "sīkfailu izmantošana"
- Meklē pēc preces nosaukuma
- Salīdzina preču cenas
- Parāda:
1. Visas atrastas preces un to cenas pieaugošā secībā
2. Lētāko preci un veikalu, kurā tā ir atrodama
3. Ja prece netika atrasta, tad izvada paziņojumu "prece netika atrasta"
4. Ja lētākā cena ir vienāda abos veikalos, tad izvada paziņojumu "cena precei (Jūsu prece) ir vienāda: (cena) € veikalos Rimi, Barbora"
