# THE LAST QUERY : retours du playtest n°1 (2026-11-25)

Statuts : ⬜ à faire · 🔄 en cours · ✅ fait · ❓ à trancher avec le groupe.
**Point au 2026-11-25 : tout est fait.** L'app est testée en local à 375 px (hôte + invité) et **redéployée sur GitHub Pages** (commit `e0174dd` sur Oozudex/FunnelRush), vérifiée en ligne à 375 px.
Les textes du jeu restent en anglais. Codes des cartes inchangés (`LIB-01` … `CEL-06`, QR `TLQ:<code>`).

---

## Règles

### R1 ✅ 1 seule carte par tour (✔ validé le 2026-11-25 · fait : game design, règles V2, source du livret, app. PDF du livret régénéré), et on peut piocher en cours de déplacement
**Retour :** pendant un tour, on ne scanne qu'une carte. Soit on traverse 2 pièces et on pioche dans la 2ᵉ, soit on s'arrête dans la 1ʳᵉ, on pioche, puis on finit son déplacement.
**Proposition (texte du livret) :**
> **① MOVE & SEARCH**: move up to **2 rooms**. Once during your move (before, in the middle or at the end), you may **search the room you are in: draw 1 card**.
> **② or, instead of searching**: **Recharge** *(Server Room)* or **Accuse** *(Library)*.

- Le tour reste à 2 étapes, mais « Search » se fait pendant le déplacement.
- Effet sur l'équilibre : on pioche 2 fois moins vite. Les mises à jour W.A.T.S.O.N. (manches 4, 8, 12) gardent la partie courte. À revoir après le playtest 2.
- **Impacts :** `Data_Detective_Game_Design.md` §5, `Regles_V2_Simplifiees.md` §4, livret (`DA/tools/build_rules.py`, page « Your turn »), carnet (`DA/tokens/build_tokens.py`, si le rappel du tour y figure), **app** (A2).

### R2 ✅ 1 seule requête par tour
**Retour :** une mauvaise manipulation a consommé 2 jetons.
**Proposition :** *"QUERY: once per turn, pay 1 token to run one search (up to 2 conditions)."*
- **Impacts :** game design §5 et §7, règles V2 §4 et §7, livret (pages « Your turn » et « Police Console »), **app** (A3).

### R3 ✅ Les cartes Bonus se gardent et se jouent quand on veut
**Proposition :** *"Keep Bonus cards face up in front of you. Play one at any time **on your turn** (it is not your action), then discard it."*
- Spare Battery : +1 token (max 3). Running Shoes : déplacement de 2 pièces en plus. Master Key : regarder la carte du dessus d'une pioche.
- **Impacts :** game design §6, règles V2 §5, livret (page « The clues »), **cartes Bonus** (ajouter *"Keep this card. Play it on your turn."*), **app** (A4).

### R4 ✅ Que faire des cartes une fois tirées ?
**Proposition :** *"After scanning, keep the card **face down in front of you**. Never put it back. The app remembers it too (tab Clues)."* Les cartes Bonus restent face visible jusqu'à leur utilisation (R3).
- **Impacts :** game design §5, règles V2 §4, livret (« Your turn » et « The clues »), dos des cartes (rappel court, optionnel).

### R5 ✅ Indices contradictoires (blond / roux) : rendre les fausses pistes plus claires
**Question du groupe :** « On a eu une carte cheveux blonds et une carte cheveux roux. » **Réponse :** c'est voulu. *Sugar bowl* (Kitchen, roux) est une fausse piste 🎭 posée par le tueur. Le blond apparaît 3 fois (Observatory, Music Room, Wine Cellar), le roux une seule.
**Proposition :** l'expliquer avec cet exemple dans le livret (*"Two clues disagree? One is planted. Find the one you see twice."*). L'app le signale aussi (A5).
- **Impacts :** livret (page « The clues & golden rules »), règles V2 §5, **app** (A5).

### R6 ✅ Plusieurs histoires (affaires) : comment ça marche ? (✔ choix **a** : une seule affaire pour le moment · fait : game design et règles V2. Le livret et l'app ne promettaient rien)
**Question du groupe.** **Réponse :** les cartes n'impriment que **l'objet** (« Muddy footprint · Greenhouse »). C'est l'app qui dit ce que l'objet révèle **dans l'affaire choisie**. Une autre affaire, c'est donc un autre tueur et d'autres révélations avec les mêmes 40 cartes. Aujourd'hui, seule l'affaire 1 (*The Foxglove Tea*) existe.
**Options :**
- **a.** Garder une seule affaire et retirer la promesse « plusieurs histoires » du livret. Le plus simple.
- **b.** Expliquer le principe en 2 lignes dans le livret et ajouter un sélecteur d'affaire dans la salle d'attente, sans écrire de 2ᵉ affaire.
- **c.** Écrire une affaire 2 complète (tueur, 40 révélations, 3 mises à jour) et ajouter le sélecteur.
- **Impacts :** livret, game design §6 et §9, **app** (`src/engine/cases/`, `Lobby.tsx`).

---

## Design / impression

### D1 ✅ Mettre le livret à jour (R1 à R6)
- Fichier : `DA/tools/build_rules.py` puis rendu `DA/rules/*.pdf` (A5, fond perdu de 3 mm, traits de coupe, 300 DPI).

### D2 ✅ Cartes Bonus : mention « Keep this card »
- Pour les cartes V2 63 × 88 mm (`DA/tools/build_print.py`) et pour les futures cartes V3 50 × 85 mm (`DA_V3/`), mêmes codes.
- Fait sur les cartes V2 : l'effet reste imprimé en clair, et un **QR + code de secours** est ajouté (la carte se scanne pour être gardée dans l'app), avec la mention *"Keep it face up · play it on your turn"*. Les cartes V3 (`DA_V3/`) devront reprendre ce QR : c'est noté dans `DA_V3/README.md`.

### D3 ✅ Carnet : rappel du tour et règle d'or (si R1, R2 et R5 sont validés)
- Fichier : `DA/tools/build_tokens.py` (carnet A5 recto verso).

---

## App

### A1 ✅ Bug : il faut parfois faire F5 au changement de joueur
**Cause probable :** l'hôte n'envoie l'état de la partie qu'au moment où il change. Si un relais MQTT perd ce message (les abonnements sont en QoS 0) ou si le téléphone était en veille, le téléphone garde l'ancien état et rien ne le renvoie.
**Proposition :** numéroter chaque état (révision). L'hôte met la révision dans son ping toutes les 4 s, et un téléphone en retard redemande l'état tout seul. Au retour de veille, il redemande aussi l'état. Fichiers : `src/net/room.ts`, `src/engine/game.ts` (compteur), `shared/types.ts`.

### A2 ✅ 1 carte par tour, pioche pendant le déplacement (R1)
- `SCANS_PER_TURN = 1` dans `src/engine/game.ts`. Le guidage du tour (`src/screens/Play.tsx`) devient : « Move up to 2 rooms. Search once on the way: scan 1 card », puis « End my turn ». Recharger et accuser restent l'action du tour à la place de la fouille.

### A3 ✅ 1 requête par tour (R2)
- Le moteur refuse une 2ᵉ requête dans le même tour (`game.ts`). La Police Console affiche « 1 query per turn: used » (`Query.tsx`), avec une confirmation avant de dépenser le jeton.

### A4 ✅ Bonus gardés et joués plus tard (R3)
- Aujourd'hui, la Spare Battery est consommée **dès le scan**. Proposition : le scan ajoute la carte dans « My bonus cards » (`Clues.tsx`), avec un bouton « Play it » (pendant son tour) qui applique l'effet et la marque comme jouée.

### A5 ✅ Signaler les indices contradictoires (R5)
- Dans l'onglet Clues : si deux indices donnent des valeurs différentes pour le même trait, afficher *"These clues disagree: one of them is planted. Trust the one you saw twice."* L'app ne dit jamais lequel est faux.

### A6 ✅ « Peut-être trop de téléphone » : comment l'alléger ? (décision : on laisse comme ça, A2 + A3 suffisent)
**Retour :** trop de temps passé sur le téléphone.
**Options (cumulables) :**
- **a.** A2 + A3 réduisent déjà : 1 scan et 1 requête par tour au maximum.
- **b.** Les cartes **Dead End** et **Bonus** sont imprimées en clair et ne se scannent pas. On ne scanne que les objets qui peuvent être des indices. Inconvénient : moins rejouable et les joueurs reconnaissent les culs-de-sac.
- **c.** Les joueurs qui ne jouent pas posent leur téléphone. L'app affiche un grand écran « X is playing » sans rien à faire, et vibre quand c'est ton tour.
- **d.** Écran de tour simplifié : un seul gros bouton par étape, et les autres onglets en second plan.

### A7 ✅ Pouvoir écrire une requête complète sans avoir tous les indices
**Retour :** aujourd'hui, une colonne reste 🔒 tant qu'aucun indice ne la débloque, donc on ne peut pas tester une requête complète.
**Proposition :** toutes les colonnes et toutes les valeurs sont ouvertes dès le début. Les indices restent affichés comme pense-bête. Fichiers : `src/engine/game.ts` (le contrôle « locked » disparaît), `src/screens/Query.tsx` (plus de 🔒, nouvelle aide), `src/screens/Scan.tsx` (plus de « X is now unlocked »). Livret et game design §7 : rien n'est verrouillé.

---

## Incohérences repérées en relisant (à corriger au passage)
- ✅ `Regles_V2_Simplifiees.md` §5 : la répartition des cartes (8 pièces × 5, des cartes dans la Server Room) ne correspond pas au game design (7 pioches de 5 ou 6 cartes, aucune carte dans la Server Room). Le game design fait foi.
- ✅ `DA/README.md` : cartes en 63 × 88 mm, alors que les cartes V3 en 50 × 85 mm sont en cours.
- ✅ Game design §7 (et livret p. 6, carnet) : il décrit une phrase à trous avec des menus déroulants, alors que l'app fait construire le SQL bloc par bloc (colonnes débloquées par les indices). Il faut mettre le game design à jour avec ce que fait l'app.

---

## Ce qui a été vérifié
- **App (local, 375 px, hôte + invité sur 2 origines)** :
  - 1 seule carte par tour ;
  - 1 seule requête par tour, avec confirmation en 2 appuis ;
  - la Spare Battery est gardée puis jouée (+1 jeton, « played ») ;
  - le changement de joueur arrive sans F5 ;
  - un message perdu volontairement (2 s de coupure côté hôte) est récupéré tout seul en ~5 s ;
  - l'alerte « These clues disagree: Hair » s'affiche avec Sugar bowl (roux) + Piano bench (blond) ;
  - toutes les colonnes sont ouvertes ;
  - aucune erreur console, pas de défilement horizontal.
- **Impression** : cartes (PDF 63 × 88 fond perdu 3 mm, PDF A4 maison, PNG 300 DPI des 6 Bonus, aperçus), livret A5 (fond perdu 3 mm + traits de coupe, et version écran), carnet A5. Tous régénérés avec les mêmes scripts et réglages. Le plateau n'a pas été touché.
- **Redéployé** le 2026-11-25 : `npm run build:pages`, puis copie du projet dans un clone du dépôt et push sur `main`. La version en ligne affiche le nouveau tour.

---

## Nouveau retour (2026-11-26) : jetons de requête physiques

### T1 ✅ Les jetons `;` sortent de l'app : jetons physiques avec un QR au dos (✔ option **A** choisie le 2026-11-26 · fait, **pas encore redéployé**)
**Retour :** « Les jetons pour faire les requêtes, il faut les enlever de l'application. On les met en physique avec des QR codes derrière, et il faudra les scanner pour pouvoir faire une requête. »

**Ce qui change :** l'app ne compte plus les jetons. Pour lancer une requête, on scanne le QR au dos d'un jeton physique (ou on tape son code de secours, par ex. `Q-07`). Un jeton scanné donne une requête, puis il retourne à la **réserve** au milieu de la table. Tout le reste devient physique : 3 jetons au départ (3 au plus), recharge en Server Room, +1 à chaque mise à jour W.A.T.S.O.N., Spare Battery +1, mauvaise accusation = on rend tous ses jetons. La limite d'une requête par tour reste contrôlée par l'app.

**Comment empêcher qu'un jeton serve à l'infini ? (à choisir)**
- **Option A (recommandée) : code unique, bloqué pour le reste de la manche.** 20 jetons `Q-01` … `Q-20`. Quand un jeton est scanné, l'app le refuse jusqu'à la fin de la manche, pour tous les joueurs. Le joueur le remet dans la réserve. Garder un jeton pour le rescanner au tour suivant ne marche donc pas : pendant la manche, il faut un autre jeton. C'est simple, rien à scanner en plus, et la réserve physique fait foi comme l'argent d'un jeu de société.
- **Option B (stricte) : code unique, consommé pour toute la partie.** Un jeton scanné est mort, et on le met dans une boîte « used ». Il faut donc beaucoup plus de jetons (environ 40). La partie peut aussi s'arrêter faute de jetons, et la recharge devient « prendre des jetons neufs ».
- **Option C (la plus simple) : le même QR sur tous les jetons.** L'app ne vérifie rien d'autre que « 1 requête par tour ». Tout repose sur l'honnêteté, comme les billets d'un Monopoly.

**Impacts :**
- **Règles et game design** (`Data_Detective_Game_Design.md` §2, §3, §5, §7 · `Regles_V2_Simplifiees.md` §4, §7) : la réserve de jetons, « scan a token to query, then put it back in the reserve », et la recharge, la mise à jour W.A.T.S.O.N., la Spare Battery et la mauvaise accusation en version physique.
- **Livret** (`DA/tools/build_rules.py`, p. 3 Setup, p. 4 Your turn, p. 6 Police Console) : à régénérer (fond perdu 3 mm, traits de coupe).
- **Planche de jetons** (`DA/tools/build_tokens.py`, `DA/tokens/`) : 20 jetons Ø 20 mm, recto `;` inchangé, **verso = QR `TLQ:Q-07` + code de secours**. Deux PDF :
  1. recto verso A4 (verso en miroir, retourner sur le bord long) ;
  2. une version « à coller » : recto et verso sur la même face, chacun collé d'un côté du carton de 1,5 mm. Pas de souci d'alignement sur une imprimante maison.

  On garde Ø 20 mm pour que les jetons rentrent dans les emplacements de la Server Room sur le plateau V3. Le QR fait alors environ 13 mm. Il se scanne au téléphone de près, et le code de secours marche toujours. Les pions P1 à P4 restent sur la planche.
- **Cartes** : texte de la Spare Battery inchangé (« Take 1 Query Token (max 3) », c'est déjà physique). Dans l'app, « Play it » ne donne plus de jeton : l'app dit seulement « take 1 token from the reserve ».
- **Carnet** : rien à changer (« 1 query per turn = 1 ; » et « +1 ; » aux manches 4, 8, 12 restent vrais).
- **App** :
  - **Moteur** (`src/engine/game.ts`, `shared/types.ts`) : plus de compteur `tokens`. Les codes de jetons sont reconnus, la règle anti-réutilisation choisie est appliquée, et la requête exige un jeton scanné.
  - **Police Console** (`Query.tsx`) : « Run » devient « Scan a token to run » (caméra + code de secours, même écran que les cartes).
  - **Recharge** (`Play.tsx`) : reste l'action du tour en Server Room, avec le texte « take tokens from the reserve up to 3 ».
  - **Messages** : la mise à jour W.A.T.S.O.N., la mauvaise accusation et la Spare Battery disent quoi faire avec les jetons physiques.
  - **Affichage** : le compteur `; ; ;` disparaît de l'en-tête, du menu (jetons par joueur), de la salle d'attente et de la fin de partie.
  - **Scan d'une carte** : si on scanne un jeton à la place d'une carte, l'app répond « This is a Query Token: use it in the Police Console ».
  - **README** de l'app à mettre à jour.
- **Plateau V3** : rien à changer, les emplacements Ø 20 mm de la Server Room restent bons.

**Fait pour T1 (2026-11-26) :**
- **Règles** : game design, règles V2, livret (p. 2, 3, 4, 6, 7, PDF régénérés) et README de la DA, de l'app.
- **Planche** :
  - `DA/tokens/the-last-query_query-tokens_pawns_A4_duplex.pdf` (recto verso, retourner sur le bord long : recto `;` + pions, verso QR en miroir) ;
  - `DA/tokens/the-last-query_query-tokens_A4_glue.pdf` (une face : recto et verso à coller de chaque côté du carton) ;
  - fond perdu de 3 mm, Ø 20 mm, QR `TLQ:Q-01` … `Q-20` + code de secours. Le QR imprimé a été décodé avec le lecteur de l'app (`TLQ:Q-07`) ;
  - l'ancienne planche `…_query-tokens_pawns_A4.pdf` est dans la corbeille.
- **App** : plus de compteur de jetons. « Scan a token to run » avec la caméra ou le code tapé (`Q-07`, `q7`, `TLQ:Q-07` acceptés).
- **Testé en local à 375 px (hôte + invité)** :
  - le jeton Q-07 paie la requête de l'hôte ;
  - il est refusé à l'invité pendant la même manche ;
  - Q-08 passe ;
  - à la manche 2, Q-07 repasse ;
  - un jeton scanné à la place d'une carte est signalé ;
  - la recharge renvoie à la réserve ;
  - pas de défilement horizontal.

### T2 ✅ Planche de jetons recto verso « découpe simple » (demande du 2026-11-26)
- `DA/tokens/the-last-query_query-tokens_A4_duplex-grid.pdf` : les 20 jetons en **carrés de 20 × 20 mm, collés en grille 4 × 5**. On découpe à la règle ou au massicot : 5 coupes verticales + 6 horizontales, le long des traits de coupe.
- Chaque face a une seule couleur de fond : noir au recto, papier au verso. Un léger décalage d'impression recto verso ne se voit donc pas.
- Fond perdu de 3 mm autour du bloc. Le verso est en miroir pour retourner sur le bord long.
- Les QR Q-01, Q-07 et Q-20 ont été décodés à leur place sur le verso.
- Les planches rondes (recto verso et à coller) restent disponibles.
