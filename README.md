# 🚙 Projet Système multi-agents
Projet pour le cours de Système multi-agents à CentraleSupélec.

## 🎯 Objectifs
L'objectif du projet est de simuler un processus d'interaction entre différents agents pour choisir le meilleur moteur pour une nouvelle voiture, en prenant en compte plusieurs critères tels que la consommation, l'impact environnemental, le coût, la durabilité, etc. Le but est de simuler différents comportements d'agents pour aboutir à la meilleure offre.  
 
La librairie de modélisation multi-agents [mesa](https://www.springerprofessional.de/en/utilizing-python-for-agent-based-modeling-the-mesa-framework/18470634) met à disposition des outils pour créer des modèles d'agents, les faire interagir, et analyser leurs résultats.

## :page_facing_up: Description
Un constructeur automobile souhaite lancer une nouvelle voiture sur le marché. Pour cela, un choix crucial est celui des moteurs qui doivent répondre à certaines exigences techniques tout en étant attrayants pour les clients (économiques, robustes, écologiques, etc.). Plusieurs types de moteurs existent et offrent donc une large gamme de modèles de voitures : essence ou diesel Internal Combustion Engine (ICE), gaz naturel comprimé (CNG), batterie électrique (EB), pile à combustible (FC), etc. La société décide de prendre en compte différents critères pour les évaluer : consommation, impact environnemental (CO2, carburant propre, NOX1...), coût, durabilité, poids, vitesse maximale ciblée, etc. Pour établir la meilleure offre/choix parmi un grand nombre d'options, elle décide de simuler un processus d'interaction où des agents, avec des opinions et des préférences différentes (voire des connaissances et des expertises différentes), discutent de la question pour aboutir à la meilleure offre. La simulation permettra à la société de simuler plusieurs typologies de comportements d'agents (expertise, rôle, préférences, etc.) à moindre coût et dans un délai raisonnable.  

Pour cela, nous avons implémenté une simulation de dialogue fondée sur l'argumentation entre agents. Des agents représentant l'ingénierie humaine devront interagir les uns avec les autres pour prendre une décision conjointe concernant le choix du meilleur moteur. Les conflits dans l'interaction surviennent lorsque les agents ont des préférences différentes sur les critères, et l'argumentation les aidera à décider quel élément sélectionner.

## 🤔 Choix techniques
Nous avons décidé d'implémenter notre simulation sur deux agents et cinq items différents. Les agents ont ainsi différents choix pour argumenter et trouver un compromis. Leurs préférences ont été générées aléatoirement.

L'algorithme proposé a été modifié dans le but de rajouter une contre proposition. Si un agent rejette une proposition en argumentant qu'elle ne respecte pas un critère donné, l'autre agent peut proposer un autre moteur (compromis) qui répond à ce critère et à ses préférences.

## :card_index_dividers: Segmentation
Notre répertoire `mesa` est segmenté en 17 fichiers python, 8 fichiers Icon, 4 fichiers xml, un fichier iml, un fichier markdown, deux fichiers .gitinore et deux fichiers texte pour les requirements :

```bash 
.
├── README.md
├── .gitignore
├── requirements.txt 
├── Icon
├── pw_argumentation.py
├── engines.csv
├── .idea
│     ├── inspectionProfiles
│     │        ├── Icon
│     │        └── profiles_settings.xml
│     ├── .gitignore
│     ├── Icon
│     ├── mesa.iml
│     ├── misc.xml
│     ├── modules.xml
│     └── workspace.xml
└── communication
      ├── agent
      │        ├── __init__.py
      │        ├── CommunicatingAgent.py
      │        └── Icon
      ├── mailbox
      │        ├── __init__.py
      │        ├── Mailbox.py
      │        └── Icon
      ├── message
      │        ├── __init__.py
      │        ├── Message.py
      │        ├── MessagePerformative.py
      │        ├── MessageService.py
      │        └── Icon
      ├── preferences
      │        ├── __init__.py
      │        ├── CriterionName.py
      │        ├── CriterionValue.py
      │        ├── Item.py
      │        ├── Preferences.py
      │        ├── Value.py
      │        └── Icon
      ├── __init__.py
      ├── Icon
      ├── requirements.txt
      └── runtests.py


```

- ``README.md`` contient l'ensemble des informations sur le projet pour pouvoir l'installer.
- ``.gitignore`` contient les fichiers qui doivent être ignorés lors de l'ajout de fichiers au dépôt Git.
- ``requirements.txt`` contient la liste des modules et des bibliothèques Python qui doivent être installés, ainsi que leur version spécifique.
- le dossier ``communication`` est la racine de la couche de communication et contient quatre sous-dossiers : ``agent`` (dossier qui contient l'implémentation de la classe agent communicant), ``mailbox`` (dossier qui contient l'implémentation de la classe mailbox), ``message`` (dossier qui contient l'implémentation de la classe message et performative) et ``preferences`` (dossier qui contient l'implémentation des classes de préférences).
- ``pw_argumentation.py`` est le fichier python qui contient notre classe d'agents et notre modèle pour la simulation d'argumentation.
- ``engines.csv`` est le fichier csv qui contient les valeurs de nos différents moteurs implémentés.

## :wrench: Installation
Pour lancer, nous vous recommandons sur un terminal uniquement :

1. Tout d'abord, assurez-vous que vous avez installé une version `python` supérieure à 3.10. Nous vous conseillons un environnement conda avec la commande suivante : 
```bash
conda create --name sma python=3.10.8
```
- Pour activer l'environnement :
```bash
conda activate sma
```
- Pour accéder au répertoire : 
```bash
cd mesa
```

2. Vous devez ensuite installer tous les `requirements` en utilisant la commande suivante :
```bash
conda install --file requirements.txt
```

3. Exécuter la simulation avec la commande suivante : 
```bash
python3 pw_argumentation.py
```

## :pencil2: Auteurs
- MICHOT Albane
- NONCLERCQ Rodolphe



