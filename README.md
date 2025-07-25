# TimeLoop: Echoes of the Past

A creative 2D puzzle-platformer game built with Python and Pygame.

## 🎮 Game Concept
You are stuck in a time loop! Each run lasts a fixed time. When time resets, your previous self becomes a "ghost" that replays your past actions. Cooperate with your past ghosts to solve puzzles, unlock doors, and escape the loop.

- **Every loop adds a new ghost**: You become your own ally.
- **10 unique levels** with increasing challenge.
- **Choose your character**: Zeno, Nova, Luna, Echo, or Bolt.
- **Parallax backgrounds, animated sprites, and creative UI.**

## 🕹️ Controls
- **Left/Right Arrows**: Move
- **Space**: Jump
- **R**: Start game (from menu)
- **Q**: Quit (from menu)
- **Left/Right (in menu)**: Change character

## 🚀 How to Run
1. **Install requirements:**
   ```bash
   pip install -r timeloop_game/requirements.txt
   pip install cairosvg
   ```
2. **Run the game:**
   ```bash
   python3 timeloop_game/main.py
   ```

## 🗂️ Project Structure
```
timeloop_game/
├── assets/
│   ├── Backgrounds/   # Parallax backgrounds (SVG/PNG)
│   ├── Characters/    # Character sprites (SVG/PNG)
│   ├── Tiles/         # Platform tiles (SVG/PNG)
│   └── sounds/        # Sound effects (WAV)
├── levels/            # level_1.json ... level_10.json
├── core/              # Main game logic
│   ├── game.py
│   ├── player.py
│   ├── ghost.py
│   ├── level_loader.py
│   ├── timer.py
│   └── puzzle.py
├── utils/
│   └── recorder.py
└── main.py            # Entry point
```

## ✨ Features
- Parallax backgrounds
- Animated, selectable characters
- Ghost replay mechanic
- Buttons, doors, moving platforms
- 10 creative levels
- Modern UI and sound effects

## 🖼️ Assets & Credits
- **Sprites, backgrounds, tiles**: [Kenney.nl](https://kenney.nl/assets) (CC0)
- **Sounds**: [Freesound.org](https://freesound.org), [Kenney.nl](https://kenney.nl/assets?q=audio)
- **Font**: Comic Sans MS (system)

## 📝 License
This project is for educational and portfolio use. All third-party assets are used under their respective licenses (mostly CC0). 