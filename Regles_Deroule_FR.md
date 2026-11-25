> ⚠️ **Obsolète** : remplacé par la V2 simplifiée (`Regles_V2_Simplifiees.md` et `Data_Detective_Game_Design.md`). Gardé pour mémoire.

# THE LAST QUERY : déroulé des règles à personnaliser (version française)

> 🇫🇷 Ceci est la **traduction française** de `Regles_Deroule.md`, pour bien comprendre les règles. Le jeu final reste **en anglais**. Vous pouvez remplir vos modifications dans l'une ou l'autre version.

**Mode d'emploi pour le groupe**
- Chaque bloc suit une partie dans l'ordre, du début à la fin.
- **📜 Règle** : la règle actuelle.
- **🎛 Levier modifiable** : ce qu'on peut changer, avec des idées d'alternatives.
- **✏️ Notre version** : à vous de remplir. Laissez vide si la règle vous va, écrivez « supprimé » pour enlever la règle.
- **🎨 Impact design** : les fichiers de `DA/` à refaire si vous changez ce bloc.

---

## BLOC 0 : Carte d'identité du jeu

📜 **Règle**
> *The Last Query* est un jeu de déduction compétitif pour **2 à 4 détectives** (ou équipes de 2), à partir de **12 ans**, pour environ **40 à 60 minutes**. Explorez le manoir sur le plateau, débloquez le SQL sur votre téléphone, et démasquez le meurtrier avant l'aube.

🎛 **Levier modifiable** : nombre de joueurs, durée, compétitif ou coopératif.
- *Alternative A* : **mode coopératif**. Tout le monde enquête ensemble contre l'horloge, et les résultats de requêtes sont partagés.
- *Alternative B* : jusqu'à **6 joueurs** en ajoutant 2 détectives.

✏️ **Notre version :**

> 

🎨 Impact design : couverture du livret, boîte, plateau (barre latérale), cartes Détective si joueurs en plus.

---

## BLOC 1 : L'histoire de départ

📜 **Règle**
> Sir Victor Ravenscroft, fondateur de *Ravenscroft Analytics*, est retrouvé mort dans la **Bibliothèque** à **23h45**, pendant la fête de ses 70 ans. La foudre a fait exploser la base de données de l'IA de la maison, **W.A.T.S.O.N.**, en **fragments de données** (Data Shards). L'orage a coupé le pont : la police n'arrivera qu'à **l'aube**. Si personne n'a résolu l'affaire d'ici là, **le meurtrier s'enfuit et tout le monde perd**.

🎛 **Levier modifiable** : noms, lieu, époque, nom de l'IA, heure du crime, ton (plus drôle, plus sombre).
- *Alternative A* : l'IA s'appelle autrement, ou elle est un personnage qui « parle » dans l'app.
- *Alternative B* : changer la victime ou le lieu (un paquebot, un train de nuit…).

✏️ **Notre version :**

> 

🎨 Impact design : livret (p. 2), plateau (horloge arrêtée à 11:45, décor), logo seulement si le nom change.

---

## BLOC 2 : Mise en place

📜 **Règle**
> 1. L'hôte ouvre l'app, choisit une **affaire** et obtient un **code de partie** (ex. `RAVEN-42`). Les autres joueurs rejoignent avec leur téléphone.
> 2. Triez les 60 cartes indices selon la pièce indiquée au dos, mélangez chaque pile et posez-la face cachée sur sa pièce (7 pièces ont une pioche).
> 3. Chaque joueur prend un détective, place son pion dans le **Grand Hall** et prend **3 ☕**.
> 4. Placez le jeton horloge sur **minuit (12:00 AM)**.
> 5. Le joueur le plus jeune commence.

🎛 **Levier modifiable** : café de départ, point de départ, premier joueur, cartes en main au départ.
- *Alternative A* : chaque joueur commence avec **`WHERE`** déjà débloqué, pour accélérer le début.
- *Alternative B* : chacun démarre dans une **pièce différente**. Le premier joueur est « celui qui a lu un polar le plus récemment ».

✏️ **Notre version :**

> 

🎨 Impact design : livret (Mise en place), plateau (médaillons P1–P4 dans le Grand Hall), jetons café.

---

## BLOC 3 : Structure d'un tour

📜 **Règle**
> À ton tour, fais 3 étapes dans l'ordre : **① SE DÉPLACER → ② AGIR (une seule action) → ③ REQUÊTES (facultatif)**.

🎛 **Levier modifiable** : nombre d'étapes et d'actions par tour.
- *Alternative A* : **2 actions** par tour au lieu d'une (partie plus rapide).
- *Alternative B* : on peut faire des requêtes **à tout moment**, même pendant le tour des autres.

✏️ **Notre version :**

> 

🎨 Impact design : livret (Un tour + aide-mémoire), plateau (résumé du tour dans la barre latérale).

---

## BLOC 4 : ① Se déplacer

📜 **Règle**
> Déplace-toi d'au plus **2 pièces** en suivant les couloirs. Un **passage secret** compte pour 1 déplacement (Cave à vin ⇄ Observatoire, Serre ⇄ Chapelle). Tu peux aussi rester sur place.

🎛 **Levier modifiable** : distance, dé ou pas, passages secrets.
- *Alternative A* : on lance un **dé** (1–2 = 1 pièce, 3–5 = 2 pièces, 6 = n'importe où).
- *Alternative B* : déplacement **gratuit de 1 pièce**, et chaque pièce en plus coûte 1 ☕.

✏️ **Notre version :**

> 

🎨 Impact design : livret, plateau si les passages secrets changent (trappes rouges).

---

## BLOC 5 : ② Agir (une action au choix)

📜 **Règle**
> Choisis **UNE** action :
> - **Fouiller** : pioche la première carte de la pioche de la pièce.
> - **Pouvoir de la pièce** : utilise le pouvoir spécial de la pièce (voir Bloc 16).
> - **Interroger** (1 ☕) : voir Bloc 10.
> - **Échanger** : si un autre détective est dans ta pièce, négociez des cartes ou du ☕ (en anglais !).
> - **Accuser** : seulement dans la Bibliothèque (voir Bloc 13).

🎛 **Levier modifiable** : liste des actions, coûts, conditions.
- *Alternative A* : **Échanger** ne compte pas comme une action (on peut échanger en plus).
- *Alternative B* : nouvelle action **« Filature »** : suivre un autre détective et regarder la carte qu'il vient de piocher.

✏️ **Notre version :**

> 

🎨 Impact design : livret (Actions), plateau (barre latérale).

---

## BLOC 6 : ③ Requêtes et économie du café ☕

📜 **Règle**
> Chaque requête sur ton téléphone coûte **1 ☕**. Les résultats sont **privés**. Tu peux faire autant de requêtes que tu peux en payer. La réserve contient **30 jetons ☕**. On gagne du café dans la Cuisine (+2), le Grand Hall (+1), avec les cartes Café et certains événements.

🎛 **Levier modifiable** : prix d'une requête, réserve de café, maximum en main.
- *Alternative A* : requête simple = 1 ☕, requête avec **`JOIN` = 2 ☕** (mais elle remplace 3 requêtes).
- *Alternative B* : **maximum 5 ☕** en main, pour éviter qu'un joueur accumule trop.
- *Alternative C* : **1 seule requête** par tour, mais gratuite.

✏️ **Notre version :**

> 

🎨 Impact design : livret (Requêtes + aide-mémoire), jetons café (nombre), plateau (réserve de café), cartes Café.

---

## BLOC 7 : Les cartes indices (60 cartes)

📜 **Règle**
> | Type | Qté | Effet |
> |---|---|---|
> | 🔑 Mot-clé (Keyword) | 16 | Débloque un mot-clé : `WHERE` ×4, `AND` ×3, `OR` ×2, `NOT` ×2, `JOIN` ×3, `=`/`≠` ×2 |
> | 🗂 Table | 8 | Débloque une table : `TIMELINE`, `ITEMS`, `SECRETS`, `CALLS` (×2 chacune) |
> | 🔬 Preuve (Evidence) | 12 | Révèle un indice scientifique pour cette affaire |
> | ☕ Café | 12 | Espresso ×8 (+1 ☕), Double Shot ×4 (+2 ☕) |
> | ⚡ Rebondissement (Twist) | 12 | Porte secrète, Café renversé, Témoin, Chat noir, Courant d'air, Second souffle (×2 chacun) |
>
> Une carte scannée est **défaussée** (l'app s'en souvient). Les cartes non scannées peuvent être gardées en main et **échangées**.
>
> Détail des rebondissements :
> - **Porte secrète** : va immédiatement dans n'importe quelle pièce.
> - **Café renversé** : oups ! Perds 1 ☕.
> - **Témoin** : interroge un suspect gratuitement.
> - **Chat noir** : échange ta place avec un autre détective de ton choix.
> - **Courant d'air** : une fenêtre claque, déplace-toi d'1 pièce.
> - **Second souffle** : fais une action de plus ce tour-ci.

🎛 **Levier modifiable** : quantités, nouveaux types, nouvelles cartes Rebondissement.
- *Alternative A* : moins de cartes Café (8) et plus de Preuves (16), pour plus d'enquête.
- *Alternative B* : nouveaux rebondissements inventés par vous, par exemple *« Panne : tous les joueurs perdent 1 ☕ »* ou *« Alibi : protège un suspect de ton carnet »*.

✏️ **Notre version :**

> 

🎨 Impact design : **cartes** (faces, dos, PDF d'impression, QR codes), livret (Les cartes).

---

## BLOC 8 : Débloquer le SQL sur le téléphone

📜 **Règle**
> Au départ, ta console ne peut lancer que `SELECT * FROM guests` (afficher la liste des invités). **Scanne une carte Mot-clé** pour débloquer ce bloc, et **scanne une carte Table** pour débloquer cette table, **pour toi seulement**. Les blocs verrouillés affichent un 🔒.

🎛 **Levier modifiable** : ce qui est débloqué au départ, déblocage personnel ou partagé.
- *Alternative A* : `WHERE` et `TIMELINE` sont **débloqués dès le départ**, pour les débutants.
- *Alternative B* : une carte scannée débloque le mot-clé **pour toute la table**, mais celui qui scanne gagne 1 ☕.

✏️ **Notre version :**

> 

🎨 Impact design : app surtout, livret (Console de police), carnet du détective (cases « débloqué »).

---

## BLOC 9 : Les données corrompues

📜 **Règle**
> Certaines cases de la base de données affichent `████ CORRUPTED`. La plupart sont dues à l'orage, mais **l'une d'elles a été effacée par le meurtrier**. Utilise le pouvoir de la **Salle des serveurs** pour restaurer une donnée.

🎛 **Levier modifiable** : nombre de cases corrompues, façon de les réparer.
- *Alternative A* : réparer coûte **2 ☕** mais peut se faire **depuis n'importe quelle pièce**.
- *Alternative B* : une réparation restaure la case **pour tous les joueurs** (et pas seulement pour toi).

✏️ **Notre version :**

> 

🎨 Impact design : livret, plateau (Salle des serveurs), app.

---

## BLOC 10 : Les interrogatoires

📜 **Règle**
> **Interroger** coûte **1 ☕** (gratuit dans la Chapelle). Choisis un suspect dans l'app et **lis sa déclaration à voix haute** aux autres joueurs. Les déclarations peuvent être des **mensonges** : le meurtrier ment toujours, et certains innocents mentent aussi. Vérifie-les avec des requêtes !

🎛 **Levier modifiable** : coût, nombre d'interrogatoires par suspect, façon de lire.
- *Alternative A* : chaque suspect a **2 déclarations**. La 2ᵉ ne se débloque qu'avec une carte Preuve liée.
- *Alternative B* : le joueur doit **jouer le personnage avec un accent** ; s'il le fait, les autres votent pour lui offrir 1 ☕ (bonus d'anglais oral).

✏️ **Notre version :**

> 

🎨 Impact design : app, livret (Actions + phrases à dire).

---

## BLOC 11 : Fin de manche et horloge

📜 **Règle**
> Quand tout le monde a joué, le téléphone de l'hôte avance l'horloge de **30 minutes** et déclenche un **événement d'orage**. La partie dure **8 manches**, de **minuit à 4h du matin** (l'aube).

🎛 **Levier modifiable** : nombre de manches, durée par manche.
- *Alternative A* : **10 manches** (de minuit à 5h) pour une partie plus longue.
- *Alternative B* : un **chrono réel** dans l'app, par exemple 4 minutes par manche quel que soit le nombre de tours joués.

✏️ **Notre version :**

> 

🎨 Impact design : **plateau** (cadran de l'horloge avec 8 cases), jeton horloge, livret (L'horloge).

---

## BLOC 12 : Les événements d'orage

📜 **Règle**
> Un événement au hasard par manche, tiré par l'app :
> - **Coupure de courant** : les requêtes coûtent +1 ☕ cette manche.
> - **Coup de tonnerre** : chaque détective se déplace d'1 pièce.
> - **Cloche de minuit** : tout le monde gagne 1 ☕.
> - **Fantôme dans le couloir** : passages secrets fermés cette manche.
> - **Données récupérées** : 1 donnée corrompue est restaurée pour tous.
> - **Porte verrouillée** : une pièce est fermée cette manche.
> - **Ragots au bar** : chacun peut donner 1 carte à son voisin de gauche.
> - **Nuit silencieuse** : rien ne se passe… suspect.

🎛 **Levier modifiable** : liste des événements, fréquence.
- *Alternative A* : un événement **toutes les 2 manches** seulement.
- *Alternative B* : inventez vos événements, par exemple *« Le meurtrier frappe encore : un suspect disparaît de la liste »*.

✏️ **Notre version :**

> 

🎨 Impact design : app, livret (Événements d'orage). Aucune carte physique.

---

## BLOC 13 : L'accusation finale

📜 **Règle**
> Va dans la **Bibliothèque**. Accuser compte comme ton action. Sur ton téléphone, choisis **Suspect + Arme + Mobile**, puis annonce-le **à voix haute en anglais** :
> *"I accuse ___! He/She was in the Library at ___, with ___, because ___!"*
> (« J'accuse ___ ! Il/Elle était dans la Bibliothèque à ___, avec ___, parce que ___ ! »)
> L'app révèle le résultat. Le meurtrier est le **seul** suspect qui réunit les 3 preuves : 🕰 **l'Occasion** (Opportunity), 🧪 **le Moyen** (Means), 💔 **le Mobile** (Motive).

🎛 **Levier modifiable** : où accuser, ce qu'il faut nommer.
- *Alternative A* : accuser **depuis n'importe quelle pièce**, mais il faut avoir **2 ☕**.
- *Alternative B* : il faut aussi **montrer la requête SQL** qui prouve l'accusation (l'app la vérifie).

✏️ **Notre version :**

> 

🎨 Impact design : livret (Accusation finale), plateau (encart *Solve the case*), app.

---

## BLOC 14 : Mauvaise accusation

📜 **Règle**
> Si tu te trompes, tu es **SUSPENDU** : tu perds tout ton ☕ et tu passes tes **2 prochains tours**. Tu restes dans la partie (tu peux toujours échanger, et les autres peuvent t'espionner).

🎛 **Levier modifiable** : dureté de la sanction.
- *Alternative A* : **éliminé**, mais tu deviens le « fantôme de Victor » et tu peux donner un indice par manche.
- *Alternative B* : plus doux : **1 tour passé**, et l'app te dit lequel des 3 éléments était faux.

✏️ **Notre version :**

> 

🎨 Impact design : jetons SUSPENDED (×4), livret.

---

## BLOC 15 : Fin de partie

📜 **Règle**
> Le premier détective qui fait une accusation correcte **gagne**. Si personne n'a trouvé après la manche 8 (l'aube), la police arrive, **le meurtrier s'enfuit et tout le monde perd**.

🎛 **Levier modifiable** : condition de victoire, système de points.
- *Alternative A* : **points** : 5 pts pour l'accusation, +1 par preuve trouvée en premier. Utile si vous voulez départager plusieurs gagnants.
- *Alternative B* : à l'aube, chacun fait une accusation secrète et **le plus proche gagne**.

✏️ **Notre version :**

> 

🎨 Impact design : livret, plateau (barre latérale).

---

## BLOC 16 : Les pièces et leurs pouvoirs

📜 **Règle**
> | Pièce | Pioche ? | Pouvoir (à la place de fouiller) |
> |---|---|---|
> | Grand Hall | ✗ | Pièce de départ. *Ragots* : prends 1 ☕. |
> | Bibliothèque (Library) | ✓ | Scène de crime. Seul endroit où l'on peut **accuser**. |
> | Salle des serveurs (Server Room) | ✗ | *Restauration* : répare 1 donnée corrompue. |
> | Cuisine (Kitchen) | ✓ | *Pause café* : prends 2 ☕. |
> | Observatoire (Observatory) | ✓ | *Télescope* : regarde les 2 premières cartes d'une pioche et remets-les dans l'ordre de ton choix. |
> | Salon de musique (Music Room) | ✓ | *Écoute indiscrète* : un autre détective te montre le résultat de sa dernière requête. |
> | Chapelle (Chapel) | ✓ | *Confession* : interroge gratuitement. |
> | Serre (Greenhouse) | ✓ | *Main verte* : en fouillant, pioche 2 cartes et garde-en 1. |
> | Cave à vin (Wine Cellar) | ✓ | *Tunnels* : au prochain tour, déplace-toi dans n'importe quelle pièce. |

🎛 **Levier modifiable** : pouvoirs, noms des pièces, pièces en plus ou en moins.
- *Alternative A* : **Écoute indiscrète** devient « vole 1 carte non scannée à un détective dans une pièce voisine ».
- *Alternative B* : remplacer une pièce par une **pièce à vous** (Garage, Grenier…) avec votre propre pouvoir.

✏️ **Notre version :**

> 

🎨 Impact design : **plateau** (plaques des pièces avec pouvoir, décor), dos de cartes par pièce, livret (Pouvoirs des pièces).

---

## BLOC 17 : Les détectives et leurs pouvoirs

📜 **Règle**
> | Détective | Pouvoir |
> |---|---|
> | **Inspecteur Rusty Holloway** (vétéran grincheux) | *Vieille école* : une fois par manche, interroge gratuitement. |
> | **Ada « Null » Byte** (hackeuse ado) | *Overclock* : ta première requête de chaque manche coûte 0 ☕. |
> | **Professeure Iris Lumen** (médecin légiste) | *Loupe* : quand tu fouilles, pioche 2 cartes et garde-en 1. |
> | **Agent Kit Marlowe** (ancien sprinteur) | *Sprint* : déplace-toi jusqu'à 3 pièces. |

🎛 **Levier modifiable** : noms, personnalités, pouvoirs. **Idée : chaque membre du groupe crée son propre détective.**
- *Alternative A* : un détective « **Linguiste** » : quand il lit un interrogatoire, il sait si c'est un mensonge, 1 fois par partie.
- *Alternative B* : chaque détective a un **pouvoir + un défaut** (par ex. Kit avance de 3 mais ne peut pas faire de JOIN).

✏️ **Notre version :**

> 

🎨 Impact design : **cartes Détective** (×4), **figurines** (pions), carnet, livret (Matériel).

---

## BLOC 18 : Les suspects et l'affaire tutoriel

📜 **Règle**
> 8 suspects : Margaret (l'épouse, botaniste), Felix (médecin), Ivy (la nièce, hackeuse), Bram (colonel), Sofia (chanteuse d'opéra), Gideon (majordome), Oscar (directeur technique), Nora (journaliste).
> Affaire tutoriel *« The Foxglove Tea »* (le thé à la digitale) : thé empoisonné, **Oscar** est le meurtrier. Toutes les tables, indices et déclarations sont dans `Data_Detective_Game_Design.md` §13.

🎛 **Levier modifiable** : noms, métiers, coupable, arme, mobiles, mensonges.
- *Alternative A* : faire de **vous trois** des suspects (avec vos vrais prénoms), c'est drôle en démo devant la classe.
- *Alternative B* : changer le coupable pour surprendre ceux qui ont lu le document.

✏️ **Notre version :**

> 

🎨 Impact design : carnet du détective (liste des 8 suspects), plateau (indices dessinés : empreintes « SIZE 44? », digitale, thé), app (données), livret (exemples).

---

## BLOC 19 : Vos idées en plus (règles libres)

Tout ce qui n'entre pas ailleurs : règles maison, mini-défis d'anglais, bonus, variantes pour enfants ou experts…

✏️ **Nos idées :**

> 
