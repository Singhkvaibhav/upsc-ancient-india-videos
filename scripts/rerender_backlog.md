# Re-render backlog

Episodes already delivered that need re-rendering once a later fix has landed.
The user asked (18 November 2026) that these be done **in batches at the end**,
not interrupting the run forward.

## Batch 1 — gallery label overlap (Episodes 1 to 11)

**What is wrong:** in the GALLERY segment the museum label card was drawn on top
of the display cases, covering part of the last case. The label is still
readable, so this is cosmetic.

**The fix:** already in `engine/anc.py` — the label now sits in the clear band
above the cases (rect 1308,126,548,228). Episodes 12 onward are clean.

**To redo:** Ep 1 to 11. Nothing to change in the episode code; just re-run.
Roughly 11 minutes each, so about two hours.

```bash
cd /home/claude/upsc-ancient-india-videos
for N in 1 2 3 4 5 6 7 8 9 10 11; do
  bash tools/run_ep.sh $N "<thumb line 1>" "<thumb line 2>" "<kicker>"
done
```

Thumbnail lines must match the ones used originally, or pass none and keep the
existing `output/youtube/AncNN_thumb.png`.

**Also worth folding into the same batch,** since these landed with the same
commit and improve any scene that uses them:
- P_ROW labels now shrink to fit their cards instead of clipping
- P_TWO body text no longer overlaps the card heading
- Mains tags are measured and centred as a group
- P_SITES clamps pins onto the board
