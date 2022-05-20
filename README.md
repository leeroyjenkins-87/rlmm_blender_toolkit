# rlmm_blender_toolkit

A set of tools to streamline level generation in UDK straight from Blender.

## Installation

1. Download [all files](https://github.com/leeroyjenkins-87/rlmm_blender_toolkit/archive/refs/heads/kismet.zip) as a zip (Code > Download zip).
1. Open blender (2.93 - LTS supported).
1. Navigate to (Edit > Preferences > Add-ons).
1. In the top right click "Install".
1. Select the Zip file.

## Usage

### Navigation

1. Make sure you are in "Object Mode".
1. Type "N" in viewport.
1. A panel will pop up on the right hand side of the view port.
1. Navigate to RLMM Toolkit.

<!-- What to do next ?? -->

## Kismet - Beta

> Remove when merging: [Current script](https://gist.github.com/ghostrider-05/f82ca429ae3d74a77f193da752697f45)

Open a new window for the `Kismet Sequence Editor` and create a new sequence.
Click on the `Add` button and your kismet nodes and when ready export the current sequence with the `Copy kismet` button.

### Object linking

Some fields will allow you to select an object in your Blender. You will first need to export your scene [as described above][#usage] and then the kismet scene will link the object with the latest export.
