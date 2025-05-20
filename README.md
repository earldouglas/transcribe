## About

This is a CLI tool for lightweight real time offline transcription of
one or more audio sources.

## Installation

Use the Nix derivation in *default.nix*, e.g. by running `nix-build`:

```
$ nix-build
$ ./result/bin/transcribe
Usage: transcribe <source0> [source1] ... [sourceN]
```

## Usage

List available audio sources with `pactl`:

```
$ nix-shell -p pulseaudio --run 'pactl list short sources | cut -f2'
alsa_output.pci-0000_c3_00.6.HiFi__Speaker__sink.monitor
alsa_input.pci-0000_c3_00.6.HiFi__Mic2__source
alsa_input.pci-0000_c3_00.6.HiFi__Mic1__source
```

Run `transcribe` on one or more audio sources:

```
$ transcribe
Usage: transcribe <source0> [source1] ... [sourceN]
```

## Examples

Transcribe from one audio source:

```
$ transcribe alsa_input.pci-0000_c3_00.6.HiFi__Mic1__source
<ch0> see here i'm now by myself uh talking to myself
<ch0> that's chaos theory
^C
```

Transcribe from multiple audio sources:

```
$ transcribe \
  alsa_input.pci-0000_c3_00.6.HiFi__Mic1__source \
  alsa_output.pci-0000_c3_00.6.HiFi__Speaker__sink.monitor
<ch1> hey hey
<ch0> howdy
^C
```
