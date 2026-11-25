// Case 1: "The Foxglove Tea" (game design V2, section 8).
// Card codes = codes printed on DA/cards (QR content "TLQ:LIB-01", backup code "LIB-01").
import type { CaseDef, CardDef, SuspectDef } from './types';

const range = (from: number, to: number, step: number, dec = 0) => {
  const out: number[] = [];
  for (let v = from; v <= to + 1e-9; v += step) out.push(Number(v.toFixed(dec)));
  return out;
};

const S = (
  id: string, name: string, link: string, age: number, height: number, shoe: number,
  hand: string, hair: string, glasses: string, smell: string, statement: string,
): SuspectDef => ({ id, name, link, statement, traits: { age, height, shoe, hand, hair, glasses, smell } });

const suspects: SuspectDef[] = [
  S('margaret', 'Lady Margaret Ravenscroft', 'Wife, botanist', 64, 1.65, 38, 'right', 'grey', 'yes', 'lavender',
    'I was in the Greenhouse with my foxgloves when the lights went out. Victor and I had our quarrels, but I loved him.'),
  S('felix', 'Dr. Felix Moreau', 'Family doctor', 58, 1.84, 43, 'left', 'brown', 'yes', 'cigar',
    'I checked his heart at ten o\'clock. He was in perfect health for a man of seventy. This was no accident.'),
  S('ivy', 'Ivy Ravenscroft', 'Niece, influencer', 24, 1.68, 37, 'right', 'red', 'no', 'perfume',
    'I was filming the storm for my followers. Forty thousand people can tell you where I was!'),
  S('bram', 'Colonel Bram Hartley', 'Old army friend', 71, 1.86, 45, 'right', 'white', 'no', 'cigar',
    'Victor and I go back fifty years. Money between old friends is nobody\'s business.'),
  S('sofia', 'Sofia Delacroix', 'Ex-fiancée, opera singer', 41, 1.72, 39, 'left', 'black', 'no', 'perfume',
    'I sang for him tonight, in the Music Room. He smiled at me. It was the last time.'),
  S('gideon', 'Gideon Pike', 'Butler', 66, 1.80, 44, 'right', 'grey', 'yes', 'silver polish',
    'I served the tea in the Library at a quarter past eleven, as always. I did not see who touched the cup after that.'),
  S('oscar', 'Oscar Lindqvist', 'Business partner, CTO', 47, 1.86, 44, 'left', 'blond', 'no', 'cigar',
    'Victor and I built this company together. Why would I hurt him? If I were you, I would talk to his wife.'),
  S('nora', 'Nora Quill', 'Journalist', 35, 1.70, 40, 'right', 'blond', 'no', 'cigar',
    'I came here for a story. Now I have one. Somebody in this house is lying to you, detective.'),
  S('hugo', 'Hugo Ravenscroft', 'Son, racing driver', 39, 1.87, 44, 'left', 'blond', 'no', 'motor oil',
    'Yes, my father and I argued about money. But I spent the whole evening in the garage with my car.'),
  S('clara', 'Clara Finch', 'Victor\'s secretary', 29, 1.74, 41, 'left', 'blond', 'yes', 'perfume',
    'I typed his letters for six years. Lately he was worried. He said someone was selling the company\'s data.'),
  S('thomas', 'Father Thomas Reilly', 'Village priest', 52, 1.78, 44, 'right', 'brown', 'yes', 'incense',
    'Victor came to confession last week. I cannot tell you what he said. I can only pray for him.'),
  S('dante', 'Dante Russo', 'Chef hired for the party', 45, 1.86, 44, 'right', 'black', 'no', 'cigar',
    'Salmon, potatoes, chocolate cake. I never left my kitchen all night. Ask anyone!'),
];

const SIZE44 = { attr: 'shoe', op: '=' as const, value: 44 };
const LEFT = { attr: 'hand', op: '=' as const, value: 'left' };
const CIGAR = { attr: 'smell', op: '=' as const, value: 'cigar' };
const TALL = { attr: 'height', op: 'between' as const, value: 1.85, value2: 1.9 };
const BLOND = { attr: 'hair', op: '=' as const, value: 'blond' };

const L = 'Library', G = 'Greenhouse', O = 'Observatory', C = 'Chapel', M = 'Music Room', K = 'Kitchen', W = 'Wine Cellar';
const clue = (room: string, object: string, reveal: string, condition: CardDef['condition']): CardDef => ({ room, object, type: 'clue', reveal, condition });
const fake = (room: string, object: string, reveal: string, condition: CardDef['condition']): CardDef => ({ room, object, type: 'planted', reveal, condition });
const dead = (room: string, object: string, reveal: string): CardDef => ({ room, object, type: 'deadend', reveal });
const battery = (room: string): CardDef => ({ room, object: 'Spare Battery', type: 'bonus', bonus: 'token', reveal: '+1 Query Token (max 3).' });
const shoes = (room: string): CardDef => ({ room, object: 'Running Shoes', type: 'bonus', bonus: 'move', reveal: 'Move again: up to 2 more rooms this turn.' });

const cards: Record<string, CardDef> = {
  'LIB-01': clue(L, 'Wet sock on the rug', 'A soaked sock, dropped in a hurry. The label inside says SIZE 44.', SIZE44),
  'LIB-02': clue(L, 'Teacup handle', 'The handle of Victor\'s cup is turned to the left. The person who served the poison is left-handed.', LEFT),
  'LIB-03': clue(L, 'Ashtray', 'Fresh cigar ash, still warm. The killer smells of cigar.', CIGAR),
  'LIB-04': dead(L, 'Victor\'s diary', 'Last entry, in Victor\'s handwriting: "Buy birthday candles."'),
  'LIB-05': fake(L, 'Hair on Victor\'s jacket', 'A long grey hair on Victor\'s jacket. The killer has grey hair.', { attr: 'hair', op: '=', value: 'grey' }),

  'GRE-01': clue(G, 'Muddy footprint', 'A deep, muddy footprint between the foxglove beds: SIZE 44.', SIZE44),
  'GRE-02': clue(G, 'Broken branch', 'A branch snapped at head height. The killer is between 1.85 m and 1.90 m tall.', TALL),
  'GRE-03': dead(G, 'Watering schedule', '"Foxglove: Tuesdays only." Nothing about the killer.'),
  'GRE-04': dead(G, 'Plant label', '"Digitalis purpurea. Poisonous!" Now you know the poison, but not the poisoner.'),
  'GRE-05': fake(G, 'Petals on the floor', 'Crushed petals and a strong perfume. The killer smells of lavender.', { attr: 'smell', op: '=', value: 'lavender' }),
  'GRE-06': shoes(G),

  'OBS-01': clue(O, 'Telescope eyepiece', 'The eyepiece is set for someone between 1.85 m and 1.90 m tall.', TALL),
  'OBS-02': clue(O, 'Hair on the telescope', 'A short blond hair caught on the telescope. The killer is blond.', BLOND),
  'OBS-03': dead(O, 'Star chart', '"Full moon tonight." Beautiful, but useless.'),
  'OBS-04': dead(O, 'Security camera', '"W.A.T.S.O.N. rebooting... 11:20 PM." The lens is blurred by the rain.'),
  'OBS-05': fake(O, 'Reading glasses', 'A pair of reading glasses near the window. The killer wears glasses.', { attr: 'glasses', op: '=', value: 'yes' }),
  'OBS-06': battery(O),

  'CHA-01': clue(C, 'Glove on a pew', 'A worn-out LEFT glove. Only the left one is used. The killer is left-handed.', LEFT),
  'CHA-02': clue(C, 'Confessional', 'The confessional smells of cigar smoke. Someone hid here tonight.', CIGAR),
  'CHA-03': dead(C, 'Hymn book', 'Page 42 is torn out. Strange, but it tells you nothing about the killer.'),
  'CHA-04': dead(C, 'Wedding photo', 'Victor & Margaret, 1982. They look happy.'),
  'CHA-05': shoes(C),

  'MUS-01': clue(M, 'Piano bench', 'Blond hair on the velvet of the piano bench. The killer is blond.', BLOND),
  'MUS-02': clue(M, 'Sheet music', 'The ink is smudged by a left hand. The killer is left-handed.', LEFT),
  'MUS-03': dead(M, 'Opera programme', '"Sofia Delacroix sings tonight!"'),
  'MUS-04': dead(M, 'Broken metronome', 'It stopped at 120 bpm. Just a broken metronome.'),
  'MUS-05': fake(M, 'Curtains', 'The heavy curtains smell of incense. The killer smells of incense.', { attr: 'smell', op: '=', value: 'incense' }),
  'MUS-06': battery(M),

  'KIT-01': clue(K, 'Spilled flour', 'A clear footprint in the spilled flour: SIZE 44.', SIZE44),
  'KIT-02': clue(K, 'Top cupboard', 'The foxglove jar was taken from the top cupboard without a stool. The killer is between 1.85 m and 1.90 m tall.', TALL),
  'KIT-03': dead(K, 'Dinner menu', 'Salmon, potatoes, chocolate cake.'),
  'KIT-04': dead(K, 'Grocery list', '"Tea, lemons, candles."'),
  'KIT-05': fake(K, 'Sugar bowl', 'A long red hair in the sugar bowl. The killer has red hair.', { attr: 'hair', op: '=', value: 'red' }),
  'KIT-06': battery(K),

  'CEL-01': clue(W, 'Behind the barrels', 'A half-smoked cigar, hidden behind the barrels. The killer smells of cigar.', CIGAR),
  'CEL-02': clue(W, 'Dusty barrel', 'A blond hair stuck in the cobwebs. The killer is blond.', BLOND),
  'CEL-03': dead(W, 'Poker IOU', '"Bram owes Victor £200,000." A motive... but not the killer\'s profile.'),
  'CEL-04': dead(W, 'Dusty bottle', 'Château Ravenscroft 1956. A very good year.'),
  'CEL-05': fake(W, 'Footprint in the dust', 'A small footprint in the dust: SIZE 38.', { attr: 'shoe', op: '=', value: 38 }),
  'CEL-06': { room: W, object: 'Master Key', type: 'bonus', bonus: 'peek', reveal: 'Peek: look at the top card of any room deck, then put it back.' },
};

export const foxglove: CaseDef = {
  id: 'foxglove-tea',
  title: 'The Foxglove Tea',
  tagline: 'Case N°1 · Ravenscroft Manor · 11:45 PM',
  intro: [
    'Sir Victor Ravenscroft, 70, founder of Ravenscroft Analytics, is found dead in his armchair in the Library, next to a cold cup of tea.',
    'The storm has cut the bridge. The killer is still in the manor, and has planted fake clues to fool you.',
    'Search the rooms, scan the evidence, query W.A.T.S.O.N.\'s guest database and be the first to name the killer.',
  ],
  table: 'guests',
  attributes: [
    { key: 'age', label: 'Age', column: 'age', type: 'number', unit: 'years', options: range(20, 75, 1) },
    { key: 'height', label: 'Height', column: 'height', type: 'number', unit: 'm', decimals: 2, options: range(1.6, 1.95, 0.01, 2) },
    { key: 'shoe', label: 'Shoe size', column: 'shoe', type: 'number', options: range(36, 46, 1) },
    { key: 'hand', label: 'Hand', column: 'hand', type: 'enum', options: ['left', 'right'] },
    { key: 'hair', label: 'Hair', column: 'hair', type: 'enum', options: ['black', 'blond', 'brown', 'grey', 'red', 'white'] },
    { key: 'glasses', label: 'Glasses', column: 'glasses', type: 'enum', options: ['yes', 'no'] },
    { key: 'smell', label: 'Smell', column: 'smell', type: 'enum', options: ['cigar', 'incense', 'lavender', 'motor oil', 'perfume', 'silver polish'] },
  ],
  suspects,
  cards,
  killerId: 'oscar',
  updateEvery: 4,
  startTokens: 3,
  maxTokens: 3,
  updates: [
    { text: 'Height sensors restored: the killer is between 1.85 m and 1.90 m tall.', condition: TALL },
    { text: 'Camera image recovered: the killer is blond.', condition: BLOND },
    { text: 'Air sensor log recovered: the killer smells of cigar.', condition: CIGAR },
  ],
  solutionStory:
    'Oscar Lindqvist poisoned Victor\'s tea with foxglove from the Greenhouse. Victor had found out that his business partner was secretly selling the company\'s data. Oscar then planted fake clues (lavender, grey hair, size 38) to frame Lady Margaret.',
};
