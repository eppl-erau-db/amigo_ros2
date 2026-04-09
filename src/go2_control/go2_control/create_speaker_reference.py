#!/usr/bin/env python3
"""
Enrollment utility for speaker verification.

Extracts WeSpeaker embeddings from WAV files, averages them, L2-normalizes,
and saves the result as a .npy reference embedding.

Usage:
    python3 create_speaker_reference.py --output ref.npy clip1.wav clip2.wav clip3.wav
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import torch
import torchaudio


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a speaker reference embedding from WAV files."
    )
    parser.add_argument(
        "wav_files",
        nargs="+",
        help="Paths to WAV files recorded from the target speaker (at least 3 recommended).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="speaker_reference.npy",
        help="Output path for the .npy embedding file (default: speaker_reference.npy).",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="english",
        help='WeSpeaker model name or path (default: "english").',
    )
    args = parser.parse_args()

    if len(args.wav_files) < 3:
        print(
            f"WARNING: Only {len(args.wav_files)} WAV file(s) provided. "
            "3 or more clips are recommended for a robust reference.",
            file=sys.stderr,
        )

    # Validate input files exist
    for wav_path in args.wav_files:
        if not Path(wav_path).is_file():
            print(f"ERROR: File not found: {wav_path}", file=sys.stderr)
            return 1

    # Load WeSpeaker model
    try:
        from wespeaker.cli.speaker import load_model
    except ImportError:
        print(
            "ERROR: wespeaker is not installed. "
            "Install with: pip3 install wespeaker",
            file=sys.stderr,
        )
        return 1

    print(f'Loading WeSpeaker model: "{args.model}" ...')
    model = load_model(args.model)

    embeddings: list[np.ndarray] = []
    for wav_path in args.wav_files:
        print(f"  Extracting embedding from: {wav_path}")
        try:
            # Load WAV and convert to float32 PCM, matching the live verifier path
            waveform, sr = torchaudio.load(wav_path)
            if sr != 16000:
                waveform = torchaudio.functional.resample(waveform, sr, 16000)
                sr = 16000
            # Mix to mono if multi-channel
            if waveform.shape[0] > 1:
                waveform = waveform.mean(dim=0, keepdim=True)
            # Use extract_embedding_from_pcm — same method as the live verifier
            emb = model.extract_embedding_from_pcm(waveform, sample_rate=sr)
            if isinstance(emb, torch.Tensor):
                emb = emb.detach().cpu().numpy()
            emb = np.array(emb, dtype=np.float32).flatten()
            norm = np.linalg.norm(emb)
            if norm < 1e-8:
                print(f"  WARNING: Near-zero embedding for {wav_path}, skipping.")
                continue
            emb = emb / norm
            embeddings.append(emb)
        except Exception as exc:
            print(f"  ERROR extracting from {wav_path}: {exc}", file=sys.stderr)
            continue

    if not embeddings:
        print("ERROR: No valid embeddings extracted. Cannot create reference.", file=sys.stderr)
        return 1

    # Average and re-normalize
    avg = np.mean(np.stack(embeddings), axis=0).astype(np.float32)
    avg_norm = np.linalg.norm(avg)
    if avg_norm < 1e-8:
        print("ERROR: Averaged embedding has near-zero norm.", file=sys.stderr)
        return 1
    reference = avg / avg_norm

    # Save
    output_path = Path(args.output)
    np.save(str(output_path), reference)
    print(f"\nSaved reference embedding:")
    print(f"  Path:  {output_path.resolve()}")
    print(f"  Shape: {reference.shape}")
    print(f"  Norm:  {np.linalg.norm(reference):.6f}")
    print(f"  From {len(embeddings)} clip(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
