# THE LAST QUERY : version 2 simplifiée

> ✅ **Validé le 2026-11-25** : jeton `;` Query Token · cartes **hybrides** (objet imprimé + QR scanné, rejouable) · erreur = retour au Grand Hall + perte des jetons · Salle des serveurs au coin opposé · 12 suspects · fausses pistes · mise à jour W.A.T.S.O.N. + carnet-grille · pas de pouvoirs de détective.
> La version de référence à jour est `Data_Detective_Game_Design.md`.

> Objectif : **un jeu qu'on comprend en 3 minutes**, même sans jamais avoir fait de SQL.
> Les phrases en *anglais* sont le texte du futur livret. Les ❓ sont les questions à trancher ensemble (récap à la fin).

---

## 1. Le jeu en 30 secondes

> **Explore the manor, collect clues, and use your phone to search the guest database. The first detective to name the killer wins.**

- Chaque pièce a une pioche de **vraies cartes indices**.
- Certains indices décrivent **le meurtrier** (sa pointure, sa taille, s'il est gaucher…). D'autres **ne servent à rien**, et quelques-uns sont des **fausses pistes**.
- Sur le téléphone, on **filtre la liste des suspects** avec ces indices. C'est du SQL, mais présenté comme des phrases simples.
- Pour faire une recherche, il faut un **jeton**. Les jetons se rechargent dans la **Salle des serveurs**, à l'autre bout du manoir par rapport à la Bibliothèque.

---

## 2. Vos idées, gardées et renforcées

| Votre idée | Ce que j'en fais |
|---|---|
| Tout le monde démarre dans le Grand Hall | ✅ Gardé. |
| Déplacement de 2 pièces max | ✅ Gardé, sans dé. |
| Jeu solo, le premier qui trouve gagne | ✅ Gardé. Il n'y a plus d'horloge ni de « tout le monde perd ». |
| Le plus jeune commence | ✅ Gardé. |
| Une pioche par pièce avec de vrais indices, dont certains inutiles | ✅ Gardé, et **renforcé** : en plus des indices inutiles, quelques **fausses pistes posées par le tueur**. Elles créent les meilleurs moments du jeu (voir §5). |
| La Salle des serveurs recharge les jetons | ✅ Gardé. C'est **la seule** façon de recharger, ce qui crée un vrai choix : « je cours recharger, ou je fouille encore ? » |
| Salle des serveurs à l'extrémité de la Bibliothèque | ✅ Placée dans le **coin opposé** à la Bibliothèque : il faut **2 tours** pour faire le trajet. ❓Q4 |
| Fin de partie avec le profil du tueur (nom, âge, taille, pointure, main…) | ✅ C'est devenu **le cœur du jeu** : chaque indice donne une caractéristique, et l'accusation finale consiste à donner le profil complet. |
| Joueurs qui ne connaissent pas le SQL | ✅ Plus aucun mot-clé à débloquer. L'app parle en phrases et montre le vrai SQL en petit, pour apprendre sans effort (voir §7). |

---

## 3. Ce qu'on supprime (pour aller plus vite)

- ❌ Les cartes Keyword et Table à scanner (débloquer le SQL)
- ❌ Le café et les cartes Café, remplacés par les **jetons de requête**
- ❌ Les cartes Twist (sauf 3 petits bonus)
- ❌ L'horloge et les 8 manches, ainsi que les événements d'orage
- ❌ Les pouvoirs des pièces (il ne reste que la Salle des serveurs et la Bibliothèque)
- ❌ Les passages secrets (ils servaient de raccourci vers la Salle des serveurs)
- ❌ Les interrogatoires, dont les phrases peuvent devenir des cartes indices de type « témoignage »
- ❓ Les pouvoirs des détectives : je propose de les **retirer** (tout le monde est pareil) et de les garder en « mode avancé ». ❓Q6

**Résultat : 40 cartes au lieu de 60, 1 type de jeton, 2 pièces spéciales, 2 étapes par tour.**

---

## 4. Les règles V2 (texte du livret)

### Setup
> 1. The host starts a game on the app. Everyone joins with their phone.
> 2. Shuffle each room deck and place it face down on its room.
> 3. Everyone puts their pawn in the **Grand Hall** and takes **3 Query Tokens**.
> 4. The **youngest** player starts.

### Your turn
> **① MOVE**: move up to **2 rooms**. You may also stay.
>
> **② ACT**: do ONE thing in your room:
> - **Search**: draw the top card of the room deck. Read it secretly and keep it face down in front of you.
> - **Recharge** *(Server Room only)*: refill up to **3 tokens**.
> - **Accuse** *(Library only)*: see below.
>
> **Anytime on your turn: QUERY.** Pay **1 token** to search the guest database on your phone.

### Accuse
> Go to the **Library** and say out loud, in English:
> *"The killer is **Oscar Lindqvist**: 47 years old, 1.86 m tall, size 44 shoes, left-handed!"*
> Then type the name in the app.
> - ✅ Right: **you win!**
> - ❌ Wrong: go back to the **Grand Hall** and lose all your tokens. ❓Q3

---

## 5. Les cartes : composition et équilibre

### 4 types de cartes

| Type | Qté | Exemple | Rôle |
|---|---|---|---|
| 🔎 **Clue** (vrai indice) | 15 | *"Muddy footprint in the Greenhouse: **size 44**."* | Donne une vraie caractéristique du tueur. |
| 📄 **Dead End** (indice inutile) | 13 | *"Dinner menu: salmon, potatoes, chocolate cake."* · *"Bram drank 6 glasses of whisky."* | Vrai, mais n'aide pas à trouver le tueur. |
| 🎭 **Planted** (fausse piste) | 6 | *"A **red** lipstick mark on Victor's cup."* (désigne Sofia, innocente) | Le tueur a posé de faux indices pour piéger les détectives. |
| ⚡ **Bonus** | 6 | *"Spare battery: +1 token"* ×3 · *"Running shoes: move again"* ×2 · *"Master key: look at the top card of any deck"* ×1 | Petits coups de pouce. |

**Total : 40 cartes = 8 pièces × 5 cartes** (toutes les pièces sauf le Grand Hall).

### Comment on reconnaît une fausse piste ? (le cœur de l'équilibre)

1. **Chaque vrai indice existe en 3 versions** dans 3 pièces différentes, avec des textes différents (*empreinte de boue taille 44*, *boîte à chaussures 44 vide*, *chaussette mouillée taille 44*).
   → Règle d'or dans le livret : ***"Find the same clue twice, and it's probably true."***
2. **Une fausse piste n'existe qu'en 1 exemplaire** et **contredit** un vrai indice.
3. Quand on combine une fausse piste avec un vrai indice, l'app répond **« 0 suspect found »**.
   → C'est le moment « Aha ! » : *« Un de mes indices est faux ! »*. Les joueurs apprennent tout seuls ce que fait un `AND`.

**Conséquence** : les fausses pistes font **gaspiller des jetons**, ce qui oblige à retourner à la Salle des serveurs. La boucle « fouiller → requête → recharger » s'équilibre toute seule.

### Répartition par pièce (5 cartes chacune)

| Pièce | Vrais | Inutiles | Faux | Bonus |
|---|---|---|---|---|
| Library (scène de crime) | 3 | 1 | 1 | 0 |
| Greenhouse | 2 | 2 | 1 | 0 |
| Observatory | 2 | 1 | 1 | 1 |
| Chapel | 2 | 2 | 0 | 1 |
| Music Room | 2 | 2 | 1 | 0 |
| Kitchen | 2 | 2 | 1 | 0 |
| Wine Cellar | 1 | 2 | 1 | 1 |
| Server Room | 1 | 1 | 0 | 3 |
| **Total** | **15** | **13** | **6** | **6** |

La **Bibliothèque** est riche en indices mais loin de la recharge. La **Salle des serveurs** recharge et donne des bonus, mais peu d'indices. C'est ce tiraillement qui crée la tension.

---

## 6. Le profil du tueur (votre fin de partie)

### Les caractéristiques de chaque suspect

| Vos idées | Mes ajouts proposés |
|---|---|
| Name · Age · Height · Shoe size · Left/right-handed | **Hair colour** · **Glasses** (yes/no) · **Smell** (cigar, lavender, perfume…) |

Il faut **4 vrais indices différents** pour isoler le tueur. Avec 5 caractéristiques en jeu (×3 versions = 15 cartes), il y a de la marge.

### Exemple : le profil d'Oscar (le tueur de l'affaire tutoriel)
| Name | Age | Height | Shoe | Hand | Hair | Glasses | Smell |
|---|---|---|---|---|---|---|---|
| Oscar Lindqvist | 47 | 1.86 m | 44 | left | blond | no | cigar |

### Exemples de vrais indices (3 versions par caractéristique)
- **Shoe** : *Muddy footprint in the Greenhouse: size 44.* · *An empty shoe box (size 44) in the Wine Cellar.* · *Wet sock on the Library rug: size 44.*
- **Hand** : *The cup handle was turned to the left.* · *Ink smudge on the left side of the letter.* · *Gloves found: only the left one is worn out.*
- **Height** : *A scratch on the door frame at 1.86 m.* · *Camera silhouette: about 1.85 m.* · *The top shelf was reached without a ladder.*
- **Hair** : *A blond hair on Victor's jacket.* · …
- **Smell** : *The Library smells of cigar.* · …

❓**Combien de suspects ?** Avec 8 suspects, 2 indices suffisent souvent : c'est trop facile. Je propose de passer à **12 suspects** (les 8 actuels + 4 nouveaux). ❓Q5

---

## 7. Le téléphone pour ceux qui ne connaissent pas le SQL

L'écran ressemble à une phrase à trous qu'on complète avec des boutons :

```
 FIND guests WHERE [ Shoe size ▾ ] [ is ▾ ] [ 44 ▾ ]
              AND  [ Hand ▾ ]      [ is ▾ ] [ left ▾ ]
                                  [ RUN QUERY · 1 token ]
```

Le résultat donne la liste des noms qui correspondent (ou « 0 suspect found »). En dessous, un petit encart :

```
 💡 Real SQL:  SELECT name FROM guests WHERE shoe = 44 AND hand = 'left';
```

- **1 jeton = 1 requête, avec 2 conditions maximum** (`WHERE` + `AND`). Pas besoin de comprendre le SQL pour jouer, mais on le voit à chaque requête.
- Le téléphone **ne montre jamais toute la table** : on ne voit que les noms qui correspondent. Sans requête, on ne sait rien des suspects.
- Bonus « école » : en fin de partie, l'app affiche **« You wrote 7 SQL queries tonight! »** avec la liste. C'est un super argument devant le jury.

---

## 8. Le symbole du jeton (à choisir) ❓Q1

| Option | Visuel | Nom | Pourquoi |
|---|---|---|---|
| **A** ⭐ | un **`;`** rouge dans un cercle noir | **Query Token** | En SQL, chaque requête se termine par `;`. C'est déjà le `;` rouge du logo : *1 jeton = 1 requête = 1 point-virgule*. Hyper cohérent avec le nom « The Last Query ». |
| **B** | un **éclair / une batterie** | **Power Cell** | On « recharge » à la Salle des serveurs : tout le monde comprend sans explication. |
| **C** | un **badge d'accès** de la maison (carte avec puce) | **Access Badge** | Ce sont les badges de W.A.T.S.O.N. : on les réactive au serveur. |
| **D** | une **carte perforée** | **Punch Card** | Look rétro-informatique, va bien avec le film noir. |

---

## 9. Le plan du manoir ❓Q4

Proposition : la **Salle des serveurs** passe dans le **coin en bas à droite** (elle échange sa place avec la Cave à vin), et on retire les passages secrets.

```
   OBSERVATORY ── LIBRARY ──── CHAPEL
        │            │            │
   MUSIC ROOM ── GRAND HALL ── KITCHEN
        │            │            │
   GREENHOUSE ── WINE CELLAR ── SERVER ROOM
```

- Bibliothèque → Salle des serveurs = **3 pièces = 2 tours**. Recharger devient un vrai choix.
- Depuis le Grand Hall, tout reste accessible en 1 tour (sauf les coins opposés), donc le début de partie reste rapide.

---

## 10. Idées en plus (à garder ou non)

1. **Mise à jour de W.A.T.S.O.N.** *(anti-blocage)* : tous les 4 tours de table, l'app révèle **une caractéristique du tueur à tout le monde**. Personne ne reste bloqué, et la partie ne dure jamais trop longtemps.
2. **Filature** : si tu finis ton déplacement dans la même pièce qu'un autre détective, tu peux payer **1 jeton** pour regarder **1 de ses cartes** au hasard. Ça crée de l'interaction, tout en restant optionnel.
3. **Carnet du détective** : une grille avec les 12 suspects en lignes et les caractéristiques en colonnes. On coche au fur et à mesure des résultats de requêtes : un mini « Qui est-ce ? » de détective.
4. **Phrases utiles en anglais** au dos du carnet : *"I found a clue in the…"*, *"I think this clue is fake because…"*, *"The killer is…"*.
5. **Plusieurs affaires** : l'app choisit le tueur au hasard parmi 3 affaires préparées, avec des pioches différentes (code couleur au dos). ❓Q2

---

## 11. Questions à valider ensemble

| # | Question | Ma recommandation |
|---|---|---|
| Q1 | Quel symbole pour le jeton ? | **A : le `;` Query Token** |
| Q2 | Les indices sont-ils imprimés en clair sur les cartes (1 affaire fixe, simple, pas de scan), ou génériques et scannés (l'app donne l'indice, donc rejouable) ? | **Imprimés en clair** pour la démo, puis plus tard un 2ᵉ jeu de cartes pour une 2ᵉ affaire |
| Q3 | Sanction si on se trompe d'accusation ? | **Retour au Grand Hall + perte de tous les jetons** (pas d'élimination) |
| Q4 | Où placer la Salle des serveurs ? | **Coin opposé à la Bibliothèque** (2 tours de trajet) |
| Q5 | Combien de suspects ? | **12** |
| Q6 | Pouvoirs des détectives : on les garde ? | **Non** en jeu de base, oui en mode avancé |
| Q7 | Fausses pistes (🎭 Planted) : on les garde ? | **Oui**, c'est ce qui rend les requêtes intéressantes |
| Q8 | Idées en plus du §10 : lesquelles on garde ? | **1 (mise à jour W.A.T.S.O.N.) et 3 (carnet)** au minimum |

---

## 12. Ce que ça change côté design (aperçu)

Liste détaillée à faire après validation. En gros :
- **Cartes** : à refaire presque entièrement (40 nouvelles cartes avec de vrais textes, 4 nouveaux types). Le style « Case File » validé est conservé.
- **Jetons** : les jetons café deviennent des jetons de requête (nouveau symbole). Les jetons SUSPENDED et horloge disparaissent.
- **Plateau** : la Salle des serveurs change de place, les passages secrets, l'horloge et les pouvoirs des pièces sont retirés de la barre latérale.
- **Carnet** : nouvelle grille suspects × caractéristiques.
- **Livret** : à réécrire, il sera beaucoup plus court.
