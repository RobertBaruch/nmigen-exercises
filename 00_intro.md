# What's this?

This is a series of graded exercises in using nMigen, the Python-based Hardware Design Language, to design and verify digital circuits!

It's also a work in progress.

Please note, the goal is not to be pedantically correct in every explanation. As you progress through the exercises, you'll learn for yourself the breadth of nMigen and what you can do with it!

## Prerequisite knowledge

You will need knowledge of:

* Basic digital electronics (do you know what an AND gate is? A flip-flop?)
* Basic Python 3 (do you know how to write a class?)
* How to run things on the command-line (do you know how to use command-line options? What a PATH is?)

## Software prerequisites

If you're using Windows, I hope you're using Windows Subsystem for Linux. If not, you're on your own.

### Option 1: Docker (recommended)

Victor Muñoz has put together a [docker container](https://github.com/vmunoz82/eda_tools) that has everything you need: Python 3, nMigen, yosys, SymbiYosys, and the Z3, boolector, and yices solvers.

You'll need to get [Docker Desktop](https://www.docker.com/get-started). If you're on Windows, follow the instructions for [Docker/WSL](https://docs.docker.com/docker-for-windows/wsl/) instead.

Also, if you're on Windows, you will want to download and run an [X server](https://medium.com/@japheth.yates/the-complete-wsl2-gui-setup-2582828f4577) so that you can use gtkwave from the command line on WSL.

Once you've done that, you can open up WSL (if you're on Windows) and then run [`eda_tools.sh`](https://raw.githubusercontent.com/vmunoz82/eda_tools/main/eda_tools.sh). This will conveniently start up the docker container with all the right options. 

You may want to replace `-v $HOME:/$HOME` in `eda_tools.sh` with `-v /your/host/working/directory:/some/nice/directory/on/docker`, and then you can access your files in `/some/nice/directory/on/docker` in the docker container. For example, I do my work in WSL in `/mnt/f` so I simply use `-v /mnt/f:/mnt/f`.

Remember that the docker container will not save local files (e.g. files in `/workspace`), so make sure you have your working directory mapped!

### Option 2: Build it all yourself

You will need:

* Python 3.8 or above: See below for Python 3.8 on WSL.

* Install yosys, Symbiyosys, yices2, and z3.
  * `sudo apt install curl`
  * Now follow the [instructions to install these](https://symbiyosys.readthedocs.io/en/latest/install.html). It is highly recommended to follow those instructions, especially for yosys since the git repo has many more fixes than the official release.
  * Note that when you see `-j$(nproc)`, it means to specify the number of processors your CPU has. You can't really go wrong by using `-j4`. You can go higher if you know you have more.
  * z3 takes a long time to compile. Go watch a YouTube video in the meantime.

* Install nMigen
  * `pip3 install wheel`
  * `pip3 install git+https://github.com/nmigen/nmigen`

* Signal viewer for simulation and formal verification
  * [gtkwave](https://sourceforge.net/projects/gtkwave/)
    * For WSL, get the Windows version unless you want to run an [X server](https://medium.com/@japheth.yates/the-complete-wsl2-gui-setup-2582828f4577).
    * The package for gtkwave for Windows gives you no clue how to install for Windows. Unzip the zip file into, say, C:, and then add C:\gtkwave\bin to your Windows path.

## Python and WSL

Python 2 and Python 3 are not compatible. This is why this happens:

* `python`, `pip` -> Python 2
* `python3`, `pip3` -> Python 3

On my freshly-installed WSL, the only version present is Python 3.8. If it is not on your version, you will want to upgrade to 3.8. Upgrading is beyond the scope of this document.

Now install some bare minimum tools:

```sh
sudo apt install python3-pip build-essential libssl-dev libffi-dev
```

In installing the yosys prerequisites, Python 2 will be installed. So be aware that when you want to run anything under Python 3, you must use `python3` (or `pip3` for installing), not `python` (or `pip`).

# Tip for vscode users:

Open File > Preferences > Settings, look for pylint args, and add:

```
--contextmanager-decorators=contextlib.contextmanager,nmigen.hdl.dsl._guardedcontextmanager
```

This is because pylint doesn't recognize that `nmigen.hdl.dsl._guardedcontextmanager` is a valid context manager. Otherwise pylint will complain for every `with m.If` statement.
