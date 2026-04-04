#!/usr/bin/env python3
"""
Offline enrollment utility for speaker verification.

Builds a single normalized reference embedding from three or more WAV files by
averaging normalized WeSpeaker embeddings and re-normalizing the result.

Enrollment inputs may be individual WAV files, directories containing WAV
files, or a mix of both.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Sequence

import numpy as np
import torch
from wespeaker.cli.speaker import load_model


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a normalized speaker reference embedding from WAV files "
            "or directories of WAV files."
        )
    )
    parser.add_argument(
        "wav_inputs",
        nargs="+",
        help=(
            "Three or more enrollment WAV files for the same speaker, or one "
            "or more directories containing WAV files."
        ),
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output reference embedding path (.pt or .npy).",
    )
    parser.add_argument(
        "--model-name-or-path",
        default="english",
        help='WeSpeaker model name or path. Defaults to "english".',
    )
    args = parser.parse_args(argv)

    args.wav_paths = _resolve_wav_paths(args.wav_inputs)
    if len(args.wav_paths) < 3:
        parser.error("Provide at least 3 enrollment WAV files in total.")

    return args


def _resolve_wav_paths(input_paths: Sequence[str]) -> list[str]:
    wav_paths: list[str] = []

    for input_path in input_paths:
        resolved_path = os.path.abspath(os.path.expanduser(input_path))

        if os.path.isdir(resolved_path):
            directory_wavs = [
                os.path.join(resolved_path, name)
                for name in sorted(os.listdir(resolved_path))
                if os.path.isfile(os.path.join(resolved_path, name)) and
                os.path.splitext(name)[1].lower() == ".wav"
            ]
            if not directory_wavs:
                raise ValueError(
                    f"Enrollment directory does not contain any WAV files: {resolved_path}"
                )
            wav_paths.extend(directory_wavs)
            continue

        if not os.path.isfile(resolved_path):
            raise FileNotFoundError(resolved_path)
        if os.path.splitext(resolved_path)[1].lower() != ".wav":
            raise ValueError(
                "Enrollment input must be a WAV file or directory containing WAV files: "
                f"{resolved_path}"
            )
        wav_paths.append(resolved_path)

    return wav_paths


def _normalize_embedding(raw_embedding, label: str) -> torch.Tensor:
    if isinstance(raw_embedding, dict):
        for key in ("embedding", "reference_embedding", "embeddings"):
            if key in raw_embedding:
                return _normalize_embedding(raw_embedding[key], label)
        if len(raw_embedding) == 1:
            return _normalize_embedding(next(iter(raw_embedding.values())), label)
        raise ValueError(f"{label} did not contain a recognizable embedding tensor")

    if isinstance(raw_embedding, torch.Tensor):
        tensor = raw_embedding.detach().cpu().to(dtype=torch.float32).flatten()
    elif isinstance(raw_embedding, np.ndarray):
        tensor = torch.from_numpy(np.asarray(raw_embedding, dtype=np.float32)).flatten()
    elif isinstance(raw_embedding, (list, tuple)):
        tensor = torch.tensor(raw_embedding, dtype=torch.float32).flatten()
    else:
        raise TypeError(f"unsupported embedding type: {type(raw_embedding).__name__}")

    if tensor.numel() == 0:
        raise ValueError(f"{label} is empty")
    if not torch.isfinite(tensor).all():
        raise ValueError(f"{label} contains non-finite values")

    norm = float(torch.norm(tensor).item())
    if norm <= 1e-12:
        raise ValueError(f"{label} has near-zero norm")

    return tensor / norm


def _save_embedding(path: str, embedding: torch.Tensor) -> str:
    resolved_path = os.path.abspath(os.path.expanduser(path))
    output_dir = os.path.dirname(resolved_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    suffix = os.path.splitext(resolved_path)[1].lower()
    if suffix == ".pt":
        torch.save(embedding.detach().cpu(), resolved_path)
    elif suffix == ".npy":
        np.save(resolved_path, embedding.detach().cpu().numpy())
    else:
        raise ValueError("Output path must end in .pt or .npy")

    return resolved_path


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)

    wav_paths = list(args.wav_paths)

    speaker = load_model(str(args.model_name_or_path).strip() or "english")

    normalized_embeddings: list[torch.Tensor] = []
    for wav_path in wav_paths:
        embedding = speaker.extract_embedding(wav_path)
        if embedding is None:
            raise RuntimeError(f"WeSpeaker returned no embedding for {wav_path}")
        normalized_embeddings.append(_normalize_embedding(embedding, wav_path))

    reference_embedding = _normalize_embedding(
        torch.stack(normalized_embeddings, dim=0).mean(dim=0),
        "averaged reference embedding",
    )
    saved_path = _save_embedding(args.output, reference_embedding)

    print(saved_path)
    print(tuple(reference_embedding.shape))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
