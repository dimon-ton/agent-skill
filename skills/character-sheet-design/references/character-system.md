# Character System Reference

## Principle

To create a character that can wear many outfits while remaining the same person, separate the system into:

1. Character Identity
2. Item Library
3. Outfit Recipes
4. Prompt Adapters, only when a target image tool is known

Final rule:

```text
Character Sheet = Identity
Outfit Library = Clothing
Outfit Recipes = Styling
Prompt Adapters = Tool-specific syntax
```

## Character Identity

This section never changes:

- Face shape
- Facial proportions
- Skin tone
- Hairstyle
- Hair color
- Body proportions
- Age appearance
- Distinctive features

## Item Library

Store clothing as individual items.

For small wardrobes, descriptive names are enough. For larger wardrobes, use stable item IDs and a slot map. See `wardrobe-system.md` for slot maps, compatibility rules, cultural/period clothing, and prompt adapters.

Tops:

- T-shirts
- Tank tops
- Shirts
- Blouses
- Hoodies
- Jackets

Bottoms:

- Jeans
- Shorts
- Skirts
- Trousers

Footwear:

- Sneakers
- Boots
- Sandals
- Heels

Accessories:

- Watches
- Glasses
- Earrings
- Necklaces
- Hats

Props:

- Phone
- Camera
- Books
- Bags

## Outfit Recipes

Combine items into reusable outfits:

- Casual
- Formal
- Business
- Sportswear
- Traditional
- Fantasy
- Beachwear
- Luxury Influencer

## Recommended Sheet Structure

Identity Sheet:

- Front View
- Left Side View
- Right Side View
- Back View
- 3/4 View
- Head Close-Up

Neutral Outfit:

- Plain T-shirt
- Simple jeans
- Basic sneakers

Avoid highly recognizable clothing on the base identity sheet. The AI may begin treating that outfit as part of the character identity.

Expression Sheet:

- Neutral
- Smile
- Happy
- Serious
- Surprised

Pose Sheet:

- Standing
- Walking
- Sitting

## Clothing Metadata

Use this metadata table for each item:

| Field | Example |
| --- | --- |
| Item ID | MC-TOP-03 |
| Slot | TOP |
| Name | White Tank Top |
| Category | Top |
| Color | White |
| Color Hex | #FFFFFF |
| Material | Cotton |
| Pattern | Solid |
| Silhouette | Fitted |
| Fit | Slim Fit |
| Texture | Smooth |
| Style | Casual |
| Season | Hot / All-season |
| Formality | Casual |
| Occasion | Home / Lifestyle |
| Mobility | High |
| Coverage | Medium |
| Visibility | Face clear |
| Compatible With | Denim Shorts |
| Conflicts With | Formal Blazer |
| Required Underlayer | None |
| Tags Short | white fitted cotton tank top |
| Description Long | White fitted cotton tank top with smooth texture |

## Best Practice

Do not create a character sheet tied to a single outfit, such as only a white tank top and black shorts. Do create a character sheet focused on identity. Future outfit changes should be handled through outfit recipes and prompts.

Keep the master sheet model-neutral. If the user names Midjourney, Firefly, Stable Diffusion, ComfyUI, or another generator, create a prompt adapter from the same identity, item library, and outfit recipes instead of rewriting the master sheet around that tool.
