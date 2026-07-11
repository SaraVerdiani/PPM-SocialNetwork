# PPM - Social Network
di Verdiani Sara, 7134296

Tipo di progetto: Full-Stack Web Application

Framework usato: Django

## Descrizione

Il progetto modella un social network in cui è possibile caricare post testuali e interagire con altri utenti in vari 
modi, come attraverso la pubblicazione di commenti, l'aggiunta di "mi piace" ai caricamenti di altre persone e relazioni
di follow-unfollow. Inoltre, all'utente autenticato viene data la possibilità di personalizzare il proprio profilo 
modificando la biografia e aggiungendo post da fissare in cima alla pagina personale, oppure rendendolo privato, così
che solamente utenti approvati potranno visualizzare i propri contenuti.

Sono presenti tre pagine principali. Nella pagina "Home" verranno 
visualizzati i post di vari utenti, mentre nella pagina "Esplora" si potranno vedere gli account di profili scelti
in modo casuale e alcuni post di notizie. La pagina "Richieste" è visibile solamente agli utenti aventi un profilo 
privato, ed è da quest'ultima che essi potranno accettare o rifiutare le richieste di segui da parte di altre persone.

## Funzioni implementate

### Ruolo: Utenti

- Possibilità di seguire o smettere di seguire altri utenti e di visualizzare i profili che altri utenti seguono o da chi
essi sono seguiti.
- Aggiunta e rimozione dei propri like ai post
- Aggiunta e rimozione dei propri commenti
- Visualizzazione degli utenti che hanno messo "mi piace" a qualche post
- Visualizzazione dei profili di altri utenti e dei loro post
- Aggiunta di post testuali con annessa possibilità di rimuoverli
- Modifica della biografia del proprio profilo
- Possibilità di rendere il proprio profilo privato e accettare o rifiutare le richieste di segui di altri utenti
- Aggiunta di post "fissati" nel profilo personale, in modo che vengano visualizzati prima di altri
- Ricerca di altri profili tramite nome utente

### Ruolo: Moderatore
Gli utenti appartenti a questo gruppo hanno dei permessi speciali:
- Cancellazione di post e commenti di altri utenti
- Disattivazione e riattivazione di account di altri utenti

### Ruolo: Admin

L'admin, avendo accesso alla pagina di amministrazione di Django, può eseguire da essa una serie di operazioni.

## Istruzioni per l'installazione locale

1. Clonare la repository del progetto
2. Creare l'ambiente virtuale: su Windows eseguire *python -m venv venv* oppure *py -m venv venv* per la creazione dell'ambiente e successivamente 
*venv\Scripts\activate* per attivarlo. Su macOs eseguire *python3 -m venv venv* per la creazione e *source venv/bin/activate* per l'attivazione 
3. Installare i requisiti attraverso il comando *pip install -r requirements.txt*
4. Configurare la struttura del database applicando le migrazioni con *python manage.py migrate*
5. Avviare il server con *python manage.py runserver*

## Database

Il database di test è il file *db.sqlite3* ed è già popolato con i dati necessari per provare le funzioni principali dell'applicazione.
È inoltre possibile ricrearlo partendo da un database vuoto applicando prima le opportune migrazioni con il comando 
nel punto 4 delle istruzioni per l'installazione locale e successivamente popolarlo attraverso l'utilizzo delle
fixture contenenti i dati presenti nel database di test predefinito. Per fare ciò, eseguire il comando 
*python manage.py loaddata groups_fixture.json users_fixtures.json post_fixture.json news_fixture.json comments_fixture.json*


## Account di prova
### Admin
Username: admin_demo

Password: admin12345

### Moderatore

Username: manager_demo

Password: manager12345

### Utente

Username: user_demo

Password: user12345

## Link di deploy

https://ppm-socialnetwork-production.up.railway.app/users/login/

# Esempio di flusso di test 

## Utente

1. Eseguire il login inserendo username e password
2. Una volta autenticati, è possibile visualizzare la home: da qui si potranno vedere i post di altri utenti,
aggiungere like e commenti cliccando sulle opportune icone.
3. Una volta aggiunti like o commenti si possono eliminare sempre cliccando l'opportuna icona 
4. Cliccando sul tasto "Aggiungi post" sarà possibile creare un post contenente del testo personalizzabile, che sarà 
visibile ad altri utenti. 
5. Successivamente, andando nella pagina "Esplora" si potranno visualizzare profili di altri utenti e seguirli attraverso
il tasto "Follow", oppure visualizzare i loro profili cliccando sul nome utente.
6. Se si desidera modificare il profilo, cliccare sul proprio nome utente e su "Edit profile". Da qui l'utente potrà 
aggiungere una biografia, rendere il proprio account privato o fissare post.

## Moderatore

1. Eseguire il login con le credenziali da moderatore
2. Una volta autenticati, sarà possibile eliminare post e commenti premendo le opportune icone.
3. Cliccando sul profilo di un utente, si visualizzerà un tasto da cui è possibile vietargli l'accesso (ban).