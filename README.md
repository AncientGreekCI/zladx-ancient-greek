# zladx-ancient-greek
A complete Ancient Greek (Koine) fan translation patch for The Legend of Zelda: Link's Awakening DX.

# The Legend of Zelda: Link's Awakening DX – Ancient Greek Translation

One of the problems of learning Ancient Greek is the lack of diverse content to develop fluency. Thankfully we are slowly getting more readers, podcasts, videos, and even music. I’ve been thinking (and I don’t think I’m the only one) it would be cool if we had more games!

After seeing someone supposedly create a Classical Greek translation of Pokemon LeafGreen (presumably using AI) and coming across a post on r/claude demonstrating Claude's ability to translate retro games, I thought I’d give it a go. I have zero coding experience but, why not?

Link’s Awakening DX seemed a good candidate since it has a community `zladx` disassembly on GitHub. There isn’t too much dialogue but enough to make it worthwhile. And though I haven’t finished it, its gameplay is more interesting than Zelda 1 and 2 in Attic Greek.

So with only a free-tier of Claude and starting with a simple prompt—“how do I make an Ancient Greek translation of Zelda: Link’s Awakening”—I present the results.

## The Translation Pipeline

Because I kept hitting the free usage limits for Claude, I used Claude to assemble the patch and change the font, but outsourced the actual text translation to Gemini. 

For selfish reasons, I wanted the script translated into Koine Greek, restricting vocabulary and syntax to the New Testament, the Septuagint, and *Athenaze*. 

Obviously, it’s not going to be a perfect translation that will please everyone, but I did try to maintain consistency. I didn’t think there would be too many modern words but there were a few that required some creativity or compromise (e.g., boomerang, raccoon, telephone). The game's strict 16-character line limits mean the translation is more functional than literal. 

Unfortunately, it was technically easier to just use unaccented capitals. Just imagine you're reading an ancient manuscript.

## How to Play

1. **Source the ROM:** Obtain a legally sourced English ROM of *The Legend of Zelda: Link's Awakening DX* (Version 1.0 or Revision A).
2. **Download the Patch:** Go to the **Releases** section on the right side of this GitHub page and download the `.IPS` patch matching your ROM version.
3. **Apply the Patch:** Use a web patching tool such as [RomPatcher.js](https://www.marcrobledo.com/RomPatcher.js/) to apply the `.IPS` file to your ROM.
4. **Save and Play:** Save the newly patched ROM to your device and load it into a Game Boy Color emulator (such as mGBA, SameBoy, or PyBoy).

*Note: This repository contains only the translation patch and text modifications. It does not contain the original game ROM.*

---

## Translation Methodology & Prompt

For transparency and for anyone looking to replicate this zero-coding AI workflow, below is the exact system prompt, ruleset, and glossary used to generate the translation through Gemini.

### Language & Length Rules

1. **Ancient Greek only.** No Modern Greek words or forms. Prefer vocabulary found in the Greek New Testament and the Septuagint (LXX); where none exists, use a classical word. Use simple syntax of beginner-textbook level (Athenaze): short sentences, common tenses, few rare constructions.
2. **Write proper polytonic Greek:** accents, breathings, iota subscripts, normal capitalisation (sentence case, capitalised names). Use the Greek question mark ";" and the raised dot "·". No Latin letters anywhere, except the game symbols listed below.
3. **Tone:** The player is addressed in the second person singular. Keep each speaker's tone (friendly, gruff, silly) but never use slang; render exclamations with simple Greek interjections.
4. **Names and invented words:** transliterate with Greek letters; keep them indeclinable (do not add case endings). Use the glossary below for ALL names, items and places. If the English contains a glossary term, use the glossary Greek, in the case the sentence needs. Never invent a second translation for a glossary term.
5. **Translate meaning, not word-for-word.** Keep jokes only if they survive; otherwise give a plain sentence with the same function in the game.
6. **Length Rules:** Text is shown 16 letters per line, and the game has almost no spare memory: EVERY entry must take NO MORE wrapped lines than the English. Method: wrap the English at 16 letters per line (break at spaces) and count the lines; wrap your Greek the same way; if your Greek has more lines, shorten it. Fewer lines is fine. No single word may exceed 16 letters.
7. **Formatting:** Numbers stay as digits (28, 980, ...). Keep the symbols exactly as in the English: ##### (the player's name, never inflect it; use it only where a vocative or a bare name works), `<left>`, `<right>`, `<dpad>`, `<down>` and any other word in angle brackets.

### Standard Phrases

*   "You got X!" / "You've got X!" -> Ἔλαβες … !
*   "You found X!" -> Εὗρες … !
*   Surprise ("Wow!", "Aye Caramba!") -> Βαβαί!
*   "Hey!" (calling) -> Ἄκουε!
*   "Good luck!" -> Εὐτύχει!
*   "Come back when you have X" -> Ἐπάνελθε ὅταν ἔχῃς …
*   "Thanks" -> Εὐχαριστῶ σοι
*   "kid" -> παιδίον
*   "little buddy" -> ὦ φίλε
*   "Press the button" -> Πίεζε τὸ πλῆκτρον
*   "Beware of X" -> Βλέπε τὸν X!
*   "Do you want ...?" -> Βούλει …;
*   "Try again?" -> Πάλιν πειρᾶσθαι;

### Glossary (English to Koine Greek)

**Names**
*   Link = Λίνκ
*   Zelda = Ζέλδα
*   Marin = Μαρίνη (acc. Μαρίνην)
*   Tarin = Ταρῖνος (gen. Ταρίνου)
*   Papahl = Παπάλ
*   Crazy Tracy = Τρέισι ἡ μαινομένη
*   Ulrira = Οὐλρίρα
*   MeowMeow = Μιαουμιάου (κυρία Μιαουμιάου)
*   Mr. Write = ὁ Γραφεύς (gen. Γραφέως, acc. Γραφέα)
*   Richard = Ῥιχάρδος (gen. Ῥιχάρδου)
*   Sale's = Σάλης
*   Martha = Μάρθα
*   Yoshi = Ἰώσι

**Places**
*   Koholint = Κοχόλιντ (ἡ νῆσος Κοχόλιντ)
*   Mabe Village = ἡ κώμη Μαβή
*   Tamaranch = τὸ ὄρος Ταμαράν
*   Tal Tal = Τάλ Τάλ
*   Toronbo = Τορόνβο
*   Goponga = Γοπόγγα
*   Kanalet = Κανάλετ
*   Ukuku = Οὐκούκου
*   Yarna = Ἰάρνα
*   Tabahl = Ταβάλ
*   Village = ἡ κώμη
*   Woods/Forest = ὁ δρυμός
*   Beach/Shore = ὁ αἰγιαλός
*   Castle = τὸ φρούριον
*   Bay = ὁ κόλπος
*   Desert = ἡ ἔρημος
*   Prairie = τὸ πεδίον
*   Swamp = τὸ ἕλος
*   Cemetery = τὰ μνημεῖα
*   Library = ἡ βιβλιοθήκη
*   Bridge = ἡ γέφυρα
*   Mountain = τὸ ὄρος (pl. τὰ ὄρη)
*   Telephone = τὸ τηλέφωνον (coinage)
*   Warp Hole = ἡ ὀπὴ μεταβάσεως

**Dungeons**
*   Tail Cave = τὸ σπήλαιον τῆς οὐρᾶς
*   Bottle Grotto = τὸ σπήλαιον τοῦ ἀσκοῦ
*   Key Cavern = τὸ σπήλαιον τῆς κλειδός
*   Angler's Tunnel = ἡ διῶρυξ τοῦ ἁλιέως
*   Catfish's Maw = τὸ στόμα τοῦ σιλούρου
*   Face Shrine = τὸ ἱερὸν τοῦ προσώπου
*   Eagle's Tower = ὁ πύργος τοῦ ἀετοῦ
*   Turtle Rock = ἡ πέτρα τῆς χελώνης
*   Wind Fish's Egg = τὸ ᾠὸν τοῦ ἰχθύος
*   Level 1-8 = Πρῶτον, Δεύτερον, Τρίτον, Τέταρτον, Πέμπτον, Ἕκτον, Ἕβδομον, Ὄγδοον
*   Dungeon = ὁ λαβύρινθος

**Story Concepts**
*   Wind Fish = ὁ ἰχθὺς τοῦ ἀνέμου
*   Ballad = τὸ ᾆσμα
*   Siren/Sirens = οἱ Σειρῆνες (τὰ ὄργανα τῶν Σειρήνων)
*   Nightmare/Nightmares = ὁ Ἐφιάλτης (pl. οἱ Ἐφιάλται)
*   Owl = ἡ γλαῦξ (hoot = Κικαῦ)
*   Monster/Monsters = τὸ θηρίον
*   Enemy/Enemies = ὁ ἐχθρός
*   Raccoon = ἡ ἀλώπηξ (fox, deliberate)
*   Hen = ἡ ὄρνις
*   Toadstool/Mushroom = ὁ μύκης
*   Fish = ὁ ἰχθύς
*   Fishing = ἁλιεύειν
*   Bottle = ὁ ἀσκός

**Items and Money**
*   Rupee/Rupees = ἡ δραχμή (pl. δραχμαί)
*   Heart Container = τὸ ἀγγεῖον τῆς καρδίας
*   Piece of Heart = τὸ μέρος καρδίας
*   Piece of Power = τὸ μέρος δυνάμεως
*   Heart/Hearts = ἡ καρδία
*   Sword = ἡ μάχαιρα
*   Shield = ὁ θυρεός / Mirror Shield = ὁ θυρεὸς τοῦ κατόπτρου
*   Bomb/Bombs = τὸ πυρίβολον (coinage)
*   Bow & Arrow = τὸ τόξον καὶ τὰ βέλη
*   Arrow/Arrows = τὸ βέλος (pl. βέλη)
*   Keys (Nightmare, Tail, Slime, Angler, Face, Bird) = ἡ κλεὶς τῶν Ἐφιαλτῶν / τῆς οὐρᾶς / τῆς ἰλύος / τοῦ ἁλιέως / τοῦ προσώπου / τῆς ὄρνιθος
*   Ocarina = ὁ αὐλός
*   Power Bracelet = τὸ ψέλιον τῆς δυνάμεως
*   Hook Shot = τὸ ἄγκιστρον
*   Magic Rod = ἡ ῥάβδος ἡ μαγική
*   Pegasus Boots = τὰ ὑποδήματα τοῦ Πηγάσου
*   Roc's Feather = τὸ πτερὸν τοῦ μεγάλου ὄρνεος
*   Shovel = ἡ σκαπάνη
*   Magic Powder = ἡ κόνις ἡ μαγική
*   Flippers = τὰ πτερύγια
*   Magnifying Lens = ἡ ὕαλος ἡ μεγαλύνουσα
*   Secret medicine = τὸ φάρμακον τὸ ἀπόκρυφον
*   Doll = τὸ παίγνιον
*   Guardian Acorn = ἡ βάλανος ἡ φυλάττουσα
*   Seashell = τὸ κογχύλιον (Secret Seashell = τὸ κογχύλιον τὸ κρυπτόν)
*   Gold Leaf = τὸ χρυσοῦν φύλλον
*   Fishhook = τὸ ἁλιευτικὸν ἄγκιστρον
*   Stick = τὸ ξύλον
*   Honeycomb = τὸ κηρίον
*   Sea Urchin = ὁ ἐχῖνος
*   Canned food / dog food = τὸ βρῶμα ἐν ἀγγείῳ
*   Raft = ἡ σχεδία
*   Pineapple = ὁ ἀνανᾶς (transliteration, coinage)
*   Broom = τὸ κόρημα

**Siren Instruments**
*   Full Moon Cello = ἡ κιθάρα τῆς πανσελήνου
*   Conch Horn = ἡ σάλπιγξ τοῦ κόγχου
*   Sea Lily's Bell = ὁ κώδων τοῦ κρίνου τῆς θαλάσσης
*   Surf Harp = τὸ ψαλτήριον τοῦ κλύδωνος
*   Wind Marimba = τὸ ξυλόφωνον τοῦ ἀνέμου (coinage)
*   Coral Triangle = τὸ τρίγωνον τοῦ κοραλλίου
*   Organ of Evening Calm = τὸ ὄργανον τῆς ἑσπερινῆς γαλήνης
*   Thunder Drum = τὸ τύμπανον τῆς βροντῆς

**Interface**
*   Button = τὸ πλῆκτρον
*   START = τὸ πλῆκτρον ἀρχῆς
*   SELECT = ἡ ἐκλογή 
*   Subscreen = ἡ ἀποθήκη
*   Map = ὁ χάρτης
*   Compass = ἡ πυξίς
