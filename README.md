# Custom Wildcard Prompt

A lightweight ComfyUI node that turns `{option one|option two|...}` blocks in your prompt into randomly selected values — one pick per generation, or several if you use multiple blocks. Works with **any model** (SD, SDXL, Flux, Qwen, etc.) and can be wired into **any text input**, including positive or negative prompts.

## Features

- **Wildcard syntax**: `{option one|option two|etc}`
- **Seed control**: fix the seed to freeze the selection, or let it vary per generation.
- **Multiple blocks per prompt**: each `{...}` block is resolved independently.
- **Debug output**: a second `STRING` output shows exactly which options were selected, so you can see what the model actually received.
- **Bracket safety check**: if `{` and `}` counts don't match, the node returns the original text plus a syntax-error message instead of silently producing garbage.

## Syntax

```
{option one|option two|option three}
```

- Options are separated by `|`.
- Whitespace around each option is trimmed.
- Nesting is not supported — the regex matches only the innermost `{...}` without inner braces.
- Empty options are dropped.

### Live examples

**Clothing and color**

```
a woman wearing {a red silk dress|a blue denim jacket|a white linen shirt}, {standing on a beach|sitting in a café|walking through a forest}
```

**Pose and emotion**

```
portrait of a man, {smiling softly|looking away|eyes closed}, {arms crossed|hands in pockets|leaning against a wall}
```

**Background**

```
{cyberpunk city at night|sunlit Italian villa courtyard|misty mountain lake}, cinematic lighting
```

**Negative prompt**

```
{blurry|low quality|extra fingers|watermark}
```

Each generation picks one option per block. With two blocks above, you get 3 × 3 = 9 possible combinations per prompt.

## Seed behavior

- **Fixed seed** → the same options are selected every run.
- **Randomize / increment seed** → a new combination is chosen each generation, like any other ComfyUI node with a seed input.
- The node uses a local `random.Random(seed)` instance, so it does **not** disturb the global random state used by other nodes.

## Installation

### Via ComfyUI Manager

Search for **Custom Wildcard Prompt** in the Manager and install.

### Manual (from console)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/eliseipanov/custom-willdcard-prompt.git
```

Then restart ComfyUI.

> Note: the repository URL above is spelled `custom-willdcard-prompt` (with `willd`). If you rename the repo later, update this line and the `Repository` field in `pyproject.toml`.

## Usage

1. Add the node **🛠️ Custom Wildcard Prompt** (category: `utils/custom`).
2. Type your prompt with `{...}` blocks into the `text` field.
3. Connect the **`final_prompt`** output to the **text input of a text encoder**, not directly to the sampler. The encoder converts the string into `CONDITIONING`:
   - **Qwen Image 2.1**: connect `final_prompt` → `prompt` input of `Text Encode Qwen Image 2.1`, then its `positive` output → sampler's `positive`.
   - **SD / SDXL / Flux**: connect `final_prompt` → `text` input of `CLIP Text Encode`, then its `CONDITIONING` output → sampler's `positive`.
4. The **`debug_info`** output is a plain `STRING` for display only. Connect it to a text viewer such as `Preview Any` or `Show Text` to see which options were selected. Do **not** connect it to the sampler or encoder.
5. For a negative prompt, repeat the same pattern: `final_prompt` → text encoder → sampler's `negative`.

```
final_prompt (STRING) → Text Encode (Qwen 2.1 or CLIP) → positive (CONDITIONING) → Sampler
debug_info (STRING) → Preview Any / Show Text (display only)
```

<img width="1105" height="406" alt="custom-wildcard-prompt" src="https://github.com/user-attachments/assets/dd4e3e80-0572-4fec-a77e-628d121ccbd0" />
*(Screenshot How-to-Use Example)*

## Outputs

| Output | Type | Description |
|---|---|---|
| `final_prompt` | `STRING` | The prompt with all `{...}` blocks resolved. |
| `debug_info` | `STRING` | A `✅ Selected: ...` summary of the chosen options, or a syntax-error message. Usefull with Show Any Node or other text/string preview nodes |

## Roadmap

1. **Priority option** — prefix an option with `^` to force it to always be chosen, e.g. `{Option one|^Option two|etc...}`. Useful when you've found the best variant (e.g. a lighting setup you liked in Qwen Edit 2.1) but don't want to delete the others yet. The `^` stays until you remove it.
2. **Comment blocks** — wrap any part of the prompt in `/* ... */` to exclude it from the output, including any `{prompt|variants}` inside. Useful for temporarily disabling a section without deleting and re-adding it, or for keeping notes next to the prompt.
3. **Partial text locking** — mark a section of the prompt as "do not randomize", so you can edit one part, compare, and restore it without losing the rest.

## Contributing

Found a bug or have a suggestion? Please open an issue or a pull request on GitHub:

- **Issues**: https://github.com/eliseipanov/custom-willdcard-prompt/issues
- **Pull requests**: https://github.com/eliseipanov/custom-willdcard-prompt/pulls

## License

MIT — see [LICENSE](LICENSE).
