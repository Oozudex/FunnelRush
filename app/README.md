# The Last Query · Police Console (app web)

Application compagnon du jeu de société **The Last Query** : chaque détective l'utilise sur son téléphone pour scanner les cartes indices, interroger la base de données de W.A.T.S.O.N. en SQL (sans le savoir) et accuser le coupable. Toute l'interface est en anglais.

**En ligne :** https://oozudex.github.io/FunnelRush/ (GitHub Pages).

## Comment ça marche, sans serveur

- **Stack :** Vite + React + TypeScript, compilé en fichiers statiques. GitHub Pages suffit : pas de serveur à héberger, pas de compte à créer.
- **Le téléphone de l'hôte fait tourner la partie.** Les règles (`src/engine/`) s'exécutent dans son navigateur, et la partie est sauvegardée sur ce téléphone à chaque action.
- **Les autres téléphones lui parlent via deux relais MQTT publics et gratuits** (HiveMQ et EMQX, utilisés en même temps au cas où l'un tombe). Ça marche sur n'importe quel réseau : 4G, Wi-Fi de l'école…
- **L'hôte doit garder l'app ouverte** pendant la partie. S'il la ferme ou recharge la page, il retrouve sa partie en la rouvrant, et les autres téléphones se reconnectent tout seuls.
- Les messages perdus par les relais sont renvoyés automatiquement, et l'hôte n'exécute jamais deux fois la même action.

## Lancer en local

Il faut Node 20 ou plus.

```bash
cd app
npm install
npm run dev
```

- Ouvre http://localhost:5173 et crée une partie.
- Les téléphones scannent le QR affiché : il pointe vers l'IP Wi-Fi de l'ordinateur (par exemple `http://192.168.1.12:5173/?join=RAVEN-42`). Ils peuvent aussi taper le code.
- Pour tester seul : 2 onglets en vue mobile, un sur `http://localhost:5173` et l'autre sur l'adresse du QR.
- Il faut Internet, même en local, pour joindre les relais MQTT.

**Caméra :** les navigateurs n'autorisent la caméra qu'en HTTPS. Sur GitHub Pages, c'est automatique. En local sur téléphone, lance `HTTPS=1 npm run dev` et accepte le certificat. Le **code de secours** imprimé sous chaque QR (par exemple `LIB-01`) marche toujours.

## Mettre à jour la version en ligne (GitHub Pages)

```bash
cd app
npm run build:pages
```

Commit puis push le dossier `docs/` à la racine du dépôt. GitHub Pages est réglé sur : branche `main`, dossier `/docs` (Settings → Pages). La mise en ligne prend environ 1 minute.

## Ce que fait l'app (règles V2)

| Écran | Rôle |
|---|---|
| **Home** | Créer une partie (code type `RAVEN-42`) ou en rejoindre une (QR qui pré-remplit le code, ou saisie manuelle). |
| **Waiting room** | Code + QR, liste des détectives en temps réel, choix du pion P1–P4, l'hôte choisit qui commence (le plus jeune) et lance la partie. |
| **Scan** | Scanner QR via la caméra (`TLQ:LIB-01`) ou code de secours (`LIB-01`, `lib01`…). Révèle l'indice en privé. Un trait débloque la colonne correspondante dans la console. Les codes Spare Battery donnent +1 jeton (une fois par carte). |
| **Query** | Phrase à blocs : `FIND guests WHERE [colonne] [opérateur] [valeur] AND …` (2 conditions max). Les colonnes restent 🔒 tant qu'aucun indice ne les concerne. Coût : 1 `;`, uniquement pendant son tour. Le vrai SQL est affiché, le résultat est privé, et « 0 SUSPECTS FOUND » s'affiche avec un effet glitch. Historique des requêtes. |
| **Clues** | Indices regroupés par trait avec « seen ×N » (règle d'or), mises à jour W.A.T.S.O.N. confirmées, culs-de-sac, bonus. |
| **Suspects** | Carnet privé : 12 suspects à cocher ✗, interrogatoire (déclaration de chaque suspect), notes, nombre d'apparitions dans les résultats. |
| **Manor** | Tour en cours, Recharge (Server Room), Accuse (Library), fin de tour, ordre des joueurs et jetons, journal. **Hôte** : finir la manche, passer le tour d'un absent, afficher le QR, terminer la partie (le tueur s'échappe). |
| **Overlays** | Mise à jour W.A.T.S.O.N. à la fin des manches 4, 8 et 12 (un trait vrai + 1 `;` pour tous), mauvaise accusation (retour au Grand Hall, jetons à 0). |
| **Fin** | Victoire ou défaite, solution complète, « You wrote N SQL queries tonight! » avec la liste. |

Adaptations V2 par rapport à la demande initiale : il n'y a plus de café ☕ (remplacé par les jetons `;`), plus de mots-clés ni de tables à débloquer (ce sont les colonnes qui se débloquent), plus d'horloge (on garde une heure indicative de 12:00 AM + 15 min par manche) ni d'événements d'orage (remplacés par les mises à jour W.A.T.S.O.N.). L'accusation porte sur un seul nom. Les interrogatoires deviennent des déclarations dans le carnet. L'effet glitch de la DA sert pour les données « corrompues ».

## Ajouter une affaire

1. Copie `src/engine/cases/foxglove.ts` (par exemple `case2.ts`).
2. Change les suspects et leurs traits, ce que révèle chaque code de carte (les mêmes 40 cartes physiques `LIB-01` à `CEL-06` sont réutilisées), le coupable, les 3 mises à jour W.A.T.S.O.N. et l'histoire.
3. Ajoute-la dans `src/engine/cases/index.ts`. L'action `lobby:case` permet déjà à l'hôte de changer d'affaire. Il ne reste qu'à ajouter un sélecteur dans la salle d'attente.

Limite connue : sans serveur, les données de l'affaire sont dans le code téléchargé, donc un joueur très motivé pourrait tricher en lisant le code. Ce n'est pas gênant pour une partie entre amis.

## Structure

```
app/
  src/engine/            règles (Game) + données des affaires, exécutées sur le téléphone de l'hôte
  src/net/link.ts        connexion aux 2 relais MQTT publics, dédoublonnage
  src/net/room.ts        HostRoom (fait tourner la partie) / GuestRoom (envoie les actions)
  src/socket.ts          API utilisée par les écrans : createGame, joinGame, resume, emit, leave
  src/screens/           Home, Lobby, Game (Scan, Query, Clues, Notebook, Manor), End
  shared/                types + générateur SQL
  src/styles.css         DA : noir / bone / rouge, Bungee, Archivo, IBM Plex Mono, Silkscreen
  public/logo.svg        logo copié depuis DA/logo
```
