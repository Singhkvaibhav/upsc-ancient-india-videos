# Ancient India, Simply Unearthed

Animated 5-minute explainers of UPSC Ancient Indian History: 44 episodes in 8 units, from the Stone Age to the Rajput kingdoms. Unlike its sibling series' bright paper style, this one is drawn as **carved stone and terracotta in a lamp-lit museum**, and each episode adds an exhibit to a growing gallery.

- `scripts/episode_plan.md`: all 44 episodes, their exhibits and status
- `scripts/sample_ep04.md`: the sample script that sets the format
- `CLAUDE.md`: instructions the Claude Code cloud session reads automatically
- `output/`: finished videos, captions, and YouTube descriptions and thumbnails

## Messages to paste into the cloud session
Paste one at a time, waiting for each to finish.

1. **Build the new look:**
   > Read CLAUDE.md and run setup.sh. Do the "First task: build the new look" section: engine/stone.py, engine/anc.py and engine/museum.py, the new palette, fonts and sounds, and adapt tools/ for Ancient India. Show me 3 stills (stone, museum and trench backgrounds) and stop.
2. **Test episode** (after you like the stills):
   > Render Episode 4 from scripts/sample_ep04.md as the test episode. Push it and show me 4 stills.
3. **Scripts for a unit** (start with Unit 1):
   > Write the Unit 1 scripts (Episodes 1–3, 5 and 6) following CLAUDE.md. Push them and stop. Don't render until I approve.
4. **After you've reviewed them on GitHub:**
   > Unit 1 scripts are approved. Render Episodes 1–3, 5 and 6.
5. Repeat steps 3 and 4 for Units 2–8, changing the unit and episode numbers.
