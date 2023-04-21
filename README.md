# 🚙 Projet Système multi-agents
Projet pour le cours de Système multi-agents à CentraleSupélec.

## 🎯 Objectifs
L'objectif du projet est de simuler un processus d'interaction entre différents agents pour choisir le meilleur moteur pour une nouvelle voiture, en prenant en compte plusieurs critères tels que la consommation, l'impact environnemental, le coût, la durabilité, etc. Le but est de simuler différents comportements d'agents pour aboutir à la meilleure offre.  
 
La librairie de modélisation multi-agents [mesa](https://www.springerprofessional.de/en/utilizing-python-for-agent-based-modeling-the-mesa-framework/18470634) met à disposition des outils pour créer des modèles d'agents, les faire interagir, et analyser leurs résultats.

## :page_facing_up: Description
Un constructeur automobile souhaite lancer une nouvelle voiture sur le marché. Pour cela, un choix crucial est celui des moteurs qui doivent répondre à certaines exigences techniques tout en étant attrayants pour les clients (économiques, robustes, écologiques, etc.). Plusieurs types de moteurs existent et offrent donc une large gamme de modèles de voitures : essence ou diesel Internal Combustion Engine (ICE), gaz naturel comprimé (CNG), batterie électrique (EB), pile à combustible (FC), etc. La société décide de prendre en compte différents critères pour les évaluer : consommation, impact environnemental (CO2, carburant propre, NOX1...), coût, durabilité, poids, vitesse maximale ciblée, etc. Pour établir la meilleure offre/choix parmi un grand nombre d'options, elle décide de simuler un processus d'interaction où des agents, avec des opinions et des préférences différentes (voire des connaissances et des expertises différentes), discutent de la question pour aboutir à la meilleure offre. La simulation permettra à la société de simuler plusieurs typologies de comportements d'agents (expertise, rôle, préférences, etc.) à moindre coût et dans un délai raisonnable.  

Pour cela, nous avons implémenté une simulation de dialogue fondée sur l'argumentation entre agents. Des agents représentant l'ingénierie humaine devront interagir les uns avec les autres pour prendre une décision conjointe concernant le choix du meilleur moteur. Les conflits dans l'interaction surviennent lorsque les agents ont des préférences différentes sur les critères, et l'argumentation les aidera à décider quel élément sélectionner.

## 🤔 Choix techniques
Nous avons décidé d'implémenter notre simulation sur deux agents et cinq items différents. Les agents ont ainsi différents choix pour argumenter et trouver un compromis. Leurs préférences ont été générées à partir de profils, qui eux sont aléatoires, attribués à chacun des agents.  
On prend aléatoirement les profils afin que les agents aient des préférences différentes et ainsi une discussion.  
Nous avons rajouté la fonction ``sorted_item_list`` dans la classe ``Preferences`` afin de faciliter l'écriture du code pour ``is_item_among_top_10_percent`` et accélérer le processus de décision côté agent.

Nous avons créé un fichier python ``arguments.py`` pour structurer les arguments en rajoutant en plus des phrases des metadata, comme par exemple le type d'argument.    
La structure de la classe ``Argument`` permet de renvoyer une phrase correspondant à l'argument, en plus de faciliter l'utilisation de ces derniers.  
Nous avons également rajouté un moyen de comparer les arguments entre eux, en particulier afin de voir s'ils sont égaux pour éviter de réutiliser plusieurs fois le même argument. 

Le dialogue s'effectue entre deux agents et cinq items (engines). Les agents parlent chacun à leur tour et propose ou argumente sur les critères. S’ils n’ont plus d’arguments, ils peuvent proposer un autre moteur (au maximum 3 moteurs peuvent être proposés).

## :card_index_dividers: Segmentation
Notre répertoire est segmenté en 18 fichiers python, 1 fichier csv, un fichier markdown, un fichier .gitinore, deux fichiers texte pour les requirements et un fichier pdf :

```bash 
.
├── README.md
├── .gitignore
├── requirements.txt 
├── pw_argumentation.py
├── engines.csv
├── Rapport_Projet_SMA_Part_2.pdf
└── communication
      ├── agent
      │        ├── __init__.py
      │        └── CommunicatingAgent.py
      ├── mailbox
      │        ├── __init__.py
      │        └── Mailbox.py
      ├── message
      │        ├── __init__.py
      │        ├── Message.py
      │        ├── MessagePerformative.py
      │        └── MessageService.py
      ├── preferences
      │        ├── __init__.py
      │        ├── CriterionName.py
      │        ├── CriterionValue.py
      │        ├── Item.py
      │        ├── Preferences.py
      │        └── Value.py
      ├── __init__.py
      ├── requirements.txt
      ├── arguments.py
      └── runtests.py


```

- ``README.md`` contient l'ensemble des informations sur le projet pour pouvoir l'installer.
- ``.gitignore`` contient les fichiers qui doivent être ignorés lors de l'ajout de fichiers au dépôt Git.
- ``requirements.txt`` contient la liste des modules et des bibliothèques Python qui doivent être installés, ainsi que leur version spécifique.
- le dossier ``communication`` est la racine de la couche de communication et contient quatre sous-dossiers : ``agent`` (dossier qui contient l'implémentation de la classe agent communicant), ``mailbox`` (dossier qui contient l'implémentation de la classe mailbox), ``message`` (dossier qui contient l'implémentation de la classe message et performative) et ``preferences`` (dossier qui contient l'implémentation des classes de préférences). Le fichier ``arguments.py`` est le fichier python qui permet de structurer nos arguments.
- ``pw_argumentation.py`` est le fichier python qui contient notre classe d'agents et notre modèle pour la simulation d'argumentation.
- ``engines.csv`` est le fichier csv qui contient les valeurs de nos différents moteurs implémentés.
- ``Rapport_Projet_SMA_Part_2.pdf`` est le rapport du projet qui contient l'ensemble des informations et justifications d'implémentation.

## :wrench: Installation
Pour lancer, nous vous recommandons sur un terminal uniquement :

1. Tout d'abord, assurez-vous que vous avez installé une version `python` supérieure à 3.9 et `Anaconda` ou `Miniconda`. 

2. Pour cloner le répertoire, choisissez l’emplacement où vous souhaitez accéder au répertoire sur votre ordinateur, en tapant la commande suivante sur votre Terminal :
```bash
cd desktop # affichera sur votre Bureau d'ordinateur 
git clone https://gitlab-student.centralesupelec.fr/albane.michot/project_sma_part_2.git
cd project_sma_part_2
```

3. Nous vous conseillons un environnement conda avec la commande suivante qui permet d'installer directement les `requirements` sur l'environnment créé : 
```bash
conda create --name mesa --file requirements.txt
```
- Pour activer l'environnement :
```bash
conda activate mesa
```

4. Exécuter la simulation avec la commande suivante : 
```bash
python3 pw_argumentation.py
```

## :pencil2: Auteurs
- MICHOT Albane
- NONCLERCQ Rodolphe



