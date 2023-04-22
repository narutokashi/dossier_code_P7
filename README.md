
# Objectif

Le projet a pour objectif de développer un algorithme de "scoring crédit" pour calculer la probabilité qu'un client rembourse son crédit et de classer les demandes en crédit accordé ou refusé. Pour cela, l'entreprise souhaite s'appuyer sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.). De plus, afin de répondre à la demande croissante de transparence de la part des clients, l'entreprise souhaite également développer un dashboard interactif permettant aux chargés de relation client d'expliquer de façon transparente les décisions d'octroi de crédit et de permettre aux clients d'accéder facilement à leurs informations personnelles.

# Découpage des dossiers

Nous avons deux repositories:
1) pour l'API: "WEB-API " (https://github.com/narutokashi/WEB-API)
2) pour le dashboard: "dashboard-P7" (https://github.com/narutokashi/dashboard-P7)

Voici leur classification:

![image](https://user-images.githubusercontent.com/130460342/233800647-198c10dd-bfa6-4020-a51d-a48bb0a827d4.png)

Les librairies utilisées se retrouvent dans le fichier requirement.txt

Pour visualiser les applications déployés sur Heroku voici les liens:
- API : https://web-api-score.herokuapp.com/
- Dashboard : https://dashboard-score.herokuapp.com/

Dans ce dossier présent nous avons le notebook de la modélisation, le tableau HTML d’analyse de data drift et les codes de Dashboard et d'API.
