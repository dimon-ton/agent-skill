---
name: use-character-sheet
description: Use an existing character sheet correctly for image generation or image editing while preserving character identity. Trigger when the user provides or references a character sheet, persona bible, turnaround sheet, expression sheet, pose sheet, or asks to create new images, outfits, poses, profile pictures, scenes, or variants of the same character without identity drift.
---

# Use Character Sheet

## Goal

Use the character sheet as the source of identity, not as a fixed outfit or fixed scene. Preserve the person. Change only the requested outfit, pose, expression, camera framing, scene, or activity.

If the `character-sheet-design` skill is available and the user asks to redesign the sheet itself, use that skill instead or alongside this one. Use this skill for applying an existing sheet to make new images.

## Required Workflow

1. Inspect the character sheet before writing the final prompt.
2. Extract identity invariants:
   - face shape and facial proportions
   - skin tone
   - age appearance
   - body proportions
   - hairstyle and hair color
   - distinctive features
   - typical expression range
3. Separate non-identity details:
   - outfit
   - jewelry and accessories
   - props
   - pose
   - background
   - lighting
   - art direction
4. Decide what the user wants changed.
5. Build the prompt around stable identity plus requested changes.
6. State constraints that prevent identity drift.
7. Save generated assets non-destructively when working with local files.

## Identity Rules

Preserve:

- the same face, facial proportions, and apparent age
- the same skin tone and body proportions
- the same hairstyle and hair color unless the user explicitly requests a hair change
- the same distinctive facial features
- the same general personality impression if visible in the sheet

Do not preserve by default:

- the exact outfit
- the exact pose
- the sheet layout
- labels, notes, text, logos, or watermarks from the sheet
- background color or reference-page design

Only treat clothing, accessories, or props as identity if the user explicitly says they are permanent character traits.

## Prompt Template

Use this structure for image generation:

```text
Use the provided character sheet as the identity reference for <character name>.
Preserve identity: <face, proportions, skin tone, age appearance, hairstyle, hair color, distinctive features>.
Create: <requested new image>.
Change only: <outfit, pose, expression, scene, framing, activity>.
Outfit/styling: <new clothing or outfit recipe>.
Scene: <environment>.
Composition: <profile picture, full body, waist-up, cinematic frame, etc.>.
Lighting/style: <visual style>.
Constraints: same person as the character sheet; no identity drift; do not copy the reference sheet layout; no labels, notes, watermark, or extra text; avoid changing face, hair, body proportions, or apparent age.
```

## Editing Existing Character Images

When editing an existing generated image of the character:

1. Identify the edit target and the reference sheet separately.
2. Preserve both the target image composition and the character identity unless the user asks to change composition.
3. Make the edit narrow: clothing swap, background change, prop addition, expression change, or pose change.
4. Repeat the invariant constraints in the edit prompt.

## Outfit Changes

For outfit requests, write prompts as a swap:

```text
Keep the same person from the character sheet. Replace only the clothing with <new outfit>. Keep face, hair, age, body proportions, expression style, and skin tone consistent.
```

Avoid wording such as "the character is the girl in the cream blouse" unless the cream blouse is permanent. Prefer "the character from the sheet, currently shown wearing a cream blouse."

## Character Sheet Audit

If the user asks whether they are using a sheet correctly, check:

- Are identity traits separated from outfit traits?
- Is the prompt asking for the same person, not just a similar style?
- Are clothing and scene described as changeable?
- Are there enough views to preserve identity?
- Are expression and pose references being used only when relevant?
- Does the prompt accidentally ask the model to reproduce the sheet layout?

## Output Style

For image tasks, return a ready-to-use prompt and a short note listing the identity invariants and requested changes. If actually generating an image, use the image-generation tool after creating the prompt, then inspect and save the output if it is project-bound.
