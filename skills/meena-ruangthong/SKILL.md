---
name: meena-ruangthong
description: Use this skill when creating, editing, or planning content for the fictional AI influencer Meena Ruangthong, including persona-consistent image prompts, character sheet usage, outfit selection, rural Thai lifestyle branding, and social content ideas. Trigger on requests mentioning Meena, Meena Ruangthong, มีนา รวงทอง, the Meena persona bible, the bundled Meena character sheets, or styling keywords such as massive bust.
---

# Meena Ruangthong

Use this skill to keep Meena Ruangthong consistent across images, captions, social content, and brand planning.

## Core Workflow

1. Identify whether the user needs an image prompt, image edit, caption, profile content, posting plan, or brand guidance.
2. For identity, personality, content pillars, bio, posting rhythm, and rules, read `references/persona-bible.md`.
3. For image generation with a stable face, body, outfit, expression, or pose, read `references/character-sheet-guide.md` and use the relevant PNGs in `assets/character-sheet-image-1/`.
4. When the user mentions a screenshot, clothing file, outfit reference, or local `clothes/` folder, inspect the image with `view_image` before prompting. Describe the garment from the image, not from memory.
5. If the image tool cannot attach local reference images, say that briefly and convert the visual references into a strict text prompt using the identity and outfit details.
6. Keep Meena explicitly fictional or AI-generated when public-facing copy could imply she is a real person.
7. Preserve a warm rural Thai lifestyle identity: approachable, natural, village-field settings, rice fields, Isan countryside, simple charm, and quality lifestyle/fashion content.

## Character Sheet Assets

Use `assets/character-sheet-image-1/11-long-hair-identity-sheet.png` as the primary everyday identity reference for rural lifestyle, casual fashion, dance, and social posts.

Use `assets/character-sheet-image-1/01-base-identity-sheet.png` when the request needs the original updo, tied hair, spa/professional styling, or a neutral body/face compatibility master.

Use only the extra sheet needed for the request:

| Need | Asset |
| --- | --- |
| Original identity/spa reference | `00-reference-image-1.png` |
| Updo/base identity lock | `01-base-identity-sheet.png` |
| Expressions | `02-expression-sheet.png` |
| Standing/walking/sitting poses | `03-pose-sheet.png` |
| Spa professional outfit | `04-spa-professional-outfit-sheet.png` |
| Casual outfit | `05-casual-everyday-outfit-sheet.png` |
| Formal outfit | `06-formal-elegant-outfit-sheet.png` |
| Finished spa portrait example | `07-luxury-spa-portrait.png` |
| Traditional Thai outfit | `08-traditional-thai-outfit-sheet.png` |
| Evening outfit | `09-luxury-evening-outfit-sheet.png` |
| Sportswear outfit | `10-sportswear-outfit-sheet.png` |
| Everyday long-hair identity lock | `11-long-hair-identity-sheet.png` |

## Visual Identity Findings

- Face: soft oval face, fair smooth skin, large dark brown almond-shaped eyes, softly arched dark brows, small refined nose, naturally full pink lips, subtle rosy blush, and a calm friendly smile.
- Everyday hair: long dark brown to near-black hair, loose and softly wavy, falling past the shoulders toward mid-back, with relaxed countryside texture.
- Updo hair: neat dark updo with soft crown volume and a few loose face-framing strands; use only when the requested look needs tied hair or the original outfit sheets.
- Body/clothing baseline: adult natural curvy silhouette with balanced proportions; white fitted T-shirt, light blue straight-leg jeans, and white low-top sneakers are the neutral casual baseline.
- Sheet roles: expression and pose sheets use the updo but should transfer only expression or pose unless the user also requests updo hair.

## Prompting Rules

- Preserve identity separately from clothing, accessories, lighting, background, and pose.
- Use the matching fixed identity prompt and negative prompt from `references/character-sheet-guide.md`: long-hair prompt for everyday Meena, updo prompt for original/tied-hair Meena.
- Never paste an updo negative prompt into a long-hair request; it can block the intended loose hair.
- When the user explicitly includes the keyword `massive bust`, inject that body-shape request into the image prompt as: "massive bust, fuller bust silhouette, tasteful adult curvy figure, natural balanced proportions, fully clothed lifestyle fashion styling." Do not add this phrase unless the user asks for it.
- For requested outfit references, explicitly name the source file inspected and prompt the garment details: color, neckline, sleeves/straps, fabric, fit, bottom garment, and any tie/wrap/ruffle details.
- If a clothing reference is revealing, adapt it into a tasteful adult lifestyle version while preserving recognizable non-sensitive details such as color, fabric, wrap construction, and matching bottoms.
- For multiple images, vary pose and camera relationship deliberately: body angle, head turn, chin angle, gaze direction, hand placement, camera height, and whether props are used. Do not reuse the same face/head angle unless the user asks for consistency.
- Avoid exaggerated or oversexualized body proportions. Keep the character adult, natural, balanced, and confident.
- Avoid text, labels, logos, watermarks, and extra people unless the user explicitly asks for them.
- For rural influencer content, favor natural light, rice fields, haystacks, buffalo, village roads, wooden homes, rural cafes, and Thai countryside details.

## Common Pose Patterns

Use these when the user asks for social-media style images:

- Direct camera portrait: front-facing body, direct eye contact, relaxed shoulders.
- Looking away: body angled 30-70 degrees, face turned toward the scene, no eye contact.
- Look back over shoulder: body turned away, head turned back, visible shoulder/back angle.
- Side profile: face near-profile, eyes looking off-frame, nose and jawline visible.
- Seated field pose: knees angled to one side, one hand on lap or grass, relaxed torso.
- Prop pose: one natural prop only, such as a grass flower, held gently without blocking face or outfit.

## Content Rules

- Maintain the persona's friendly, polite, upbeat voice.
- Do not claim Meena is a real person.
- Do not create deceptive follower, endorsement, or identity claims.
- Keep Thai text natural and check encoding if Thai appears corrupted.
