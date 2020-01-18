* get Anaconda Python 3.7 version from https://www.anaconda.com/distribution/#download-section
* install it by running the .sh as a regular user, preferably into your home directory:
  * `cd ~`
    * `sh Downloads/Anaconda3-2019.10-Linux-x86_64.sh`
  * use anaconda's package manager (`conda`) to make a python3.6 environment, and get `conda` to install `pyqt` and `wxpython` rather 
  than get `pip` to do it. (It seems you need to have `wxpython` and `pyqt` both installed, even though only `pyqt` will get used by psychopy).
    * `conda activate base` 
    * `conda create -n mypsychopy python=3.6 wxpython` 
    * `conda activate mypsychopy`
  * Although this might have been fixed since the time of writing, the version of pyglet (a windowing system) that 
  comes with psychopy (1.4.9 as I write on Jan 18th 2020) doesn't work, and causes major problems with the visual 
  presentation side of things, to the point of crashing the experiment when it starts up. The solution is to roll 
  back to a specific earlier version. That's what the "pyglet==1.3.2" part of the next line does.
    * `pip install psychopy pyglet==1.3.2`
