from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from bs4 import BeautifulSoup

######################################################################
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
#Il calendarId si vede nelle impostazioni del calendario su google
CAL_ID = 'qj9e8du9plsq6qbf1ml5v6i7vc@group.calendar.google.com'

#INSERIRE LE DATE DELLA PRIMA SETTIMANA DI LEZIONE
primoLun='2018-09-17'
primoMar='2018-09-18'
primoMer='2018-09-19'
primoGio='2018-09-20'
primoVen='2018-09-21'
primoSab='2018-09-22'

#INSERIRE NOME DEL FILE HTML
nome_file_html="Orario_delle_lezioni_NUOVO.html"

#####################################################################

def main():

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=CAL_ID, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    #APRO IL FILE E ESTRAPOLO SOLO QUELLO CHE MI SERVE (orarioTestuale)
    f = open(nome_file_html)
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
        for j in range(len(giornoCorsi[i])):

            if (giornoCorsi[i][j]=='Lunedì'):
                d=primoLun
            elif(giornoCorsi[i][j]=='Martedì'):
                d=primoMar
            elif(giornoCorsi[i][j]=='Mercoledì'):
                d=primoMer
            elif(giornoCorsi[i][j]=='Giovedì'):
                d=primoGio
            elif(giornoCorsi[i][j]=='Venerdì'):
                d=primoVen
            elif(giornoCorsi[i][j]=='Sabato'):
                d=primoSab

            timestamp_inizio=d+'T'+inizioCorsi[i][j]+':00+02:00'
            timestamp_fine=d+'T'+fineCorsi[i][j]+':00+02:00'

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
                'RRULE:FREQ=WEEKLY;COUNT='+str(count)
            ]
            }
            event = service.events().insert(calendarId=CAL_ID, body=event).execute()


if __name__ == '__main__':
    main()
