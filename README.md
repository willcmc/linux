# Utilities
Bash scripts, python codes, etc to do smart stuff.

## Bash 

### Nvidia Ubuntu Driver Installer Shell
* [nvidia_driver.sh](https://github.com/willcmc/util/blob/main/nvidia_driver.sh)
    * Installs (or reinstalls or updates) your nvidia drivers.
    * For people like me, who are tired of reinstalling drivers every other month thanks to the umpteen issues.

## Python 

### WhatsApp Conversation Analysis
* [WA_An_Latest.py](https://github.com/willcmc/util/blob/main/WA_An_Latest.py)
    * Requires your exported text file from WhatsApp. Place it in the same directory as the script and run it via```python3 WA_An_Latest.py```. Enter the file name and your username as on WhatsApp.
    * This should generate a bar plot showing how much you and the other person in the conversation talked since the beginning of the exported conversation, on a daily basis.
    * This will not work for group conversations.

### [Python Gnuplot Data Animator](https://github.com/willcmc/util/tree/main/py-gnuplot-animate)
* [gen.py](https://github.com/willcmc/util/blob/main/py-gnuplot-animate/gen.py)
    * Generates gnuplot scripts for data stored under `./data/`.
    * Runs the scripts and generates the images for the plots.
    * Combines images into a video file.
