Automated SMS
===============

#### v2.0.0



Il progetto ancora in fase di sviluppo ha l'intento di automatizzare svariati servizi web per compiere azioni come la registrazione utente e il reset della password. Lo script è scritto completamente in python ed utilizza la libreria Selenium per eseguire l'automazione del browser e la libreria Scheduling per implementare un intervallo di azione della task dei servizi.E' possibile definire i servizi attivi all'interno del codice tramite valori booleani e assegnare le corrispondenti task che sfrutttano un approccio multithread per l'esecuzione. Le varie azioni vengono tracciate tramite l'utilizzo di un logger basico che reindirizza l'output su un file specificato all'interno del codice. 

Documentazione
---------------

### Run Script
L'esecuzione dello script richiede dei parametri necessari ovvero *--browser/-b*, *--number/-n*, *--every/-ev*.

- **--browser/-b** Specifica il browser da utilizzare per l'automazione
- **--number/-n** Specifica il file di testo contenente i numeri telefonici (compresi di prefisso) da utilizzare durante le task automatiche
- **--every/-ev** Specifica il tempo (in secondi) che indica allo script l'intervallo temporale per l'esecuzione generica delle task 


### Driver 
Per il corretto funzionamento della libreria Selenium sono presenti i relativi driver all'interno delle directory del progetto che sono suddivisi in base al browser e poi in base all'OS in uso. Lo script riconosce in automatico l'architettura del sistema su cui viene eseguito e definisce le opportune path da utilizzare in relazione al sistema operativo indicato.


### Features API 
Il progetto utilizza delle librerie custom per sfruttare delle feature.
Sono definite all'interno della path */features* e comprendono una libreria per l'utilizzo di proxy e una libreria per l'utilizzo di *Random User-Agent*.

> **Feature Proxy**<br/>
> La libreria *proxy.py* presente in feature contiene la funzione *randomHttps* che si occupa di restiture le informazioni necessarie per utilizzare un proxy con le configurazioni del browser. All'interno della libreria è presente una lista di dizionari contenente i vari proxy, è possibile aggiungere o rimuovere una configurazione tramite la definizione all'interno della lista. Una configurazione è definita da un dizionario contenente:
> - **ip** per identificare l'host a cui effettura la connessione
> - **port** per identificare la porta di collegamento del proxy 
> - **country** è un'informazione aggiuntiva per sapere il paese di provenienza del proxy 


> **Feature User-Agent**<br />
> La libreria *user_agent.py* presente in feature contiene le funzioni *randomChrome* e *randomFirefox* per restituire un User-Agent in base al browser indicato. Sono presenti due liste (*chrome_agents* e *firefox_agents*) contenenti gli User-Agent formattati come stringhe, è possibile aggiungere o rimuovere un User-Agent modificanto i valori presenti nelle liste. Le corrispettive funzioni ritorna un User-Agent randomico.