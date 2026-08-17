# Dark Kingdom

A text-based RPG adventure that runs in the terminal. Choose a character, fight your way through the Dark Forest, gear up at the Castle Merchant, and face down the Dark King in a final showdown.

## Features

- Three playable characters (Warrior, Wizard, Rogue), each with their own stats and special attack
- Turn-based combat with regular attacks, special attacks (with cooldowns), critical hits, and potions
- A branching path through the castle (Armory or Dungeon) with random enemy encounters
- A merchant shop for buying weapons and upgrades between fights
- A multi-stage final boss battle against the Dark King

## Requirements

- Python 3.7+
- No external dependencies — uses only the standard library (`time`, `random`)

## How to run

```bash
python3 DarkKingdom.py
```

Follow the on-screen prompts to choose your character and make decisions throughout the story.

## Notes

Colored text is done with raw ANSI escape codes, so it displays best in a terminal that supports them (most Linux/macOS terminals and modern Windows terminals). If you see garbled characters instead of colors, try running it in Windows Terminal or WSL.
