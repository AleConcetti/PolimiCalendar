from bs4 import BeautifulSoup

#APRO IL FILE E ESTRAPOLO SOLO QUELLO CHE MI SERVE (orarioTestuale)
f = open("Orario_delle_lezioni_NUOVO.html")
soup = BeautifulSoup(f, "html.parser")
orario = soup.find("div", { "id" : "orarioTestuale" })

#TRASFORMO IL BLOCCO orario IN TANTI ELEMENTI PER POI SCARTARE QUELLO CHE NON MI SERVE
listaElementi=[]
for el in orario:
            listaElementi.append(str(el))

#SCARTO LE PROVE FINALI E I <br/> TRASFORMANDOLE IN ELEMENTI VUOTI
for i in range(len(listaElementi)):
    if 'PROVA FINALE' in listaElementi[i]:
        for j in range(10):
            listaElementi[i+j]=' '
    if '<br/>' in listaElementi[i]:
        listaElementi[i] = ' '

#ORA METTO SOLO GLI ELEMENTI NON VUOTI IN UN'ALTRA LISTA (listaElemSenzaSpazi)
listaElemSenzaSpazi=[]
for i in range(len(listaElementi)):
    if not str(listaElementi[i]).isspace():
        listaElemSenzaSpazi.append(listaElementi[i])


numCorsi = int(len(listaElemSenzaSpazi)/8) #Per ogni corso ci sono otto elementi. Lo si vede printando.
#print(listaElemSenzaSpazi)

#ORA ORGANIZZO MEGLIO LA LISTA DIVIDENDOLA IN N PARTI (N=numCorsi)
listaDivisaInCorsi=[] #ListaDivisaInCorsi è una lista di liste di stringhe.
temp=[]
for j in range(numCorsi):
    for i in range(8*j,8+8*j):
        temp.append(listaElemSenzaSpazi[i])
    listaDivisaInCorsi.append(temp)
    temp=[]



#ORA ESTRAPOLO DA listaDivisaInCorsi I SINGOLI PARAMETRI DELL'EVENTO

titoliCorsi=[] #titoliCorsi è una lista con i titoli dei corsi IN ORDINE
for i in range(numCorsi):
    inizioTitolo=str(listaDivisaInCorsi[i][0]).find('<b>') + 12
    fineTitolo=str(listaDivisaInCorsi[i][0]).find('</b>')
    titoliCorsi.append(listaDivisaInCorsi[i][0][inizioTitolo:fineTitolo])

semestreCorsi=[] #semestreCorsi è una lista di interi che indica per ogni corso se è il primo o il secondo semestre
for i in range(numCorsi):
    semestreCorsi.append(int(listaDivisaInCorsi[i][2]))

dataInizioCorsi=[] #DataInizioCorsi è una lista di stringhe che indica la            data di inizio
for i in range(numCorsi):
    dataInizioCorsi.append(str(listaDivisaInCorsi[i][4]).replace(' ','').replace('\n','').replace('\t',''))

dataFineCorsi=[] #DataFineCorsi è una lista di stringhe che indica la data di fine
for i in range(numCorsi):
    dataFineCorsi.append(str(listaDivisaInCorsi[i][6]).replace(' ','').replace('\n','').replace('\t',''))

stringheLezioni=[] #StringheLezioni è una lista di stringhe con le info sulle lezioni
for i in range(numCorsi):
    stringa=str(listaDivisaInCorsi[i][7])
    flag=1
    while(flag):
        apriParentesi=stringa.find('<')
        chiudiParentesi=stringa.find('>')
        if(apriParentesi!=-1 and chiudiParentesi!=-1):
            stringa=stringa.replace(stringa[apriParentesi:chiudiParentesi+1],' ')
        else:
            flag=0

    flag = 1
    while (flag):
        apriParentesi = stringa.find('(')
        chiudiParentesi = stringa.find(')')
        if (apriParentesi != -1 and chiudiParentesi != -1):
            stringa = stringa.replace(stringa[apriParentesi:chiudiParentesi + 1], '|')
        else:
            flag = 0

    stringheLezioni.append(stringa[2:])#Levo i due spazi inziali che sono proprio brutti


#ORA DIVIDO LA STRINGA DELLE LEZIONI IN TANTI ELEMENTI giorno,oraInizio,oraFine,tipo, etc..

lezioni=[] #lezioni è una lista di liste che contengono le singole lezioni. Esempio lezioni[0][1] è la seconda lezione della settimana della materia 1
lezSingCorso=[] #mi serve come supporto per creare la lista lezioni
for i in range(numCorsi):
    for lez in str(stringheLezioni[i]).split('|'):
        if not lez.isspace():
            lezSingCorso.append(lez)
    lezioni.append(lezSingCorso)
    lezSingCorso=[]
giorno=[]
inizio=[]
fine=[]
tipo=[]
dove=[]
giornoCorsi=[]
inizioCorsi=[]
fineCorsi=[]
tipoCorsi=[]
doveCorsi=[]
for i in range(numCorsi):
    for j in range(len(lezioni[i])):
        strSplittata=(str(lezioni[i][j]).split(' '))
        while '' in strSplittata:
            strSplittata.remove('')
        giorno.append(strSplittata[0])
        inizio.append(strSplittata[2])
        fine.append(strSplittata[4].replace(',',''))
        tipo.append(strSplittata[5])
        dove.append(strSplittata[strSplittata.index('aula')+1])
    giornoCorsi.append(giorno)
    inizioCorsi.append(inizio)
    fineCorsi.append(fine)
    tipoCorsi.append(tipo)
    doveCorsi.append(dove)
    giorno = []
    inizio = []
    fine = []
    tipo = []
    dove = []

#ESEMPI
#print('Il corso 0 ha lezioni in questi giorni della settimana: ', giornoCorsi[0])
#print('La seconda lezione della settimana del corso 2 inizia a questa ora: ', inizioCorsi[2][1])



for i in range(numCorsi):
    print('Titolo: ', titoliCorsi[i])
    print('Semestre: ', semestreCorsi[i])
    print('Inizio: ', dataInizioCorsi[i])
    print('Fine: ', dataFineCorsi[i])
    print('Orario: ',)
    for j in range(len(giornoCorsi[i])):
        print('       ', giornoCorsi[i][j],tipoCorsi[i][j],'dalle',inizioCorsi[i][j],'alle',fineCorsi[i][j], doveCorsi[i][j])
    print(' ','*'*100, ' ', sep='\n')

#Vedi Selenium libreria per navigare in internet

for i in range(numCorsi):
    for j in range(len(giornoCorsi[i])):

        if (giornoCorsi[i][j]=='Lunedì'):
            d='2018-09-17'
        elif(giornoCorsi[i][j]=='Martedì'):
            d='2018-09-18'
        elif(giornoCorsi[i][j]=='Mercoledì'):
            d='2018-09-19'
        elif(giornoCorsi[i][j]=='Giovedì'):
            d='2018-09-20'
        elif(giornoCorsi[i][j]=='Venerdì'):
            d='2018-09-21'
        elif(giornoCorsi[i][j]=='Sabato'):
            d='2018-09-22'

        timestamp_inizio=d+'T'+inizioCorsi[i][j]+':00-07:00'
        timestamp_fine=d+'T'+fineCorsi[i][j]+':00-07:00'

        if(semestreCorsi[i]==1):
            count=14
        else:
            count=15

        event = {
        'summary': titoliCorsi[i],
        'location': doveCorsi[i][j],
        'description': tipoCorsi[i][j],
        'start': {
            'dateTime': timestamp_inizio,
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': timestamp_fine,
            'timeZone': 'Europe/Rome',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT='+count
        ]
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
