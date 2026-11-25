# THE LAST QUERY : retours du playtest n°1 (2026-11-25)

Statuts : ⬜ à faire · 🔄 en cours · ✅ fait · ❓ à trancher avec le groupe.
**Point au 2026-11-25 : tout est fait.** L'app est testée en local à 375 px (hôte + invité) et **n'est pas encore redéployée** sur GitHub Pages.
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
- **Pas fait** : redéploiement de l'app (`npm run build:pages` puis push de `docs/`), en attente de votre accord.
