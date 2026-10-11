LINK'S AWAKENING DX - ANCIENT GREEK
Translated: ALL dialogue (IDs 000-2AF, 665 entries) and the menus (file select, name entry, erase/copy, save menu, Game Over). Left in English on purpose: the title-screen logo and copyright line. Not done: credits, polytonic accents.

TO PLAY
1. Find which version of the English DX ROM you have. In PowerShell run
      Get-FileHash -Algorithm MD5 yourfile.gbc
   07c211479386825042efb4ad31bb525f  ->  use LA_Greek_v1.0.ips   (original release)
   ccbb56212e3dbaa9007d389a17e9d075  ->  use LA_Greek_RevA.ips   (Rev A, the "SGB Enhanced" file)
   7351daa3c0a91d8f6fe2fbcca6182478  ->  use LA_Greek_RevB.ips   (Rev B)
   Use a patch ONLY on the matching, unmodified ROM. The wrong version leaves English fragments in the text.
2. Apply the patch with a patcher, for example the free browser tool "RomPatcher.js" or "Floating IPS (Flips)".
3. Open the patched ROM in an emulator.
Only patches are shared, never the game itself.

SPARE ROOM LEFT per dialogue bank (bytes): dialog_1 383, dialog_2 356, dialog_3 874, dialog_4 405, dialog_dx 983.

FILES (Claude runs these)
- greek_dialog.txt    the master translation in full polytonic Greek; the converter turns it into capitals for the game
- glossary.txt        the agreed Greek for names, items, places
- GEMINI_PROMPT.txt   is built from prompt_template.txt + glossary.txt with build_prompt.py
- check_translation.py  checks a batch against the English source and merges the clean entries
- build_all.py        ONE STEP: dialogue + menus -> Greek ROMs for v1.0/Rev A/Rev B and a verified patch for each
- apply_menus.py      menus: Greek words in the file-menu layouts, redrawn headings, save menu and Game Over lettering
- apply_greek.py, make_patch.py, apply_ips.py, preview.py   build tools
