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