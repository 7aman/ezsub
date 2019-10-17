# Install

## 1) Dependencies

### 1-1: python 3.7+

`ezsub` is written in python 3 language.  
Python is usually pre-installed in many linux distributions but it might be the deprecating version 2. In this case please install python 3.7+.  
In Windows you need to install [python 3.7+](https://www.python.org/downloads/windows).  

### 1-2: pip3

`ezsub` is provided as a package on [pypi](https://pypi.org/project/ezsub) and you can install it command tool named `pip`.  

In most Linux Distros `pip` has been installed with python itself and user have both pip (that points to pip2) and pip3 installed. In this case use `pip3` because there is no `ezsub` package for pip2.  

In Windows if you install python 3 from its official installer, you can select if you want to install pip too. After installing just use `pip` or `easy_install` command to install `ezsub` because there is no command named `pip3` in Windows.

### 1-3: unrar [optional]

Most of uploaded subtitles to subscene are compressed in zip format. Python has a built-in package named `zipfile` to handle zip files.

There is a small amount of subtitles that are compressed in rar format. For rar files `ezsub` depends on a third party package named [rarfile](https://pypi.org/project/rarfile/). `rarfile` itself depends on `unrar` executable which must exist in `PATH`. If you want to handle these files too, you need `unrar`.  

For most operating systems it can be downloaded from [unrar official site](https://www.rarlab.com/rar_add.htm).  

Also Linux users could install this tool from their official or unofficial repositories.  

Windows users must download this [self-extracting archive](https://www.rarlab.com/rar/unrarw32.exe). This file is not `unrar` executable but contains it. If you run this, it will ask a folder to extract `UnRar.exe` file. Point to a PATH directory such as `C:\Windows`.  

Notice: If ezsub could not find `unrar` executable in PATH, it will just ignore rar files and prints a warning message complaining about it.  

## 2) ezsub

And finally you ready to install `ezsub`:

- For latest published release using pip3

```shell
# Linux: run this command in terminal
python3 -m pip install --user --upgrade ezsub
#or
pip3 install --user --upgrade ezsub

# Windows: run this command in cmd or powershell
python -m pip install --upgrade ezsub
pip install --upgrade ezsub
```

And if you have `git` installed on your system, you can install "in-progress" version from github repository.

- Install latest "in-progress" version from github (not recommended):

```shell
# Linux and Mac: run this command in terminal
python3 -m pip install --user --upgrade https://github.com/7aman/ezsub/archive/master.zip

# Windows: run this command in cmd or powershell
python -m pip install --user --upgrade https://github.com/7aman/ezsub/archive/master.zip
```

[Back to Home](./ReadMe.md)
