---
name: Industrial elegant supply chain dashboard with Neo4j.
colors:
  surface: '#f9f9fd'
  surface-dim: '#d9dadd'
  surface-bright: '#f9f9fd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f7'
  surface-container: '#ededf1'
  surface-container-high: '#e8e8ec'
  surface-container-highest: '#e2e2e6'
  on-surface: '#1a1c1f'
  on-surface-variant: '#41484a'
  inverse-surface: '#2f3034'
  inverse-on-surface: '#f0f0f4'
  outline: '#71787a'
  outline-variant: '#c1c8ca'
  surface-tint: '#3d646e'
  primary: '#00242b'
  on-primary: '#ffffff'
  primary-container: '#0e3a43'
  on-primary-container: '#7ca4ae'
  inverse-primary: '#a5cdd8'
  secondary: '#645e4c'
  on-secondary: '#ffffff'
  secondary-container: '#ece2cb'
  on-secondary-container: '#6b6452'
  tertiary: '#470300'
  on-tertiary: '#ffffff'
  tertiary-container: '#6e0b01'
  on-tertiary-container: '#fc745c'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c0e9f5'
  primary-fixed-dim: '#a5cdd8'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#244c56'
  secondary-fixed: '#ece2cb'
  secondary-fixed-dim: '#cfc6b0'
  on-secondary-fixed: '#201b0d'
  on-secondary-fixed-variant: '#4c4636'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a6'
  on-tertiary-fixed: '#3f0300'
  on-tertiary-fixed-variant: '#881f10'
  background: '#f9f9fd'
  on-background: '#1a1c1f'
  surface-variant: '#e2e2e6'
typography:
  h1:
    fontFamily: Sora
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  h3:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Source Sans 3
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Source Sans 3
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Source Sans 3
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  label-caps:
    fontFamily: Sora
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 24px
  margin: 32px
---

## Brand & Style

This design system is engineered for the high-stakes world of global logistics and supply chain management. It evokes a sense of "Industrial Elegance"—combining the rugged reliability of heavy industry with the sophisticated precision of modern data science. The target audience consists of logistics directors and data analysts who require high-density information without cognitive fatigue.

The aesthetic follows a **Corporate / Modern** approach with **Tactile** undertones. It utilizes soft textures to mimic technical materials and subtle gradients to provide depth. The interface feels established and grounded, using its color palette to differentiate between structural stability (Petroleum Blue) and human-centric interaction points (Warm Sand and Vibrant Coral).

## Colors

The palette is anchored by **Petroleum Blue**, used for primary navigation and deep structural elements to convey authority. **Smoke White** serves as the primary canvas, ensuring maximum legibility and a clean, airy workspace.

**Warm Sand** is employed as a secondary surface color to soften the industrial edge, used primarily for sidebar backgrounds or secondary card states. **Vibrant Coral** is the functional accent, reserved strictly for calls to action, critical alerts, and Neo4j graph nodes that require immediate attention. **Graphite Gray** provides the necessary contrast for secondary text and borders, maintaining a professional hierarchy.

## Typography

This design system utilizes a dual-typeface strategy to balance character with utility. **Sora** brings a geometric, technical feel to headlines and titles, reflecting the precision of supply chain nodes and data points. Its wide stance ensures that dashboard sections are clearly demarcated.

**Source Sans 3** is the workhorse typeface for all body copy, data tables, and labels. It is chosen for its exceptional legibility at small sizes and its neutral, professional tone. Letter spacing is slightly tightened for headlines to maintain impact, while labels use all-caps with increased tracking to differentiate them from standard prose.

## Layout & Spacing

The layout is built on a **12-column fluid grid** designed for desktop density. A base 8px rhythm governs all spatial relationships. Dashboard cards should ideally span 3, 4, 6, or 12 columns depending on data complexity. 

Gutters are kept consistent at 24px to provide ample breathing room between complex data visualizations. For the Neo4j graph explorer, the layout transitions to a full-screen "Canvas" mode with a 32px safe-area margin to ensure the UI does not feel cramped during deep-dive analysis.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and **Tonal Layers**. Rather than using harsh black shadows, this design system uses a diffused Petroleum Blue tint for its shadows (`rgba(14, 58, 67, 0.08)`), which makes elevated elements feel integrated into the industrial environment.

Backgrounds feature a very subtle "noise" or "grain" texture (2% opacity) to eliminate the sterile feel of flat digital surfaces. Cards use a two-step depth model:
1. **Surface:** Smoke White cards on a Warm Sand background.
2. **Elevated:** Smoke White cards with a soft shadow when hovered or active.

Subtle linear gradients (e.g., Petroleum Blue to a 10% lighter shade) are used on primary buttons and header bars to imply a tactile, metallic sheen.

## Shapes

The shape language is consistently **Rounded**, utilizing a base radius of 8px for standard components and 12px for primary dashboard cards. This softens the "industrial" feel, making the data feel more approachable and modern.

Graph nodes within the Neo4j visualization should be perfect circles, while tooltips and popovers utilize the `rounded-lg` (16px) setting to differentiate them from the structural grid. Buttons follow a standard 8px radius, unless they are icon-only utility buttons, which may be circular.

## Components

### Buttons & Inputs
Primary buttons use the Petroleum Blue gradient with white text. Secondary buttons utilize a Petroleum Blue outline on a transparent or Smoke White background. Input fields are Graphite Gray outlines (low opacity) that shift to Petroleum Blue on focus, with a 1px border.

### Cards
Cards are the primary container for data. They must feature a 12px corner radius and a subtle 1px border in a light Graphite Gray (`#E0E0E0`). The header section of a card should be separated by a thin horizontal rule or a subtle Warm Sand background tint.

### Neo4j Graph Nodes
Nodes are color-coded:
- **Entities:** Petroleum Blue.
- **Critical Alerts:** Vibrant Coral.
- **Secondary Assets:** Warm Sand with Graphite text.
Relationships (edges) should be Graphite Gray with Source Sans 3 labels for maximum clarity.

### Chips & Status Indicators
Status chips use a "Pill" shape (32px radius). Success states use a muted green (not in core palette, use sparingly), while the primary system status relies on Petroleum Blue (Neutral/Active) and Vibrant Coral (Attention Required).

### Lists & Tables
Tables utilize Source Sans 3 at 14px for high-density data. Rows alternate with a very subtle Smoke White and a faint Warm Sand tint to assist horizontal eye-tracking across long supply chain manifests.