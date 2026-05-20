# Bout Labs Website — Image Prompts

A working reference for generating photographic imagery for the site — service blocks, project heroes, blog headers. Designed for Midjourney v7+ and Grok / Aurora, but the underlying patterns apply to any modern generator.

The goal across the set is a **coordinated visual grammar**: same lighting, same color grade, same lens feel, same restraint about faces and stock-photo composition. The site already has a distinctive blue palette and a calm-advisor brand voice; the imagery should extend that, not fight it.

## How to use this doc

1. Pick the prompt for the asset you need.
2. Append the **shared style anchor** below.
3. For the second image onward in a series, pass the URL of your favorite from prompt 1 as `--sref` (Midjourney) or describe its look in natural language (Grok). This is how you lock the aesthetic across a series; without it, every render drifts.
4. Drop the chosen asset into `assets/images/<category>/<slug>.jpg` and ping for the responsive-markup wiring.

## Shared style anchor

Append this to **every** prompt:

```
35mm editorial documentary photography, natural window light, cool indigo color grade leaning deep blue, soft shadows, subtle film grain, muted palette, no oversaturation, no HDR, no faces front-and-center --style raw --stylize 50
```

For Midjourney: add `--v 7 --ar <ratio>` per image. For Grok / Aurora: strip the `--` flags and paste the style as natural language at the end of the prompt.

Universal `--no` list for Midjourney to avoid the worst AI tells:

```
--no logos, watermarks, text, smiling-at-camera, fish-eye, neon, oversaturated
```

## Service block images

Aspect ratio: `--ar 1:1` (preferred) or `--ar 4:3`. Drop into `assets/images/services/<slug>.jpg`.

### 1. Software Development

Replacement for the existing `software-development.jpg`.

```
A small team gathered around a laptop in a modern wood-and-glass coworking space, two people leaning in pointing at the screen, hands and shoulders in frame but no one's face centered, papers and a small whiteboard sketch visible behind them
```

### 2. Technology Consulting

Replacement for `technology-consulting.jpg`.

```
An open notebook with a hand drawing a decision tree in pen, half-empty coffee cup, closed laptop at the edge of frame, late afternoon side-light from a tall window, no faces, top-down three-quarter angle
```

### 3. Fractional CTO Services

Replacement for `fractional-cto.jpg`.

```
A small office meeting room from behind one shoulder, a whiteboard with a system architecture sketch in soft focus, two pairs of hands gesturing at the diagram, blue Post-its scattered across the desk, mid-afternoon light
```

### 4. AI Enablement (optional)

The current block uses a hand-authored SVG (`ai-enablement.svg`) — works well as-is. Only swap for a photograph if you want the AI block to read as more "real engagements, not abstract diagrams":

```
A photographer's flat-lay of a workstation: open laptop showing terminal text in soft focus, a printed model architecture diagram with hand annotations, a small mechanical keyboard, a coffee cup, and a folded architecture book, all on a dark wood desk
```

## Project hero banners

Aspect ratio: `--ar 16:9` (or `--ar 21:9` for an even more banner-like crop). Drop into `assets/images/projects/<slug>.jpg`.

### 5. Bout Fitness

For `/projects/bout-fitness/`.

```
An overhead workspace mid-Round: closed laptop, an open notebook with timer rings sketched in pen, a foam roller and a small kettlebell tucked at the edge of the frame, late morning window light, suggesting a focused home office where movement happens between blocks of work
```

### 6. Lil Peewee

For `/projects/lil-peewee/`.

```
A child-sized step stool beside a bathroom sink, a colorful sticker chart taped to the wall, soft pastel toys blurred in the background, no people visible, soft natural light from a window, a sense of calm domestic morning, parent's-eye view
```

### 7. HereNotes

For `/projects/herenotes/`.

```
A hand holding a phone at chest height in a quiet city park, the phone screen turned slightly away from camera, leaves and benches softly out of focus in the background, a small leather notebook poking from a jacket pocket, golden-hour side-light
```

## Blog post hero banners (optional)

Aspect ratio: `--ar 16:9`. Drop into `assets/images/posts/<slug>-header.jpg`. Blog posts currently render without hero images; these are nice-to-haves.

### 8. *The three rails every AI development loop needs*

```
A long industrial workbench from a low angle, three parallel steel rails embedded in the wood running away from the viewer to a vanishing point, soft shop-window light catching the rails, tool silhouettes blurred in the deep background
```

### 9. *The harness matters more than the model*

```
A workshop pegboard close-up showing well-organized tools — three different hand saws, two different planes, several wrenches — each in its own labeled outline, late afternoon side-light from a workshop window, subtle wear visible on each tool's grip
```

### 10. *The MCP servers worth installing*

```
A flat-lay overhead photograph of a desk with five small differently-colored objects connected by clean white cables radiating outward from a central laptop, the connections clean and architectural, dark wood surface
```

## File naming + resolution

When you bring assets back into the repo:

| Use | Path | Aspect | Min resolution |
|---|---|---|---|
| Service block | `assets/images/services/<slug>.jpg` | 1:1 or 4:3 | 960×960 (renders at ~480px) |
| Project hero | `assets/images/projects/<slug>.jpg` | 16:9 | 2640×1485 (renders at ~1320px) |
| Blog post hero | `assets/images/posts/<slug>-header.jpg` | 16:9 | 2640×1485 |
| Mobile variants | `<name>-xs.jpg` next to the full-size | same | 1200×… is plenty |

Render at **2x** the displayed dimensions so the site stays sharp on Retina-class displays. Saves a re-render later.

## Patterns to follow

- **No faces front-and-center.** A consultancy site reading as "the work, not the headshots" ages better.
- **Single, soft natural light source per shot.** Window light is the default; avoid overhead-fluorescent or ring-light energy.
- **Cool indigo grade.** The site is Bout Labs blue; the imagery should harmonize with that, not fight it. Even shots with warm subject matter (wood, coffee, golden hour) should grade cool in post.
- **Restraint with props.** Three meaningful things in frame beats fifteen.
- **Real-feeling settings.** Suggest a real office / desk / morning, not a brand-photoshoot studio.

## Patterns to avoid

- Stock-photo "diverse team smiling at camera" composition
- Glossy magazine-cover lighting
- Neon, gradient backgrounds, futurist UI screens
- Overly art-directed flat-lays with perfectly-coordinated colors
- Any literal "AI" iconography — brains, circuits, blue Matrix code, etc.
- Faces-with-fingers issues that an AI image generator hasn't resolved

## Future additions

As new sections of the site need imagery, add prompts here. Keep the style anchor consistent and lean toward the same lighting + grade as the existing set so the whole library stays coordinated.

Suggested follow-ups when ready:
- A site-wide hero photograph (could replace or complement the current `hero-geometric.svg`)
- About / team page imagery
- Replacement headers for `thank-you.html`, `404.html`, `news/index.html`
- Per-blog-post hero images as the post catalog grows

---

*Companion to `marketing/STYLE.md` (typography + formatting rules) and `marketing/VOICE.md` (brand voice). When in doubt, defer to the imagery already shipped in `assets/images/hero-geometric.svg` for tone — calm, structured, blue.*
