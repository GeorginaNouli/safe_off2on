#!/usr/bin/env bash

CONDA_DIR="$PWD/miniconda3"
MUJOCO_DIR="$PWD/.mujoco"

if [ ! -d "$CONDA_DIR" ]; then
    mkdir -p "$CONDA_DIR"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -O "$CONDA_DIR/miniconda.sh"
    bash "$CONDA_DIR/miniconda.sh" -b -u -p "$CONDA_DIR"
    rm "$CONDA_DIR/miniconda.sh"

    # use the just-installed conda
    "$CONDA_DIR/bin/conda" env create -f environment.yml
    source "miniconda3/etc/profile.d/conda.sh"

fi

if [ ! -d "$MUJOCO_DIR/mujoco210" ]; then
    mkdir -p "$MUJOCO_DIR"
    wget https://github.com/deepmind/mujoco/releases/download/2.1.0/mujoco210-linux-x86_64.tar.gz \
        -O "$MUJOCO_DIR/mujoco210.tar.gz"
    tar -xzf "$MUJOCO_DIR/mujoco210.tar.gz" -C "$MUJOCO_DIR"
    rm "$MUJOCO_DIR/mujoco210.tar.gz"
fi

sudo apt install libglew-dev
unzip models.zip
