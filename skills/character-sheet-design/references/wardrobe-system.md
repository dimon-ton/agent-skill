# Wardrobe System Reference

Use this reference when a character sheet must support many outfit variants, reusable clothing pieces, cultural or period outfits, or multiple image-generation tools.

## Core Model

Keep the master sheet model-neutral:

```text
Character Identity = stable person
Item Library = reusable clothing, accessories, footwear, props
Outfit Recipes = named combinations of item IDs
Prompt Adapters = tool-specific syntax generated from the same master data
```

Do not put Midjourney, Firefly, Stable Diffusion, or ComfyUI syntax directly into the master character sheet. Create an adapter only after the target tool is known.

## Slot Map

Create a slot map before writing many clothing items:

| Slot | Use |
| --- | --- |
| `BASE` | underlayer, shirt, blouse, tank, dress base |
| `TOP` | visible top when not an underlayer |
| `BTM` | trousers, skirt, shorts, leggings |
| `OUT` | jacket, coat, cloak, shell, outerwear |
| `SHOE` | sneakers, boots, sandals, heels |
| `HEAD` | hat, hood, crown, helmet, headpiece |
| `ACC` | jewelry, glasses, belts, bags, small wearables |
| `PROP` | handheld or scene props |
| `MOTIF` | recurring trim, embroidery, symbol, pattern |

Use stable item IDs when a wardrobe has more than a few items:

```text
MC-TOP-03 = modern casual top 03
SW-SHOE-02 = sportswear shoe 02
FW-MAIN-01 = formalwear main piece 01
CP-HED-01 = cosplay/period headwear 01
```

## Item Metadata

For each item, capture practical generation controls, not only visual labels:

| Field | Purpose |
| --- | --- |
| `item_id` | stable ID used by recipes |
| `slot` | one slot from the slot map |
| `name` | human-readable item name |
| `desc_long` | full visual description |
| `tags_short` | compact prompt phrase |
| `category` | garment, footwear, accessory, prop, motif |
| `color_name` | common color name |
| `color_hex` | approximate color value when useful |
| `material` | cotton, denim, silk, leather, armor, etc. |
| `pattern` | solid, stripe, floral, embroidery, print |
| `texture` | smooth, ribbed, matte, glossy, quilted |
| `silhouette` | fitted, boxy, A-line, straight, cropped, oversized |
| `fit` | slim, regular, relaxed, tailored |
| `season` | hot, mild, cold, wet, all-season |
| `formality` | casual, smart casual, business, formal, ceremonial |
| `occasion` | portrait, action, travel, stage, school, beach, gala |
| `mobility` | low, medium, high |
| `coverage` | low, medium, high |
| `visibility` | face clear, face partial, hands clear, body obscured |
| `compatible_with` | item IDs or slots that work well |
| `conflicts_with` | items, slots, poses, or contexts to avoid |
| `required_underlayer` | required base item or none |
| `reference_links` | source images, boards, or notes when available |

## Compatibility Rules

Write explicit rules when the outfit can fail visually:

- State required underlayers for transparent, open, armor, ceremonial, or period pieces.
- Mark face-obscuring headwear as `visibility=face_partial` or `face_hidden`.
- Mark bulky outerwear, long trains, armor, or tight skirts with reduced `mobility`.
- Note when necklaces conflict with collars, chokers, scarves, or high necklines.
- Note when props require a hand pose.
- For cultural, ceremonial, or period looks, record source, region, era, strictness, and no-mix rules.

## Outfit Recipes

Write recipes as item-ID combinations plus intent:

```text
portrait = BASE + BTM + SHOE + ACC
travel = BASE + OUT + BTM + SHOE + PROP
formal = BASE + MAIN + SHOE + ACC
action = BASE + BTM + SHOE + no face-obscuring headwear
```

Each recipe should include:

- `name`
- `intent`
- `item_ids`
- `required_items`
- `optional_items`
- `excluded_items`
- `pose_notes`
- `avoid`

## Prompt Adapters

Create prompt adapters from the master sheet after the user names a target tool.

Generic image model:

```text
Use the character identity exactly: <identity>.
Change only clothing: <recipe name and item tags_short>.
Scene: <scene>.
Composition: <framing>.
Constraints: preserve identity; clothing is not identity; no text, logos, watermark, or extra people unless requested.
Avoid: identity drift, outfit lock-in, incompatible layers, face-obscuring items unless requested.
```

Midjourney-style adapter:

```text
<identity>, wearing <recipe tags_short>, <scene>, <composition>, consistent character, character sheet, no text, no logo --style raw
```

Stable Diffusion or ComfyUI adapter:

```text
Positive: <identity>, <recipe tags_short>, <scene>, <composition>, consistent face, consistent body proportions
Negative: identity drift, different person, changed face, changed hairstyle, text, logo, watermark, extra people, incompatible clothing layers
Control inputs: use reference image, pose/control image, or regional prompt only when the workflow supports it.
```

Firefly-style adapter:

```text
Prompt: <identity> in <recipe tags_short>, <scene>, <composition>.
Settings note: keep reference image/character reference active when available; avoid text and logos unless explicitly required.
```

## Minimum Checklist

Before calling a wardrobe system reusable, check:

- Identity is separate from clothing.
- Slot map exists.
- Every major clothing item has a stable item ID.
- Items include silhouette, fit, material, pattern, texture, color, season, formality, occasion, mobility, coverage, and visibility.
- Accessories and props are separate from garments.
- Compatibility, conflicts, and required underlayers are recorded.
- At least three recipe presets exist, such as portrait, action, and formal or seasonal.
- Prompt adapters are separate from the master sheet.
