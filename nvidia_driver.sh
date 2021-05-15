#!/bin/bash

# ==============INSTRUCTIONS==============
# run the following commands:
# 1. chmod +x nvidia_driver.sh
# 2. ./nvidia_driver.sh
# ========================================

# Looking for latest drivers
echo "Looking for the latest release of nvidia-driver";
# replace the regex with "^nvidia-(driver-)?[0-9]+\s" if it doesn't work
ver=($(apt-cache search nvidia | grep -P "^nvidia-driver-[0-9]{3}\s-\s(NVIDIA driver metapackage)" | grep -Po "[0-9]{3}"));
latver=${ver[-1]};

if ! nvidia-smi 2>&1 >/dev/null; 
    then
        echo "NVIDIA Driver not found. Installing latest driver (nvidia-driver-$latver)";
        read -p "Press Enter to continue" </dev/tty
        sudo apt-add-repository ppa:graphics-drivers/ppa;
        sudo apt-get install nvidia-driver-$latver;
    else
        # looking for installed version
        version=($(nvidia-smi | grep -Po 'Driver Version: \K([0-9]{3})'));
        echo "NVIDIA Driver (version ${version}) found. Proceeding to uninstall and (re)install latest version (nvidia-driver-$latver).";
        read -r -p "Are you sure? [y/N] " response
        
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
            # Uninstalling
            sudo apt-get autoremove nvidia-*;
            # standard stuff
            sudo apt-get update;
            #  installing latest driver
            sudo apt-get install nvidia-driver-$latver;
        else
            exit 1
        fi
fi




