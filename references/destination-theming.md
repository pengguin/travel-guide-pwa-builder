# Destination-aware theming

Use this reference when creating a new guide, adapting a guide to another destination, or changing its brand palette.

## Start from place, not nationality

Choose two or three visual anchors from the actual route:

- landscape: alpine snow, chalk desert, tropical canopy, coast, volcanic rock;
- built environment: brick, glazed tile, limestone, timber, concrete, neon;
- light and season: dry autumn, winter blue, humid summer, high-altitude glare;
- trip character: expedition, heritage, food, rail, city, slow travel.

Do not default to national flag colors. They often produce loud interfaces and can flatten a multi-region trip into a stereotype.

## Map anchors to semantic tokens

- `paper` and `surface`: quiet local material or atmospheric neutral;
- `ink`: near-black with a slight destination tint;
- `primary`: the darkest recognizable place color, used for navigation and large fields;
- `secondary`: one accessible accent for actions, time markers, and key states;
- `highlight`: a warmer or brighter supporting accent used sparingly;
- `soft`: a low-chroma tint for chips and secondary panels;
- `danger`: reserved for genuine risks and errors, not destination decoration.

Keep text contrast at WCAG AA where practical: 4.5:1 for ordinary text and 3:1 for large text and essential UI boundaries. Check white text on both `primary` and `secondary`; if the accent is too light, use dark text or darken the accent.

## Bundled theme families

- `heritage`: parchment, indigo-green, fired clay, old gold;
- `desert`: sand, basalt, rust, saffron;
- `mountain`: snow, spruce, alpine blue, amber;
- `coast`: sea mist, navy, teal, coral;
- `forest`: warm cream, evergreen, moss, copper;
- `tropical`: pale sand, jungle green, lagoon blue, mango;
- `polar`: ice grey, midnight blue, glacier cyan, signal red;
- `urban`: cool paper, charcoal, cobalt, muted magenta.

These are starting systems, not destination claims. A coastal heritage city may still use `heritage`; a high-desert route may use `desert` even when the country also contains mountains.

## Review checklist

1. Compare the palette with the route's three most representative local images.
2. Test hero, navigation, buttons, badges, warnings, map fallback, and print styles.
3. Check light surfaces in outdoor brightness and dark fields in low light.
4. Verify theme and background colors in the manifest and launch shell.
5. Recolor or regenerate the app icon so it belongs to the same system.
6. Confirm the new guide is visibly distinct from prior guides without changing its information architecture.
