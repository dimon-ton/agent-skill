# How to Use This Character Sheet Set

This folder contains a reusable character system based on `00-reference-image-1.png`.

## Files

| File | Use |
| --- | --- |
| `00-reference-image-1.png` | Original identity and spa outfit reference |
| `01-base-identity-sheet.png` | Updo/base identity reference; use for tied-hair, spa, formal, or compatibility checks |
| `11-long-hair-identity-sheet.png` | Everyday long-hair identity reference for rural, fashion, lifestyle, and dance images |
| `02-expression-sheet.png` | Reference for facial expressions |
| `03-pose-sheet.png` | Reference for standing, walking, and sitting poses |
| `04-spa-professional-outfit-sheet.png` | Spa uniform outfit reference |
| `05-casual-everyday-outfit-sheet.png` | Casual outfit reference |
| `06-formal-elegant-outfit-sheet.png` | Formal outfit reference |
| `07-luxury-spa-portrait.png` | Example finished spa portrait |
| `08-traditional-thai-outfit-sheet.png` | Traditional Thai outfit reference |
| `09-luxury-evening-outfit-sheet.png` | Evening gown outfit reference |
| `10-sportswear-outfit-sheet.png` | Sportswear outfit reference |

## Best Workflow

### Recommended Setup

Use two identity masters:

- `01-base-identity-sheet.png` remains the face/body master and original updo reference.
- `11-long-hair-identity-sheet.png` is the everyday Meena reference for rural, fashion, lifestyle, and dance images.

### Identity Selection

1. Use `11-long-hair-identity-sheet.png` for normal rural, fashion, lifestyle, and dance images.
2. Use `01-base-identity-sheet.png` only when you want the original updo, spa, formal, or tied-hair look.
3. Use outfit, expression, and pose sheets as transfer references only; do not let them overwrite the chosen hairstyle.

### Daily Image Workflow

1. Upload `11-long-hair-identity-sheet.png` as the main character reference for long-hair Meena.
2. Upload one outfit sheet if you want a specific outfit.
3. Upload `02-expression-sheet.png` only when you need a specific expression.
4. Upload `03-pose-sheet.png` only when you need a specific pose.
5. Use the long-hair variant prompt and long-hair negative prompt below.

## Fixed Identity Prompt

```text
Young adult woman with a soft oval face, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, dark brown to near-black hair styled in a neat elegant updo with soft volume at the crown and tidy swept-back hair, natural adult appearance, natural balanced adult proportions.
```

## Long-Hair Variant Identity Prompt

Use this when you want Meena with loose long hair instead of the tidy updo. Keep the face and body identity from `01-base-identity-sheet.png`; change only the hairstyle.

```text
Young adult Thai woman with the same soft oval face as the base identity sheet, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, natural adult appearance, natural balanced adult proportions. Her hair is dark brown to near-black, long, loose, natural, and softly wavy, falling past the shoulders to mid-back, with light face-framing strands and a relaxed countryside look. The hair should feel natural and slightly imperfect, not salon-styled, not tied up, not in a bun, not tidy or swept back.
```

## Identity Lock

```text
Preserve the same face, fair skin tone, large dark brown almond-shaped eyes, softly arched brows, refined nose, full pink lips, neat dark updo hairstyle, adult age appearance, natural balanced adult proportions, and calm graceful presence.

Clothing, earrings, spa uniform, silver sash, background, pose, and lighting are styling only. They are not permanent identity.
```

## Long-Hair Identity Lock

```text
Preserve the same face from the base identity sheet: same fair skin tone, same large dark brown almond-shaped eyes, same softly arched brows, same refined nose, same full pink lips, same adult age appearance, same natural balanced adult proportions, and same calm graceful presence.

Only change the hairstyle from the original updo to loose long dark hair. Hair should be natural, relaxed, softly wavy, slightly imperfect, and untied. Clothing, earrings, background, pose, and lighting are styling only. They are not permanent identity.
```

## Universal Negative Prompt

```text
Avoid: changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, loose long hair replacing the updo, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
```

## Long-Hair Negative Prompt

Use this with the long-hair variant. Do not use the universal negative prompt because it blocks loose long hair.

```text
Avoid: changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, updo, bun, ponytail, tied hair, tidy swept-back hair, short hair, bob haircut, overly perfect salon hair, wet hair, messy dirty hair, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
```

## Generic Image Prompt Template

```text
Create a photorealistic image of the same character.

Use the character identity exactly:
[paste Fixed Identity Prompt]

Change only the outfit/styling:
[choose one outfit recipe below]

Scene:
[describe the location]

Composition:
[portrait / half body / full-length portrait / character sheet]

Expression/Pose:
[describe expression and pose]

Constraints:
Preserve identity; clothing is not identity; keep the same face, skin tone, hairstyle, body proportions, and adult age appearance. No text, logos, watermark, or extra people.

Avoid:
[paste Universal Negative Prompt]
```

## Long-Hair Image Prompt Template

```text
Create a photorealistic image of the same character with loose long hair.

Use the base identity sheet only for the face, skin tone, eyes, nose, lips, age, and body proportions. Do not copy the updo hairstyle.

Use this long-hair identity:
[paste Long-Hair Variant Identity Prompt]

Change only the outfit/styling:
[choose one outfit recipe below]

Scene:
[describe the location]

Composition:
[portrait / half body / full-length portrait / character sheet]

Expression/Pose:
[describe expression and pose]

Constraints:
Preserve identity; the original updo is not identity; clothing is not identity. Keep the same face, skin tone, eye shape, nose, lips, body proportions, and adult age appearance. Hair must be loose, long, dark, natural, softly wavy, and untied. No text, logos, watermark, or extra people.

Avoid:
[paste Long-Hair Negative Prompt]
```

## Long-Hair Character Sheet Prompt

Use this to generate a new long-hair reference sheet from the current base identity sheet.

```text
Create a clean photorealistic character reference sheet of the same young adult Thai woman from the base identity sheet, changing only the hairstyle to loose long dark hair.

Identity:
Young adult Thai woman with the same soft oval face as the base identity sheet, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, natural adult appearance, natural balanced adult proportions.

Hair:
Dark brown to near-black long hair, loose and untied, softly wavy, falling past the shoulders to mid-back, natural volume, light face-framing strands, relaxed countryside style, slightly imperfect and not overly polished. Do not use a bun, updo, ponytail, tidy swept-back style, or short haircut.

Outfit:
Plain fitted white short-sleeve T-shirt, light blue straight-leg jeans, plain white low-top sneakers.

Sheet layout:
Full-body front view, left side view, right side view, back view, three-quarter view, and a close-up head portrait. Neutral gray studio background, even soft light, clean vertical divisions, no labels, no text.

Constraints:
Preserve the same face, fair skin tone, eye shape, eye spacing, brows, nose, lips, adult age appearance, and natural balanced adult proportions from the base identity sheet. Only the hairstyle changes from the original updo to loose long hair.

Avoid:
Changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, updo, bun, ponytail, tied hair, tidy swept-back hair, short hair, bob haircut, overly perfect salon hair, wet hair, messy dirty hair, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
```

## Outfit Recipes

### Spa Professional

```text
Navy short-sleeve wrap spa uniform top, diagonal silver glitter collar trim and sash, small silver circular buttons, matching navy fitted skirt, small silver drop earrings.
```

Use reference: `04-spa-professional-outfit-sheet.png`

### Casual Everyday

```text
White fitted short-sleeve T-shirt, light blue straight-leg jeans, plain white low-top sneakers, optional small beige crossbody bag.
```

Use reference: `05-casual-everyday-outfit-sheet.png`

### Formal Elegant

```text
Cream silk blouse with modest neckline, high-waisted black tailored trousers, black pointed low heels, small pearl stud earrings.
```

Use reference: `06-formal-elegant-outfit-sheet.png`

### Traditional Thai Elegant

```text
Deep sapphire blue Thai silk fitted bodice, silver-gold sabai-style draped sash over one shoulder, matching long Thai silk skirt with tasteful traditional pattern, delicate gold earrings and bracelet.
```

Use reference: `08-traditional-thai-outfit-sheet.png`

### Luxury Evening

```text
Elegant deep emerald satin evening gown, modest V neckline, fitted waist, floor-length skirt, subtle draped structure, delicate gold drop earrings, thin gold bracelet, nude or gold heels.
```

Use reference: `09-luxury-evening-outfit-sheet.png`

### Sportswear

```text
Fitted white performance T-shirt, black high-waisted athletic leggings, lightweight pale blue zip training jacket worn open, white running shoes.
```

Use reference: `10-sportswear-outfit-sheet.png`

## Example Prompt

```text
Create a photorealistic luxury spa portrait of the same character.

Use the character identity exactly:
Young adult woman with a soft oval face, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, dark brown to near-black hair styled in a neat elegant updo with soft volume at the crown and tidy swept-back hair, natural adult appearance, natural balanced adult proportions.

Change only the outfit/styling:
Navy short-sleeve wrap spa uniform top, diagonal silver glitter collar trim and sash, small silver circular buttons, matching navy fitted skirt, small silver drop earrings.

Scene:
Warm luxury spa reception room with soft amber lighting, elegant curtains, polished wood, and neutral decor.

Composition:
Mid-thigh portrait.

Expression/Pose:
Calm professional smile, standing with hands gently folded.

Constraints:
Preserve identity; clothing is not identity; keep the same face, skin tone, hairstyle, body proportions, and adult age appearance. No text, logos, watermark, or extra people.

Avoid:
Changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, loose long hair replacing the updo, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
```

## Practical Tips

- For everyday rural, fashion, lifestyle, and dance images, use `11-long-hair-identity-sheet.png` first. Use `01-base-identity-sheet.png` when the original updo or tied-hair look is required.
- Use only one outfit sheet at a time unless the goal is to combine outfits.
- If the face changes, regenerate with stronger wording: `same face as the base identity sheet, same eyes, same nose, same lips, same updo`.
- For long-hair images, say: `same face as the base identity sheet, same eyes, same nose, same lips, but loose long dark hair instead of the updo`.
- For long-hair images, do not paste the universal negative prompt because it includes `loose long hair replacing the updo`.
- If the clothing leaks into future outputs, add: `the outfit is removable styling, not permanent identity`.
- If the generator adds text or logos, repeat: `no text, no labels, no logos, no watermark`.
