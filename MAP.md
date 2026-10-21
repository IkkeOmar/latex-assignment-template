# Template map

| File | Purpose |
|---|---|
| `main.tex` | Document class, title, TOC, part headings, and the `\input` list. Add one `\input{qN}` per question. |
| `preamble.tex` | Packages, colours, boxes and macros. Rarely edited per question. |
| `q1.tex`, `q2.tex` | One file per question. |
| `fig/` | Vector figures referenced by `\includegraphics`. |
| `Makefile` | `make` compiles, `make clean` removes build artifacts. |

## Macros available in any `qN.tex`

| Macro | Use |
|---|---|
| `\question{n}{short title}{verbatim text}` | Numbered question with blue box and TOC entry. |
| `\partheading{A}{title}{Questions 1--10}` | New part, forces a page break. |
| `\Intro{text}` | Italic lead paragraph under a part heading. |
| `answerbox` | Environment. Purple box for the final result. |
| `questionbox` | Environment. Blue box; already used by `\question`. |
| `parambox` | Environment. Grey box for given values. |
| `\dt` | Renders `delta t`. |
| `\mean{x}` | Renders `<x>`. |

## Adding a question

1. Create `q3.tex`, copy `q1.tex`.
2. Change the number, title and body.
3. Add `\input{q3}` to `main.tex`.
4. `make`.
