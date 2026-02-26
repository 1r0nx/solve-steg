# StegSolve-like (Python)

A small Python tool that reproduces many features of **StegSolve** on Linux.  
It generates multiple image transformations useful for **steganography analysis** and **CTF challenges**.

The tool extracts bit planes, color channels, XOR combinations, LSB data, and other useful visualizations.

---

# Features

## Bit Planes

Extracts every bit of each channel:

- Red bit 0 → bit 7
- Green bit 0 → bit 7
- Blue bit 0 → bit 7
- Alpha bit 0 → bit 7

Useful to reveal hidden data embedded in specific bits.

---

## Full Color Channels

Equivalent to StegSolve “Full Red / Green / Blue / Alpha”.

Generates:

- full_R.png
- full_G.png
- full_B.png
- full_A.png

Each image isolates a single channel.

---

## LSB Extraction

Extracts the Least Significant Bit of RGB channels.

Files generated:

- R_LSB.png
- G_LSB.png
- B_LSB.png

Very useful for detecting LSB steganography.

---

## XOR Channel Analysis

Generates XOR combinations between channels:

- xor_R_G.png
- xor_R_B.png
- xor_G_B.png

This can reveal hidden patterns that only appear when channels interact.

---

## Image Inversion

Creates a negative of the image:

    inverted.png

Sometimes hidden information becomes visible after inversion.

---

## Inverted Alpha Bit Planes

Alpha channel bit planes but inverted:

    alpha_bit0_inv.png
    alpha_bit1_inv.png
    ...
    alpha_bit7_inv.png

---

# Installation

## Requirements

    python3
    numpy
    pillow

Install dependencies:

    `git clone <this repo>`
    pip install -r req.txt

---

# Usage

Basic usage:

With -o options not specified, it will create a directory `_planes`

    python3 solve-steg.py image.png 


 You can copy in /usr/bin and run it like a normal command
	`solve-steg.py imag.png` 

Specify output directory:

    solve-steg.py image.png -o results

There a two files to test in the `test` directory

---

# Output

All generated images are saved in the output directory.

Example structure:

    _planes/
    │
    ├── R_bit0.png
    ├── R_bit1.png
    ├── ...
    ├── G_bit0.png
    ├── B_bit0.png
    ├── A_bit0.png
    │
    ├── full_R.png
    ├── full_G.png
    ├── full_B.png
    ├── full_A.png
    │
    ├── R_LSB.png
    ├── G_LSB.png
    ├── B_LSB.png
    │
    ├── xor_R_G.png
    ├── xor_R_B.png
    ├── xor_G_B.png
    │
    ├── inverted.png
    │
    └── alpha_bit*_inv.png

---

# Safety

The tool does not overwrite existing directories unless explicitly allowed.

This prevents accidental loss of analysis data.

---

# Use Cases

- CTF challenges
- Steganography analysis
- Hidden QR codes
- Hidden messages in bit planes
- Image forensic analysis

---

# Example (CTF workflow)

Typical workflow:

    1. Run the tool
    2. Browse generated images quickly
    3. Look for anomalies
    4. Combine results
    5. Decode hidden data

---
# Comparison with StegSolve

| Feature        | This Tool | StegSolve |
| -------------- | --------- | --------- |
| Bit planes     | ✓         | ✓         |
| Full channels  | ✓         | ✓         |
| XOR analysis   | ✓         | ✓         |
| LSB extraction | ✓         | ✓         |
| CLI automation | ✓         | ✗         |
| Linux native   | ✓         | Partial   |

---

# License

MIT License