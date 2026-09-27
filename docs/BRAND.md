# Media Transcoder Brand Guide

## Identity idea

The visual system is called **Signal Flow**. It treats transcoding as a visible path from source signal to transformed output: frames, waveform segments, directional motion, and a compact conversion mark.

The identity is intentionally technical rather than cinematic. Media Transcoder is a CLI utility, so the artwork suggests a controlled processing pipeline instead of implying a desktop editor or streaming platform.

## Palette

| Role | Color | Hex |
|---|---|---|
| Carbon | Deep background | `#0A0A0C` |
| Graphite | Panels / secondary surfaces | `#17181C` |
| Signal Lime | Primary action / input signal | `#C6FF33` |
| Ultraviolet | Conversion / transform accent | `#9B5CFF` |
| Soft White | Primary text | `#F4F7F5` |
| Muted Silver | Secondary text | `#A7ADB5` |

## Project logo

`assets/project-logo.svg` is the primary square mark.

The symbol combines:

- a media frame boundary;
- directional conversion chevrons;
- a central signal/play geometry;
- a short waveform reference.

Use it on dark or neutral backgrounds with enough clear space around the outer frame. Avoid stretching, recoloring individual components, adding shadows, or placing the mark on visually noisy imagery.

## Hero cover

`assets/project-cover.svg` is the repository hero artwork. It contains the project name, concise positioning, author attribution, and an abstract input → process → output media pipeline.

Use the full cover at the top of repository documentation. Do not crop it into a square logo; the project logo is designed for that purpose.

## Typography

The SVG assets use system-safe sans-serif families so they render without bundled font files. Documentation should prefer GitHub's native typography and monospace code blocks for commands.

## Visual character

- technical;
- local-first;
- precise;
- high-contrast;
- motion-aware without animation;
- minimal enough for a developer tool.

## Distinction

This identity is built around **signal routing and transcoding** rather than document scanning, OCR motifs, generic terminal windows, or blue/coral product styling. The lime/ultraviolet palette, segmented pipeline geometry, and abstract conversion symbol are specific to Media Transcoder's job: transforming local media through a visible FFmpeg workflow.

## Author lockup

Use the Arabic name **رضوان عبدالهادي** when an Arabic signature is appropriate and **Radwan Abd alhady Ahmed** in English metadata or documentation. The author line should remain secondary to the product name.
