# How to Use This Character Sheet Set

This folder contains a reusable character system based on `00-reference-image-1.png`.

## Files

| File | Use |
| --- | --- |
| `00-reference-image-1.png` | Original identity and spa outfit reference |
| `01-base-identity-sheet.png` | Main identity reference; use this first for consistency |
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

1. Upload `01-base-identity-sheet.png` as the main character reference.
2. Upload one outfit sheet if you want a specific outfit.
3. Upload `02-expression-sheet.png` only when you need a specific expression.
4. Upload `03-pose-sheet.png` only when you need a specific pose.
5. Use the fixed identity prompt below in every generation.

## Fixed Identity Prompt

```text
Young adult woman with a soft oval face, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, dark brown to near-black hair styled in a neat elegant updo with soft volume at the crown and tidy swept-back hair, graceful youthful adult appearance, slim natural body proportions.
```

## Identity Lock

```text
Preserve the same face, fair skin tone, large dark brown almond-shaped eyes, softly arched brows, refined nose, full pink lips, neat dark updo hairstyle, youthful adult age appearance, slim natural proportions, and calm graceful presence.

Clothing, earrings, spa uniform, silver sash, background, pose, and lighting are styling only. They are not permanent identity.
```

## Universal Negative Prompt

```text
Avoid: changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, loose long hair replacing the updo, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
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
[portrait / half body / full body / character sheet]

Expression/Pose:
[describe expression and pose]

Constraints:
Preserve identity; clothing is not identity; keep the same face, skin tone, hairstyle, body proportions, and youthful adult age appearance. No text, logos, watermark, or extra people.

Avoid:
[paste Universal Negative Prompt]
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
Young adult woman with a soft oval face, fair smooth skin, gentle balanced facial proportions, large dark brown almond-shaped eyes with natural spacing, softly arched dark eyebrows, small refined nose, naturally full pink lips, subtle rosy blush, calm refined smile, dark brown to near-black hair styled in a neat elegant updo with soft volume at the crown and tidy swept-back hair, graceful youthful adult appearance, slim natural body proportions.

Change only the outfit/styling:
Navy short-sleeve wrap spa uniform top, diagonal silver glitter collar trim and sash, small silver circular buttons, matching navy fitted skirt, small silver drop earrings.

Scene:
Warm luxury spa reception room with soft amber lighting, elegant curtains, polished wood, and neutral decor.

Composition:
Mid-thigh portrait.

Expression/Pose:
Calm professional smile, standing with hands gently folded.

Constraints:
Preserve identity; clothing is not identity; keep the same face, skin tone, hairstyle, body proportions, and youthful adult age appearance. No text, logos, watermark, or extra people.

Avoid:
Changed face, changed eye shape, changed eye spacing, changed skin tone, changed hairstyle color, loose long hair replacing the updo, different person, older or younger age, exaggerated body proportions, heavy makeup, doll-like skin, anime, CGI, illustration, distorted hands, distorted legs, text, labels, logos, watermark, extra people.
```

## Practical Tips

- For the most consistent result, use `01-base-identity-sheet.png` in every generation.
- Use only one outfit sheet at a time unless the goal is to combine outfits.
- If the face changes, regenerate with stronger wording: `same face as the base identity sheet, same eyes, same nose, same lips, same updo`.
- If the clothing leaks into future outputs, add: `the outfit is removable styling, not permanent identity`.
- If the generator adds text or logos, repeat: `no text, no labels, no logos, no watermark`.
