{
  description = "A flake providing a dev shell for PyTorch with CUDA and CUDA development using NVCC.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux"; # Adjust if needed
      pkgs = import nixpkgs {
        system = system;
        config.allowUnfree = true;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          cudatoolkit
          cudaPackages.cudnn
          cudaPackages.cuda_cudart
          ruff
          tesseract
      ];

        nativeBuildInputs = with pkgs; [
          libsForQt5.wrapQtAppsHook
          makeWrapper
        ];

        shellHook = ''
          export CUDA_PATH=${pkgs.cudatoolkit}

          # Add necessary paths for dynamic linking
          export LD_LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath (with pkgs; [
              "/run/opengl-driver" # Needed to find libGL.so
              cudatoolkit
              cudaPackages.cudnn
              libGLU
              libGL
              glib
            ])
          }:$LD_LIBRARY_PATH

          # Set LIBRARY_PATH to help the linker find the CUDA static libraries
          export LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath [
              pkgs.cudatoolkit
            ]
          }:$LIBRARY_PATH

          export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
        '';
      };
    };
}
