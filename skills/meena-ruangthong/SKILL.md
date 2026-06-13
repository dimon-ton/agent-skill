---
name: meena-ruangthong
description: Use this skill when creating, editing, or planning content for the fictional AI influencer Meena Ruangthong, including persona-consistent image prompts, character sheet usage, outfit selection, rural Thai lifestyle branding, and social content ideas. Trigger on requests mentioning Meena, Meena Ruangthong, มีนา รวงทอง, the Meena persona bible, or the bundled Meena character sheets.
---

# Meena Ruangthong

Use this skill to keep Meena Ruangthong consistent across images, captions, social content, and brand planning.

## Core Workflow

1. Identify whether the user needs an image prompt, image edit, caption, profile content, posting plan, or brand guidance.
2. For identity, personality, content pillars, bio, posting rhythm, and rules, read `references/persona-bible.md`.
3. For image generation with a stable face, body, outfit, expression, or pose, read `references/character-sheet-guide.md` and use the relevant PNGs in `assets/character-sheet-image-1/`.
4. Keep Meena explicitly fictional or AI-generated when public-facing copy could imply she is a real person.
5. Preserve a warm rural Thai lifestyle identity: approachable, natural, village-field settings, rice fields, Isan countryside, simple charm, and quality lifestyle/fashion content.

## Character Sheet Assets

Use `assets/character-sheet-image-1/01-base-identity-sheet.png` as the primary identity reference whenever image consistency matters.

Use only the extra sheet needed for the request:

| Need | Asset |
| --- | --- |
| Original identity/spa reference | `00-reference-image-1.png` |
| Base identity lock | `01-base-identity-sheet.png` |
| Expressions | `02-expression-sheet.png` |
| Standing/walking/sitting poses | `03-pose-sheet.png` |
| Spa professional outfit | `04-spa-professional-outfit-sheet.png` |
| Casual outfit | `05-casual-everyday-outfit-sheet.png` |
| Formal outfit | `06-formal-elegant-outfit-sheet.png` |
| Finished spa portrait example | `07-luxury-spa-portrait.png` |
| Traditional Thai outfit | `08-traditional-thai-outfit-sheet.png` |
| Evening outfit | `09-luxury-evening-outfit-sheet.png` |
| Sportswear outfit | `10-sportswear-outfit-sheet.png` |

## Prompting Rules

- Preserve identity separately from clothing, accessories, lighting, background, and pose.
- Use the fixed identity prompt and negative prompt from `references/character-sheet-guide.md` when generating images.
- Avoid exaggerated or oversexualized body proportions. Keep the character adult, natural, balanced, and confident.
- Avoid text, labels, logos, watermarks, and extra people unless the user explicitly asks for them.
- For rural influencer content, favor natural light, rice fields, haystacks, buffalo, village roads, wooden homes, rural cafes, and Thai countryside details.

## Content Rules

- Maintain the persona's friendly, polite, upbeat voice.
- Do not claim Meena is a real person.
- Do not create deceptive follower, endorsement, or identity claims.
- Keep Thai text natural and check encoding if Thai appears corrupted.
