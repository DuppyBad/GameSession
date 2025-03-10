{
  description = "Python development environment with venv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    # List of supported systems
    # Surprisingly, it does actually compile on darwin, but we do not truly support MacOS
    supportedSystems = [
      "x86_64-linux"
      "aarch64-linux"
      "x86_64-darwin"
      "aarch64-darwin"
    ];

    # Function to create shell for a given system
    forSystem = system: let
      pkgs = nixpkgs.legacyPackages.${system};

      pythonPackage = pkgs.python312Full;
      venvDir = ".venv";
      requirementsFile = "requirements.txt";

      setupVenv = pkgs.writeScriptBin "setup-venv" ''
        #!${pkgs.bash}/bin/bash

        if [ ! -d "${venvDir}" ]; then
          echo "Creating new virtual environment..."
          ${pythonPackage}/bin/python -m venv ${venvDir}
        fi

        source ${venvDir}/bin/activate

        if [ -f "${requirementsFile}" ]; then
          echo "Installing requirements..."
          pip install -r ${requirementsFile}
        else
          echo "No ${requirementsFile} found."
        fi
      '';
    in
      # fish is optional, feel free to replace with shell of your choice
      pkgs.mkShell {
        buildInputs = with pkgs; [
          pythonPackage
          setupVenv
          python312Packages.pygame
        ];
        # shellHook runs in it's own scope, so even though the script is a bash script, the bash instance is terminated
        # almost a pure function...
        shellHook = ''
          echo "Python development environment"
           ${setupVenv}/bin/setup-venv
        '';
      };
  in {
    devShells = builtins.listToAttrs (
      map (system: {
        name = system;
        value = {
          default = forSystem system;
        };
      })
      supportedSystems
    );
  };
}
