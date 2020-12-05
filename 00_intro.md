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

> It's unfortunate that installation of everything you need isn't a one-click process... although [FPGAWars' Apio](http://fpgawars.github.io/) goes a long way towards doing this. I just think that while yosys and nMigen are undergoing constant positive updates, Apio doesn't keep up with them. In the meantime, we just install all the tools separately.

Also, if you're using Windows, I hope you're using Windows Subsystem for Linux. If not, you're on your own.

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
