> ⚠️ **Obsolète** : remplacé par la V2 simplifiée (`Regles_V2_Simplifiees.md` et `Data_Detective_Game_Design.md`). Gardé pour mémoire.

# THE LAST QUERY : déroulé des règles à personnaliser

**Mode d'emploi pour le groupe**
- Chaque bloc suit une partie dans l'ordre, du début à la fin.
- **📜 Rule** : la règle actuelle (en anglais, c'est le texte du jeu).
- **🎛 Levier modifiable** : ce qu'on peut changer, avec des idées d'alternatives.
- **✏️ Notre version** : à vous de remplir. Laissez vide si la règle vous va, écrivez « supprimé » pour enlever la règle.
- **🎨 Impact design** : les fichiers de `DA/` à refaire si vous changez ce bloc. C'est utile pour savoir ce que coûte une modification.

---

## BLOC 0 : Carte d'identité du jeu

📜 **Rule**
> *The Last Query* is a competitive deduction game for **2–4 detectives** (or teams of 2), ages **12+**, about **40–60 minutes**. Explore the manor on the board, unlock SQL on your phone, and name the killer before dawn.

🎛 **Levier modifiable** : nombre de joueurs, durée, compétitif ou coopératif.
- *Alternative A* : **mode coopératif**. Tout le monde enquête ensemble contre l'horloge, et les résultats de requêtes sont partagés.
- *Alternative B* : jusqu'à **6 joueurs** en ajoutant 2 détectives.

✏️ **Notre version :**

> 

🎨 Impact design : couverture du livret, boîte, board (sidebar), cartes Détective si joueurs en plus.

---

## BLOC 1 : L'histoire de départ

📜 **Rule**
> Sir Victor Ravenscroft, founder of *Ravenscroft Analytics*, is found dead in the **Library** at **11:45 PM** during his 70th birthday party. Lightning shattered the database of the smart house AI **W.A.T.S.O.N.** into **Data Shards**. The storm cuts the bridge: the police arrive at **dawn**. If nobody solves the case by then, **the killer escapes and everyone loses**.

🎛 **Levier modifiable** : noms, lieu, époque, nom de l'IA, heure du crime, ton (plus drôle, plus sombre).
- *Alternative A* : l'IA s'appelle autrement, ou elle est un personnage qui « parle » dans l'app.
- *Alternative B* : changer la victime ou le lieu (un paquebot, un train de nuit…).

✏️ **Notre version :**

> 

🎨 Impact design : livret (p. 2), board (horloge arrêtée à 11:45, décor), logo seulement si le nom change.

---

## BLOC 2 : Mise en place (Setup)

📜 **Rule**
> 1. The host opens the app, chooses a **case** and gets a **game code** (e.g. `RAVEN-42`). Other players join with their phones.
> 2. Sort the 60 clue cards by the room on their back, shuffle each pile, and place it face down on its room (7 rooms have a deck).
> 3. Each player takes a detective, puts their pawn in the **Grand Hall** and takes **3 ☕**.
> 4. Put the clock token on **12:00 AM**.
> 5. The youngest player starts.

🎛 **Levier modifiable** : café de départ, point de départ, premier joueur, cartes en main au départ.
- *Alternative A* : chaque joueur commence avec **1 carte Keyword `WHERE`** déjà débloquée, pour accélérer le début.
- *Alternative B* : chacun démarre dans une **pièce différente**. Le premier joueur est « celui qui a lu un polar le plus récemment ».

✏️ **Notre version :**

> 

🎨 Impact design : livret (Setup), board (médaillons P1–P4 dans le Grand Hall), jetons café.

---

## BLOC 3 : Structure d'un tour

📜 **Rule**
> On your turn, do 3 steps in order: **① MOVE → ② ACT (one action) → ③ QUERY (optional)**.

🎛 **Levier modifiable** : nombre d'étapes et d'actions par tour.
- *Alternative A* : **2 actions** par tour au lieu d'une (partie plus rapide).
- *Alternative B* : on peut faire QUERY **à tout moment**, même pendant le tour des autres.

✏️ **Notre version :**

> 

🎨 Impact design : livret (A Turn + quick reference), board (résumé du tour dans la sidebar).

---

## BLOC 4 : ① MOVE (se déplacer)

📜 **Rule**
> Move up to **2 rooms** along corridors. A **secret passage** counts as 1 move (Wine Cellar ⇄ Observatory, Greenhouse ⇄ Chapel). You may also stay.

🎛 **Levier modifiable** : distance, dé ou pas, passages secrets.
- *Alternative A* : on lance un **dé** (1–2 = 1 pièce, 3–5 = 2 pièces, 6 = n'importe où).
- *Alternative B* : déplacement **gratuit de 1 pièce**, et chaque pièce en plus coûte 1 ☕.

✏️ **Notre version :**

> 

🎨 Impact design : livret, board si les passages secrets changent (trappes rouges).

---

## BLOC 5 : ② ACT (une action au choix)

📜 **Rule**
> Choose **ONE**:
> - **Search**: draw the top card of the room's deck.
> - **Room Power**: use the room's special power (see Bloc 16).
> - **Interrogate** (1 ☕): see Bloc 10.
> - **Trade**: if another detective is in your room, negotiate cards or ☕ (in English!).
> - **Accuse**: only in the Library (see Bloc 13).

🎛 **Levier modifiable** : liste des actions, coûts, conditions.
- *Alternative A* : **Trade** ne compte pas comme une action (on peut échanger en plus).
- *Alternative B* : nouvelle action **« Shadow »** : suivre un autre détective et regarder la carte qu'il vient de piocher.

✏️ **Notre version :**

> 

🎨 Impact design : livret (Actions), board (sidebar).

---

## BLOC 6 : ③ QUERY et économie du café ☕

📜 **Rule**
> Each query on your phone costs **1 ☕**. Results are **private**. You can run as many queries as you can pay for. There are **30 ☕ tokens** in the bank. You get coffee from the Kitchen (+2), the Grand Hall (+1), Coffee cards and some events.

🎛 **Levier modifiable** : prix d'une requête, réserve de café, maximum en main.
- *Alternative A* : requête simple = 1 ☕, requête avec **`JOIN` = 2 ☕** (mais elle remplace 3 requêtes).
- *Alternative B* : **maximum 5 ☕** en main, pour éviter qu'un joueur accumule trop.
- *Alternative C* : **1 seule requête** par tour, mais gratuite.

✏️ **Notre version :**

> 

🎨 Impact design : livret (Query + quick reference), jetons café (nombre), board (coffee bank), cartes Coffee.

---

## BLOC 7 : Les cartes indices (60 cartes)

📜 **Rule**
> | Type | Qty | Effect |
> |---|---|---|
> | 🔑 Keyword | 16 | Unlock a keyword: `WHERE` ×4, `AND` ×3, `OR` ×2, `NOT` ×2, `JOIN` ×3, `=`/`≠` ×2 |
> | 🗂 Table | 8 | Unlock a table: `TIMELINE`, `ITEMS`, `SECRETS`, `CALLS` (×2 each) |
> | 🔬 Evidence | 12 | Reveal a forensic clue for this case |
> | ☕ Coffee | 12 | Espresso ×8 (+1 ☕), Double Shot ×4 (+2 ☕) |
> | ⚡ Twist | 12 | Secret Door, Spilled Coffee, Witness, Black Cat, Cold Draft, Second Wind (×2 each) |
>
> A scanned card is **discarded** (the app remembers it). Unscanned cards can be kept in hand and **traded**.

🎛 **Levier modifiable** : quantités, nouveaux types, nouvelles cartes Twist.
- *Alternative A* : moins de cartes Coffee (8) et plus d'Evidence (16), pour plus d'enquête.
- *Alternative B* : nouvelles Twist inventées par vous, par exemple *« Blackout : all players lose 1 ☕ »* ou *« Alibi : protect one suspect from your notebook »*.

✏️ **Notre version :**

> 

🎨 Impact design : **cartes** (faces, dos, PDF d'impression, QR codes), livret (The Cards).

---

## BLOC 8 : Débloquer le SQL sur le téléphone

📜 **Rule**
> At the start, your console can only run `SELECT * FROM guests`. **Scan a Keyword card** to unlock that block, and **scan a Table card** to unlock that table, **for you only**. Locked blocks show a 🔒.

🎛 **Levier modifiable** : ce qui est débloqué au départ, déblocage personnel ou partagé.
- *Alternative A* : `WHERE` et `TIMELINE` sont **débloqués dès le départ**, pour les débutants.
- *Alternative B* : une carte scannée débloque le mot-clé **pour toute la table**, mais celui qui scanne gagne 1 ☕.

✏️ **Notre version :**

> 

🎨 Impact design : app surtout, livret (Police Console), carnet du détective (cases « unlocked »).

---

## BLOC 9 : Les données corrompues

📜 **Rule**
> Some cells in the database show `████ CORRUPTED`. Most are noise from the storm, but **one was erased by the killer**. Use the **Server Room** power to restore one record.

🎛 **Levier modifiable** : nombre de cases corrompues, façon de les réparer.
- *Alternative A* : réparer coûte **2 ☕** mais peut se faire **depuis n'importe quelle pièce**.
- *Alternative B* : une réparation restaure la case **pour tous les joueurs** (et pas seulement pour vous).

✏️ **Notre version :**

> 

🎨 Impact design : livret, board (Server Room), app.

---

## BLOC 10 : Les interrogatoires

📜 **Rule**
> **Interrogate** costs **1 ☕** (free in the Chapel). Pick a suspect in the app and **read their statement out loud** to the table. Statements can be **lies**: the killer always lies, and some innocents lie too. Check them with queries!

🎛 **Levier modifiable** : coût, nombre d'interrogatoires par suspect, façon de lire.
- *Alternative A* : chaque suspect a **2 déclarations**. La 2ᵉ ne se débloque qu'avec une carte Evidence liée.
- *Alternative B* : le joueur doit **jouer le personnage avec un accent** ; s'il le fait, les autres votent pour lui offrir 1 ☕ (bonus d'anglais oral).

✏️ **Notre version :**

> 

🎨 Impact design : app, livret (Actions + table talk).

---

## BLOC 11 : Fin de manche et horloge

📜 **Rule**
> When everyone has played, the host phone advances the clock by **30 minutes** and triggers a **Storm Event**. The game lasts **8 rounds**, from **12:00 AM to 4:00 AM** (dawn).

🎛 **Levier modifiable** : nombre de manches, durée par manche.
- *Alternative A* : **10 manches** (de minuit à 5:00 AM) pour une partie plus longue.
- *Alternative B* : un **chrono réel** dans l'app, par exemple 4 minutes par manche quel que soit le nombre de tours joués.

✏️ **Notre version :**

> 

🎨 Impact design : **board** (cadran de l'horloge avec 8 cases), jeton horloge, livret (The Clock).

---

## BLOC 12 : Les événements d'orage

📜 **Rule**
> One random event per round, drawn by the app:
> Power Flicker (queries cost +1 ☕) · Thunderclap (everyone moves 1 room) · Midnight Bell (everyone +1 ☕) · Ghost in the Corridor (secret passages closed) · Data Recovered (1 corrupted record restored for all) · Locked Door (one room closed) · Gossip at the Bar (give 1 card to your left) · Silent Night (nothing… suspicious).

🎛 **Levier modifiable** : liste des événements, fréquence.
- *Alternative A* : un événement **toutes les 2 manches** seulement.
- *Alternative B* : inventez vos événements, par exemple *« The killer strikes again: one suspect disappears from the list »*.

✏️ **Notre version :**

> 

🎨 Impact design : app, livret (Storm Events). Aucune carte physique.

---

## BLOC 13 : L'accusation finale

📜 **Rule**
> Go to the **Library**. Accusing is your action. On your phone, choose **Suspect + Weapon + Motive**, then say it **out loud in English**:
> *"I accuse ___! He/She was in the Library at ___, with ___, because ___!"*
> The app reveals the result. The killer is the **only** suspect with all 3 proofs: 🕰 **Opportunity**, 🧪 **Means**, 💔 **Motive**.

🎛 **Levier modifiable** : où accuser, ce qu'il faut nommer.
- *Alternative A* : accuser **depuis n'importe quelle pièce**, mais il faut avoir **2 ☕**.
- *Alternative B* : il faut aussi **montrer la requête SQL** qui prouve l'accusation (l'app la vérifie).

✏️ **Notre version :**

> 

🎨 Impact design : livret (Final Accusation), board (encart *Solve the case*), app.

---

## BLOC 14 : Mauvaise accusation

📜 **Rule**
> If you are wrong, you are **SUSPENDED**: lose all your ☕ and skip your next **2 turns**. You stay in the game (you can still trade, and others can eavesdrop on you).

🎛 **Levier modifiable** : dureté de la sanction.
- *Alternative A* : **éliminé**, mais tu deviens le « fantôme de Victor » et tu peux donner un indice par manche.
- *Alternative B* : plus doux : **1 tour passé**, et l'app te dit lequel des 3 éléments était faux.

✏️ **Notre version :**

> 

🎨 Impact design : jetons SUSPENDED (×4), livret.

---

## BLOC 15 : Fin de partie

📜 **Rule**
> The first detective with a correct accusation **wins**. If nobody has solved it after round 8 (dawn), the police arrive, **the killer escapes, and everyone loses**.

🎛 **Levier modifiable** : condition de victoire, système de points.
- *Alternative A* : **points** : 5 pts pour l'accusation, +1 par preuve trouvée en premier. Utile si vous voulez départager plusieurs gagnants.
- *Alternative B* : à l'aube, chacun fait une accusation secrète et **le plus proche gagne**.

✏️ **Notre version :**

> 

🎨 Impact design : livret, board (sidebar).

---

## BLOC 16 : Les pièces et leurs pouvoirs

📜 **Rule**
> | Room | Deck? | Power (instead of searching) |
> |---|---|---|
> | Grand Hall | ✗ | Start room. *Gossip*: take 1 ☕. |
> | Library | ✓ | Crime scene. Only place to **accuse**. |
> | Server Room | ✗ | *Restore*: repair 1 corrupted record. |
> | Kitchen | ✓ | *Coffee Break*: take 2 ☕. |
> | Observatory | ✓ | *Telescope*: look at the top 2 cards of any deck and reorder them. |
> | Music Room | ✓ | *Eavesdrop*: another detective shows you their last query result. |
> | Chapel | ✓ | *Confession*: interrogate for free. |
> | Greenhouse | ✓ | *Green Thumb*: search, draw 2, keep 1. |
> | Wine Cellar | ✓ | *Tunnels*: next turn, move to any room. |

🎛 **Levier modifiable** : pouvoirs, noms des pièces, pièces en plus ou en moins.
- *Alternative A* : **Eavesdrop** devient « vole 1 carte non scannée à un détective dans une pièce voisine ».
- *Alternative B* : remplacer une pièce par une **pièce à vous** (Garage, Attic…) avec votre propre pouvoir.

✏️ **Notre version :**

> 

🎨 Impact design : **board** (plaques des pièces avec pouvoir, décor), dos de cartes par pièce, livret (Room Powers).

---

## BLOC 17 : Les détectives et leurs pouvoirs

📜 **Rule**
> | Detective | Power |
> |---|---|
> | **Inspector Rusty Holloway** (grumpy veteran) | *Old School*: once per round, interrogate for free. |
> | **Ada "Null" Byte** (teen hacker) | *Overclock*: your first query each round costs 0 ☕. |
> | **Professor Iris Lumen** (forensic scientist) | *Magnifier*: when you search, draw 2 and keep 1. |
> | **Agent Kit Marlowe** (ex-sprinter) | *Sprint*: move up to 3 rooms. |

🎛 **Levier modifiable** : noms, personnalités, pouvoirs. **Idée : chaque membre du groupe crée son propre détective.**
- *Alternative A* : un détective « **Linguist** » : quand il lit un interrogatoire, il sait si c'est un mensonge 1 fois par partie.
- *Alternative B* : chaque détective a un **pouvoir + un défaut** (par ex. Kit avance de 3 mais ne peut pas faire de JOIN).

✏️ **Notre version :**

> 

🎨 Impact design : **cartes Détective** (×4), **standees** (pions), carnet, livret (Components).

---

## BLOC 18 : Les suspects et l'affaire tutoriel

📜 **Rule**
> 8 suspects: Margaret (wife, botanist), Felix (doctor), Ivy (niece, hacker), Bram (colonel), Sofia (opera singer), Gideon (butler), Oscar (CTO), Nora (journalist).
> Tutorial case *"The Foxglove Tea"*: poisoned tea, **Oscar** is the killer. All tables, clues and statements are in `Data_Detective_Game_Design.md` §13.

🎛 **Levier modifiable** : noms, métiers, coupable, arme, mobiles, mensonges.
- *Alternative A* : faire de **vous trois** des suspects (avec vos vrais prénoms), c'est drôle en démo devant la classe.
- *Alternative B* : changer le coupable pour surprendre ceux qui ont lu le document.

✏️ **Notre version :**

> 

🎨 Impact design : carnet du détective (liste des 8 suspects), board (indices dessinés : empreintes « SIZE 44? », foxglove, thé), app (données), livret (exemples).

---

## BLOC 19 : Vos idées en plus (règles libres)

Tout ce qui n'entre pas ailleurs : règles maison, mini-défis d'anglais, bonus, variantes pour enfants ou experts…

✏️ **Nos idées :**

> 
