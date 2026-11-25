# The Last Query · Police Console (app web)

Application compagnon du jeu de société **The Last Query** : chaque détective l'utilise sur son téléphone pour scanner les cartes indices, interroger la base de données de W.A.T.S.O.N. en SQL (sans le savoir) et accuser le coupable. Toute l'interface est en anglais.

**Stack :** Vite + React + TypeScript côté client, Node + Express + Socket.IO côté serveur, le tout dans un seul dossier. C'est la solution la plus simple pour avoir des salons en temps réel, et un seul service à héberger.

## Lancer en local

Il faut Node 20 ou plus.

```bash
cd app
npm install
npm run dev
```

- Ouvre http://localhost:5173 sur l'ordinateur et crée une partie.
- Les téléphones (sur le **même Wi-Fi**) scannent le QR code affiché : il pointe automatiquement vers l'IP Wi-Fi de l'ordinateur (par exemple `http://192.168.1.12:5173/?join=RAVEN-42`). Ils peuvent aussi ouvrir cette adresse et taper le code.
- Pour tester seul : 2 onglets en vue mobile, un sur `http://localhost:5173` et l'autre sur `http://127.0.0.1:5173` (ou l'adresse du QR).

**Caméra des téléphones en local :** les navigateurs n'autorisent la caméra qu'en HTTPS. En Wi-Fi local, lance plutôt :

```bash
HTTPS=1 npm run dev
```

Accepte ensuite le certificat auto-signé sur chaque téléphone. Sans HTTPS, le **code de secours** imprimé sous chaque QR (par exemple `LIB-01`) marche toujours. Une fois l'app déployée en HTTPS, la caméra fonctionne directement.

## Version de production en local

```bash
npm run build
npm start
```

Tout est servi sur http://localhost:3001 (ou sur le port de la variable `PORT`).

## Déployer gratuitement pour la démo (Render)

1. Mets le projet sur GitHub (c'est déjà fait si ce dossier est dans le dépôt).
2. Sur https://render.com, choisis **New → Blueprint**, puis le dépôt : le fichier `render.yaml` à la racine configure tout. Sinon, en manuel : **New → Web Service**, avec ces réglages :
   - Root Directory : `app`
   - Build Command : `npm ci --include=dev && npm run build`
   - Start Command : `npm start`
   - Instance type : Free
3. Render donne une URL en `https://…onrender.com`. Le QR code de la salle d'attente l'utilise automatiquement, et la caméra marche en HTTPS.

Le service gratuit s'endort après 15 minutes sans visite. Ouvre l'URL une minute avant la démo pour le réveiller. Les parties sont gardées en mémoire et dans `.games.json`, ce qui fait qu'un redémarrage ne coupe pas une partie en cours. En revanche, sur Render gratuit, ce fichier est effacé quand le service s'endort.

### GitHub Pages (interface) + Render (serveur)

GitHub Pages ne sert que des fichiers statiques. Il héberge donc l'**interface** (dossier `docs/` à la racine), qui se connecte au **serveur** Render.

1. Déploie le serveur sur Render (étapes ci-dessus). Note son URL, par exemple `https://the-last-query.onrender.com`.
2. Si l'URL est différente, modifie la ligne de `docs/config.js`. Tu peux aussi reconstruire : `TLQ_SERVER=https://ton-url.onrender.com npm run build:pages`.
3. Sur GitHub : Settings → Pages → Source « Deploy from a branch », branche `main`, dossier `/docs`.
4. Après chaque modification de l'app, lance `npm run build:pages` puis commit le dossier `docs/`.

Autres options gratuites possibles : Railway, Fly.io, Koyeb (même build et même start). Vercel et Netlify ne conviennent pas, car Socket.IO a besoin d'un serveur qui tourne en continu.

## Ce que fait l'app (règles V2)

| Écran | Rôle |
|---|---|
| **Home** | Créer une partie (code type `RAVEN-42`) ou en rejoindre une (QR qui pré-remplit le code, ou saisie manuelle). |
| **Waiting room** | Code + QR, liste des détectives en temps réel, choix du pion P1–P4, l'hôte choisit qui commence (le plus jeune) et lance la partie. |
| **Scan** | Scanner QR via la caméra (`TLQ:LIB-01`) ou code de secours (`LIB-01`, `lib01`…). Révèle l'indice en privé. Un trait débloque la colonne correspondante dans la console. Les codes Spare Battery donnent +1 jeton (une fois par carte). |
| **Query** | Phrase à blocs : `FIND guests WHERE [colonne] [opérateur] [valeur] AND …` (2 conditions max). Les colonnes restent 🔒 tant qu'aucun indice ne les concerne. Coût : 1 `;`, uniquement pendant son tour. Le vrai SQL est affiché, le résultat est privé, et « 0 SUSPECTS FOUND » s'affiche avec un effet glitch. Historique des requêtes. |
| **Clues** | Indices regroupés par trait avec « seen ×N » (règle d'or), mises à jour W.A.T.S.O.N. confirmées, culs-de-sac, bonus. |
| **Suspects** | Carnet privé : 12 suspects à cocher ✗, interrogatoire (déclaration de chaque suspect), notes, nombre d'apparitions dans les résultats. |
| **Manor** | Tour en cours, Recharge (Server Room), Accuse (Library), fin de tour, ordre des joueurs et jetons, journal. **Hôte** : finir la manche, passer le tour d'un absent, afficher le QR pour reconnecter, terminer la partie (le tueur s'échappe). |
| **Overlays** | Mise à jour W.A.T.S.O.N. à la fin des manches 4, 8 et 12 (un trait vrai + 1 `;` pour tous), mauvaise accusation (retour au Grand Hall, jetons à 0). |
| **Fin** | Victoire ou défaite, solution complète, « You wrote N SQL queries tonight! » avec la liste. |

Adaptations V2 par rapport à la demande initiale : il n'y a plus de café ☕ (remplacé par les jetons `;`), plus de mots-clés ni de tables à débloquer (ce sont les colonnes qui se débloquent), plus d'horloge (on garde une heure indicative de 12:00 AM + 15 min par manche) ni d'événements d'orage (remplacés par les mises à jour W.A.T.S.O.N.). L'accusation porte sur un seul nom (plus de Who + Weapon + Motive). Les interrogatoires deviennent des déclarations dans le carnet. L'effet glitch de la DA sert pour les données « corrompues ».

## Ajouter une affaire

1. Copie `server/cases/foxglove.ts` (par exemple `server/cases/case2.ts`).
2. Change les suspects et leurs traits, ce que révèle chaque code de carte (les mêmes 40 cartes physiques `LIB-01` à `CEL-06` sont réutilisées), le coupable, les 3 mises à jour W.A.T.S.O.N. et l'histoire.
3. Ajoute-la dans `server/cases/index.ts`. Elle apparaît dans `/api/info`, et l'hôte peut la choisir avec l'événement `lobby:case`. Un sélecteur dans la salle d'attente reste à ajouter quand il y aura 2 affaires.

Les données secrètes (traits des suspects, révélations, coupable) restent **côté serveur**. Le téléphone ne reçoit que les noms et les résultats de ses propres requêtes.

## Structure

```
app/
  server/index.ts        Express + Socket.IO, salons, sauvegarde .games.json
  server/game.ts         règles : tours, manches, scan, requêtes, accusation
  server/cases/          données des affaires (Foxglove Tea)
  shared/                types + générateur SQL partagés client/serveur
  src/screens/           Home, Lobby, Game (Scan, Query, Clues, Notebook, Manor), End
  src/styles.css         DA : noir / bone / rouge, Bungee, Archivo, IBM Plex Mono, Silkscreen
  public/logo.svg        logo copié depuis DA/logo
```
