# THE LAST QUERY — Murder at Ravenscroft Manor

> *"The house remembers everything. The killer made it forget."*

**Version 2 (simplified)**, validated with the team on 2026-11-25.

**Genre:** competitive deduction board game + phone companion app
**Players:** 2–4 detectives, each playing alone
**Duration:** 25–40 minutes
**Age:** 10+
**SQL needed to play:** none. **What you secretly learn:** `SELECT`, `WHERE`, `AND`, `BETWEEN`, and the fact that "0 rows" means one of your conditions is wrong.

---

## 1. The Story

**Sir Victor Ravenscroft**, 70, is the founder of *Ravenscroft Analytics*, the company that "knows everything about everyone".

His manor, an old Scottish house on a cliff, is a **smart house**. Its AI, **W.A.T.S.O.N.** (*Wireless Automated Tracking System Of the Night*), keeps a file on every guest: age, height, shoe size, which hand they write with…

Tonight is Victor's 70th birthday party. Twelve guests are invited. A storm cuts the bridge to the village.

At **11:45 PM**, Victor is found dead in his armchair in the **Library**, next to a cold cup of tea.

The killer left traces all over the manor, and also **planted fake clues** to trick the detectives.

**Your mission:** search the rooms, collect clues, query W.A.T.S.O.N.'s guest database from your phone, and be the **first** to name the killer.

---

## 2. The Game in 30 Seconds

> **Explore the manor, collect clues, and use your phone to search the guest database. The first detective to name the killer wins.**

- Every room has a deck of **clue cards**.
- Some clues describe **the killer** (shoe size, height, left-handed…). Some are **dead ends**. A few are **fake clues planted by the killer**.
- On your phone, you **filter the list of suspects** with your clues. That's SQL, shown as simple sentences.
- Each search on the phone costs **1 Query Token** `;`. Tokens are recharged in the **Server Room** (at the opposite end of the manor from the Library, with no cards to search), and everyone gets +1 token at each W.A.T.S.O.N. update.

---

## 3. Components

| Component | Quantity | Notes |
|---|---|---|
| Game board (manor map) | 1 | 9 rooms, A2 |
| Detective pawns | 4 | no special powers |
| Clue cards | 40 | 7 room decks of 5–6 cards (no deck in the Grand Hall or the Server Room) |
| Query Tokens `;` | 16 | 3 per player + spares |
| Detective Notebook | 1 pad | suspects × traits grid |
| Phone app "Police Console" | — | one phone per player |

---

## 4. The Manor (Board)

```
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │ OBSERVATORY  │─────│   LIBRARY    │─────│    CHAPEL    │
   │              │     │ (crime scene)│     │              │
   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
          │                    │                    │
   ┌──────┴───────┐     ┌──────┴───────┐     ┌──────┴───────┐
   │  MUSIC ROOM  │─────│  GRAND HALL  │─────│   KITCHEN    │
   │              │     │   (start)    │     │              │
   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
          │                    │                    │
   ┌──────┴───────┐     ┌──────┴───────┐     ┌──────┴───────┐
   │  GREENHOUSE  │─────│ WINE CELLAR  │─────│ SERVER ROOM  │
   └──────────────┘     └──────────────┘     └──────────────┘
```

- **No secret passages.**
- The **Server Room** is in the corner opposite the Library: **3 rooms away = 2 turns**. Going to recharge is a real choice.

### Special rooms
| Room | What happens there |
|---|---|
| **Grand Hall** | Everyone starts here. No deck. |
| **Library** | Crime scene. The **only** room where you can **accuse**. Richest deck in true clues. |
| **Server Room** | **Recharge**: refill up to 3 tokens. **No deck**: you only come here to recharge. |
| All other rooms | Search only. |

---

## 5. Rules

### Setup
1. The host starts a game on the app. Everyone joins with their phone.
2. Shuffle each room deck and place it face down on its room.
3. Everyone puts their pawn in the **Grand Hall** and takes **3 Query Tokens**.
4. The **youngest** player starts. Play goes clockwise.

### Your turn
**① MOVE**: move up to **2 rooms** along corridors. You may also stay.

**② ACT**: do ONE thing in your room:
- **Search**: draw **up to 2 cards** from the top of the room deck, one at a time. Scan them (or read them) secretly and keep them face down in front of you. If the deck is empty, the room has been searched clean.
- **Recharge** *(Server Room only)*: refill up to **3 tokens** (you can never have more than 3).
- **Accuse** *(Library only)*: see below.

**Anytime during your turn: QUERY.** Pay **1 token** to run one search on your phone (up to **2 conditions**).

### W.A.T.S.O.N. update
Every **4 rounds**, the host taps *End round* and the app:
- reveals **one true trait of the killer to everyone**;
- gives **every detective +1 token** (max 3).

This is the **only** way to get tokens outside the Server Room. No one gets stuck, and the game never drags.

### Accuse
Go to the **Library** and say out loud, in English, the killer's full profile:

> *"The killer is **Oscar Lindqvist**: 47 years old, 1.86 m tall, size 44 shoes, left-handed!"*

Then type the name in the app.
- ✅ **Right**: you win!
- ❌ **Wrong**: go back to the **Grand Hall** and lose all your tokens. You stay in the game.

### Golden rule (printed in the booklet)
> ***"Find the same clue twice, and it's probably true."***
> ***"0 suspects found? One of your clues is fake!"***

---

## 6. Clue Cards (40)

### Format: scan + printed (hybrid)
Each clue card shows **the object** (illustration + name + room), for example *"MUDDY FOOTPRINT · Greenhouse"*, plus a **QR code** and a backup code.
**Scanning it** shows what the object reveals **in the current case** (*"Size 44"*), or that it leads nowhere.

- You still have to **walk to the room** to draw its cards: the board stays essential.
- The same card can be a true clue in one case and a dead end in another, so the game is **replayable** and can't be learned by heart.
- **Bonus cards** are printed in full and are never scanned.
- For the demo, the app ships with **Case 1: The Foxglove Tea** (§8).

### 4 card types (Case 1)
| Type | Qty | Example | Role |
|---|---|---|---|
| 🔎 **Clue** | 15 | *Muddy footprint → size 44* | A real trait of the killer. **5 traits × 3 versions** in 3 different rooms. |
| 📄 **Dead End** | 13 | *Dinner menu → salmon, potatoes, chocolate cake* | True, but useless to find the killer. |
| 🎭 **Planted** | 6 | *Lavender petals → the killer smells of lavender* | Fake clue left by the killer. Only **1 copy**, and it **contradicts** the real clues. |
| ⚡ **Bonus** | 6 | *Spare Battery: +1 token* ×3 · *Running Shoes: move again* ×2 · *Master Key: look at the top card of any deck* ×1 | Small boosts. Printed, not scanned. |

### Why it balances
- True clues appear **3 times**, fakes only **once**: frequency tells you what to trust.
- A fake clue combined with a true one usually gives **"0 suspects found"**. That's the "Aha!" moment, and players discover what `AND` does on their own.
- Fakes make you **waste tokens**, which forces a trip to the Server Room (or a wait for the next W.A.T.S.O.N. update). The loop *search → query → recharge* balances itself.
- The Library is rich in clues but far from the recharge. The Server Room has no cards at all: going there costs you a search.

### Distribution per room (7 decks)
| Room | Clue | Dead End | Planted | Bonus | Total |
|---|---|---|---|---|---|
| Library | 3 | 1 | 1 | 0 | 5 |
| Greenhouse | 2 | 2 | 1 | 1 | 6 |
| Observatory | 2 | 2 | 1 | 1 | 6 |
| Chapel | 2 | 2 | 0 | 1 | 5 |
| Music Room | 2 | 2 | 1 | 1 | 6 |
| Kitchen | 2 | 2 | 1 | 1 | 6 |
| Wine Cellar | 2 | 2 | 1 | 1 | 6 |
| Server Room | — | — | — | — | **0** |
| **Total** | **15** | **13** | **6** | **6** | **40** |

---

## 7. The Phone: "Police Console" (no SQL knowledge needed)

The query screen is a sentence with blanks, filled with dropdowns:

```
 FIND guests WHERE [ Shoe size ▾ ] [ is ▾ ]      [ 44 ▾ ]
              AND  [ Height ▾ ]    [ between ▾ ] [ 1.85 ] and [ 1.90 ]
                                   [ RUN QUERY · 1 ; ]
```

- The result is the **list of matching names**, or **"0 suspects found"**.
- Under each result, a small box shows the real SQL:
  `💡 SELECT name FROM guests WHERE shoe = 44 AND height BETWEEN 1.85 AND 1.90;`
- **1 token = 1 query, max 2 conditions.** With 3–4 clues you need several queries and your notebook to cross-check.
- The phone **never shows the whole table**: you only see names that match.
- Other screens: **scanner** (QR + backup code), **my clues** (list of scanned cards), **accuse**, and **host mode** (*End round*, W.A.T.S.O.N. updates).
- End of game: *"You wrote 7 SQL queries tonight!"* with the full list.

---

## 8. Case 1: *"The Foxglove Tea"*

### The 12 suspects (table `GUESTS`)
| name | link to Victor | age | height | shoe | hand | hair | glasses | smell |
|---|---|---|---|---|---|---|---|---|
| Lady Margaret Ravenscroft | wife, botanist | 64 | 1.65 | 38 | right | grey | yes | lavender |
| Dr. Felix Moreau | family doctor | 58 | 1.84 | 43 | left | brown | yes | cigar |
| Ivy Ravenscroft | niece, influencer | 24 | 1.68 | 37 | right | red | no | perfume |
| Colonel Bram Hartley | old army friend | 71 | 1.86 | 45 | right | white | no | cigar |
| Sofia Delacroix | ex-fiancée, opera singer | 41 | 1.72 | 39 | left | black | no | perfume |
| Gideon Pike | butler | 66 | 1.80 | 44 | right | grey | yes | silver polish |
| **Oscar Lindqvist** | business partner, CTO | **47** | **1.86** | **44** | **left** | **blond** | no | **cigar** |
| Nora Quill | journalist | 35 | 1.70 | 40 | right | blond | no | cigar |
| Hugo Ravenscroft *(new)* | son, racing driver | 39 | 1.87 | 44 | left | blond | no | motor oil |
| Clara Finch *(new)* | Victor's secretary | 29 | 1.74 | 41 | left | blond | yes | perfume |
| Father Thomas Reilly *(new)* | village priest | 52 | 1.78 | 44 | right | brown | yes | incense |
| Dante Russo *(new)* | chef hired for the party | 45 | 1.86 | 44 | right | black | no | cigar |

### The killer's 5 traits (true clues)
Size **44** · **left**-handed · height **1.85–1.90 m** · **blond** · smells of **cigar**

**Balance check:**
- No pair of clues is enough (e.g. *size 44 + left* → Oscar **and Hugo**).
- **Hugo is the trap**: same height, shoes, hand and hair as Oscar. Only the **cigar** smell separates them.
- 3 clues including the smell → Oscar alone. So players need **3 to 4 clues**.

### The 40 cards
| Room | Card (object) | Type | What the scan reveals |
|---|---|---|---|
| Library | Wet sock on the rug | 🔎 | size 44 |
| Library | Teacup handle | 🔎 | turned to the left → left-handed |
| Library | Ashtray | 🔎 | fresh cigar ash |
| Library | Victor's diary | 📄 | "Buy birthday candles." |
| Library | Hair on Victor's jacket | 🎭 | grey hair |
| Greenhouse | Muddy footprint | 🔎 | size 44 |
| Greenhouse | Broken branch | 🔎 | broken at head height → 1.85–1.90 m |
| Greenhouse | Watering schedule | 📄 | "Foxglove: Tuesdays only." |
| Greenhouse | Plant label | 📄 | "Digitalis purpurea. Poisonous!" |
| Greenhouse | Petals on the floor | 🎭 | lavender smell |
| Greenhouse | Running Shoes | ⚡ | move again |
| Observatory | Telescope eyepiece | 🔎 | set for someone 1.85–1.90 m tall |
| Observatory | Hair on the telescope | 🔎 | blond hair |
| Observatory | Star chart | 📄 | "Full moon tonight." |
| Observatory | Security camera | 📄 | "W.A.T.S.O.N. rebooting… 11:20 PM". The lens is blurred by the rain. |
| Observatory | Reading glasses | 🎭 | the killer wears glasses |
| Observatory | Spare Battery | ⚡ | +1 token |
| Chapel | Glove on a pew | 🔎 | left glove, worn out |
| Chapel | Confessional | 🔎 | smells of cigar |
| Chapel | Hymn book | 📄 | page 42 is torn out |
| Chapel | Wedding photo | 📄 | Victor & Margaret, 1982 |
| Chapel | Running Shoes | ⚡ | move again |
| Music Room | Piano bench | 🔎 | blond hair |
| Music Room | Sheet music | 🔎 | ink smudged by a left hand |
| Music Room | Opera programme | 📄 | "Sofia Delacroix sings tonight!" |
| Music Room | Broken metronome | 📄 | stopped at 120 bpm |
| Music Room | Curtains | 🎭 | smell of incense |
| Music Room | Spare Battery | ⚡ | +1 token |
| Kitchen | Spilled flour | 🔎 | footprint size 44 |
| Kitchen | Top cupboard | 🔎 | opened without a stool → 1.85–1.90 m |
| Kitchen | Dinner menu | 📄 | salmon, potatoes, chocolate cake |
| Kitchen | Grocery list | 📄 | "Tea, lemons, candles." |
| Kitchen | Sugar bowl | 🎭 | long red hair |
| Kitchen | Spare Battery | ⚡ | +1 token |
| Wine Cellar | Behind the barrels | 🔎 | half-smoked cigar |
| Wine Cellar | Dusty barrel | 🔎 | blond hair stuck in the cobwebs |
| Wine Cellar | Poker IOU | 📄 | "Bram owes Victor £200,000." |
| Wine Cellar | Dusty bottle | 📄 | Château Ravenscroft 1956 |
| Wine Cellar | Footprint in the dust | 🎭 | size 38 |
| Wine Cellar | Master Key | ⚡ | look at the top card of any deck |

The fakes mostly frame **Margaret** (lavender, size 38, grey hair): Oscar tried to make the wife look guilty.

### W.A.T.S.O.N. updates (every 4 rounds)
Round 4: height 1.85–1.90 m · Round 8: blond · Round 12: smells of cigar. Each time, every detective also gets +1 token (max 3).

### Solution
**Oscar Lindqvist**, 47, 1.86 m, size 44, left-handed, blond, smells of cigar. He poisoned Victor's tea with foxglove because Victor had found out he was selling company data.

---

## 9. Learning Goals (pitch for the jury)

| In the game | In SQL |
|---|---|
| Searching the guest file | `SELECT name FROM guests` |
| Using one clue | `WHERE shoe = 44` |
| Combining two clues | `AND` |
| "Between 1.85 and 1.90 m" | `BETWEEN` |
| "0 suspects found" | an empty result: one condition is false |

- **No prior SQL needed**: players read sentences, and the real SQL is always visible.
- **Physical + digital**: the board gives the clues, the phone gives the answers.
- **English everywhere**: clue cards, the accusation speech, table talk.
- **Replayable**: the same cards, with new cases added to the app.

---

## 10. Next Steps

1. **Design updates** (see the impact list for `DA/`).
2. **App (mobile-first, 100% responsive)**, MVP order:
   1. Join a game with a code
   2. Scanner (QR + backup code) → my clues
   3. Query screen (sentence builder + real SQL)
   4. Accuse
   5. Host mode (End round, W.A.T.S.O.N. updates)
3. **Playtest**, then adjust: start tokens, deck sizes, update frequency.
