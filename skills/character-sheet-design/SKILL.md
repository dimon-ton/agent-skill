---
name: character-sheet-design
description: Create, revise, audit, or prompt character sheets that preserve a character's identity across many outfits, poses, scenes, and image-generation models. Use when the user asks for a reusable character sheet, identity bible, wardrobe or outfit system, clothing item library, prompt adapter, expression/pose sheet, consistent character prompts, or help separating character identity from clothing and styling.
---

# Character Sheet Design

## Core Rule

Treat the character sheet as identity, not clothing. Keep the person's face, proportions, body, age appearance, skin tone, hair, and distinctive features stable. Put clothing in an item library and combine clothing through outfit recipes.

When the user provides an existing character, first extract the stable identity. Then describe any clothing as removable styling unless the user explicitly says it is permanent.

Read `references/character-system.md` when you need the full schema for identity, clothing metadata, recommended sheet views, expressions, poses, or outfit recipes.

Read `references/wardrobe-system.md` when the task needs many outfit variants, clothing slot maps, item IDs, compatibility rules, cultural/period clothing, or prompt adapters for tools such as Firefly, Midjourney, Stable Diffusion, ComfyUI, or generic image models.

## Workflow

1. Identify the use case: new character sheet, revision, image prompt, outfit expansion, clothing metadata, or consistency audit.
2. Separate the content into three layers:
   - Character Identity: never-changing person traits.
   - Item Library: individual garments, accessories, footwear, and props.
   - Outfit Recipes: reusable combinations of item-library entries.
3. Add a prompt adapter layer only when a target generator or workflow is named; keep the master sheet model-neutral.
4. Build or revise the identity sheet before outfit-specific sheets.
5. Use a neutral outfit for the base identity sheet unless the user requests a culturally or narratively required outfit.
6. For outfit requests, keep identity language fixed and swap only item-library or recipe language.
7. For image prompts, state invariants explicitly: preserve face, hairstyle, body proportions, age appearance, skin tone, and distinctive features.
8. Avoid wording that makes one outfit part of the character's identity unless it is truly permanent.

## Outputs

For a character system, produce:

- Identity Sheet: front, side, back, 3/4, and head close-up.
- Expression Sheet: neutral, smile, happy, serious, surprised.
- Pose Sheet: standing, walking, sitting.
- Item Library: tops, bottoms, footwear, accessories, props.
- Outfit Recipes: named combinations such as casual, formal, traditional, sportswear, fantasy, beachwear, luxury, or user-defined styles.
- Optional Prompt Adapters: generator-specific syntax derived from the same model-neutral master sheet.

For a single image-generation prompt, produce:

- Identity invariants.
- Outfit recipe or item list.
- Scene and composition.
- Constraints that prevent identity drift.
- Avoid list for accidental outfit lock-in, extra people, text, logos, and unwanted style changes.

## Clothing Metadata

For each clothing item, include concise metadata:

`Item ID`, `Slot`, `Name`, `Category`, `Color`, `Color Hex`, `Material`, `Pattern`, `Silhouette`, `Fit`, `Texture`, `Style`, `Season`, `Formality`, `Occasion`, `Mobility`, `Coverage`, `Visibility`, `Compatible With`, `Conflicts With`, `Required Underlayer`, `Tags Short`, `Description Long`, `Reference Links`.

Use this metadata when users want many outfit variants, want consistency across generations, or need a reusable wardrobe system.

Use stable item IDs when a wardrobe has more than a few items. Prefer slot prefixes such as `TOP`, `BTM`, `OUT`, `SHOE`, `ACC`, `HEAD`, and `PROP`, or domain prefixes such as `SW` for sportswear, `FW` for formalwear, and `CP` for cosplay or period clothing.

## Prompt Pattern

Use this structure for image prompts:

```text
Use the character identity exactly: <stable identity traits>.
Change only the outfit/styling: <outfit recipe or item list>.
Scene: <environment>.
Composition: <views, framing, sheet layout, or portrait framing>.
Expression/Pose: <requested expression and pose>.
Constraints: preserve identity; clothing is not identity; no text, logo, watermark, or extra characters unless requested.
Avoid: identity drift, changed face, changed body proportions, changed hair, outfit treated as permanent identity.
```

## Consistency Audit

When reviewing an existing sheet or prompt, flag:

- Outfit details mixed into identity.
- Missing side/back/3/4/head views.
- Missing expression or pose coverage.
- Clothing without item metadata.
- Missing slot map or item IDs for a large wardrobe.
- Missing compatibility rules, conflicts, underlayers, coverage, mobility, or visibility notes.
- Outfit recipes that cannot be recombined.
- Tool-specific prompt syntax mixed into the master sheet instead of separated into prompt adapters.
- Prompt wording that could cause the model to treat clothing as permanent.
