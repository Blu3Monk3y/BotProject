AUTOMATED BOT
===============

#### v1.0.0



The project i still in a developing phase, it's a telegram bot programmed in python which allow people to organize channells and to provide the affiliation links from amazon to a large spectrum of oudience. 

Documentazione
---------------

### Run Script
The bot is runned running the TelegramBot.py


### Driver 
The bot uses Selenium as main library to automatize processes, so u will find the drivers in the driver dir present in the project.


### Features API 


> **Feature Proxy**<br/>
> La libreria *proxy.py* presente in feature contiene la funzione *randomHttps* che si occupa di restiture le informazioni necessarie per utilizzare un proxy con le configurazioni del browser. All'interno della libreria è presente una lista di dizionari contenente i vari proxy, è possibile aggiungere o rimuovere una configurazione tramite la definizione all'interno della lista. Una configurazione è definita da un dizionario contenente:
> - **ip** per identificare l'host a cui effettura la connessione
> - **port** per identificare la porta di collegamento del proxy 
> - **country** è un'informazione aggiuntiva per sapere il paese di provenienza del proxy 


> **Feature User-Agent**<br />
>The * user_agent.py * library present in the feature contains the functions * randomChrome * and * randomFirefox * to return a User-Agent based on the browser indicated. There are two lists (* chrome_agents * and * firefox_agents *) containing the User-Agents formatted as strings, it is possible to add or remove a User-Agent by modifying the values in the lists. The corresponding functions return a random User-Agent.
