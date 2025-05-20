{ pkgs ? import <nixpkgs> {} }:

let

  src = ./.;

  vosk =
    pkgs.python3.pkgs.buildPythonPackage rec {
      pname = "vosk";
      version = "0.3.45";
      format = "wheel";
      src = pkgs.fetchurl {
        url = "https://github.com/alphacep/vosk-api/releases/download/v${version}/vosk-${version}-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl";
        sha256 = "sha256-JeAlCTxDmdcnj1Q1aO2MxUYKw6S/SMI2c6zh4l0mYZ8=";
      };
    };

  python =
    pkgs.python3.withPackages (ps: [
      ps.pasimple
      ps.srt
      ps.requests
      ps.cffi
      ps.tqdm
      vosk
    ]);

  ld-library-path =
    pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.libpulseaudio
    ];

in

  pkgs.writeShellApplication {
    name = "transcribe";
    runtimeInputs = [
      python
    ];
    text = ''
      export LD_LIBRARY_PATH="${ld-library-path}"
      ${src}/transcribe.py "$@"
    '';
  }
