#!/usr/bin/env python3

import argparse
import os
import sys
import numpy as np
from PIL import Image

def save_image(arr, path, description=""):
    """Save a float array (0..1) as PNG and print info"""
    arr_uint8 = (arr * 255).astype(np.uint8)
    img = Image.fromarray(arr_uint8)
    img.save(path)
    h, w = arr.shape[:2]
    print(f"    [+] Saved {description} -> {path} ({w}x{h})")

def extract_bitplanes(img, outdir):
    print("[*] Extracting 8 bitplanes per channel (R,G,B,A)\n")
    arr = np.array(img) / 255.0  # normalize 0..1
    channels = ['R', 'G', 'B', 'A']
    if arr.shape[2] == 3:
        arr = np.dstack([arr, np.ones((arr.shape[0], arr.shape[1]))])  # add alpha if missing
    for i, c in enumerate(channels):
        channel = arr[:, :, i]
        for bit in range(8):
            plane = np.floor(channel * 255 / (1 << bit)) % 2
            save_image(plane, os.path.join(outdir, f"{c}_bit{bit}.png"), f"{c} bitplane {bit}")
    print("\n")

def save_full_channels(img, outdir):
    print("[*] Generating full channels (Full Red, Green, Blue, Alpha)\n")
    arr = np.array(img.convert("RGBA")).astype(np.uint8)
    channels = ['R','G','B','A']
    for i, c in enumerate(channels):
        plane = np.zeros_like(arr)
        plane[:,:,i] = arr[:,:,i]
        plane[:,:,3] = arr[:,:,3]  # keep alpha
        save_image(plane/255.0, os.path.join(outdir,f"full_{c}.png"), f"Full {c}")
    print("\n")

def save_inverted(img, outdir):
    print("[*] Generating inverted image\n")
    arr = 1.0 - np.array(img) / 255.0
    save_image(arr, os.path.join(outdir,"inverted.png"), "Inverted Image")
    print("\n")

def save_LSB(img, outdir):
    print("[*] Extracting LSB of R,G,B channels\n")
    arr = np.array(img) / 255.0
    channels = ['R','G','B']
    if arr.shape[2] == 3:
        arr = np.dstack([arr, np.ones(arr.shape[:2])])
    for i, c in enumerate(channels):
        channel = arr[:,:,i]
        lsb = np.floor(channel*255) % 2
        save_image(lsb, os.path.join(outdir,f"{c}_LSB.png"), f"{c} LSB")
    print("\n")

def save_XOR(img, outdir):
    print("[*] Generating XOR between channels (R⊕G, R⊕B, G⊕B)\n")
    arr = np.array(img) / 255.0
    if arr.shape[2] == 3:
        arr = np.dstack([arr, np.ones(arr.shape[:2])])
    R = (np.floor(arr[:,:,0]*255) % 2).astype(np.uint8)
    G = (np.floor(arr[:,:,1]*255) % 2).astype(np.uint8)
    B = (np.floor(arr[:,:,2]*255) % 2).astype(np.uint8)
    save_image(R ^ G, os.path.join(outdir,"xor_R_G.png"), "XOR R⊕G")
    save_image(R ^ B, os.path.join(outdir,"xor_R_B.png"), "XOR R⊕B")
    save_image(G ^ B, os.path.join(outdir,"xor_G_B.png"), "XOR G⊕B")
    print("\n")
    
def save_alpha_inverted(img, outdir):
    print("[*] Generating inverted alpha bitplanes\n")
    arr = np.array(img) / 255.0
    if arr.shape[2] == 3:
        alpha = np.ones(arr.shape[:2])
    else:
        alpha = arr[:,:,3]
    for bit in range(8):
        plane = 1 - (np.floor(alpha*255/(1<<bit)) %2)
        save_image(plane, os.path.join(outdir,f"alpha_bit{bit}_inv.png"), f"Alpha bit {bit} inverted")
    print("\n")

def main():
    parser = argparse.ArgumentParser(
        description="StegSolve-like Python tool: generate bitplanes, full channels, LSB, XOR, inversions etc. in a directory",
        epilog="Example:\n  python stegsolve_like.py image.png -o output_dir"
    )
    parser.add_argument("image", help="Path to the input image (PNG, JPG, etc.)")
    parser.add_argument("-o","--outdir", default="_planes", help="Directory where generated images will be saved")
            
    args = parser.parse_args()
    
    if args.image is None:
        parser.print_help()
        sys.exit(0)

    
    # Check if output folder exists
    if os.path.exists(args.outdir):
        print(f"[!] Warning: Output directory '{args.outdir}' already exists.")
        sys.exit(0)
    else:
        os.makedirs(args.outdir)
        print(f"[*] Created output directory '{args.outdir}'")

    os.makedirs(args.outdir, exist_ok=True)
    img = Image.open(args.image).convert("RGBA")
    w,h = img.size
    print(f"[*] Loaded image: {args.image} ({w}x{h})\n")
    
    extract_bitplanes(img, args.outdir)
    save_full_channels(img, args.outdir)
    save_inverted(img, args.outdir)
    save_LSB(img, args.outdir)
    save_XOR(img, args.outdir)
    save_alpha_inverted(img, args.outdir)

    print(f"[*] All done! Generated images are in '{args.outdir}'")

if __name__ == "__main__":
    main()