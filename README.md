# ezsub

[![Downloads](https://img.shields.io/pypi/dw/ezsub.svg)](https://pypi.org/project/ezsub/)
[![Published Version](https://img.shields.io/pypi/v/ezsub.svg)](https://pypi.org/project/ezsub/)
![GitHub Release](https://img.shields.io/github/release/7aman/ezsub.svg?label=repo%20version)
[![License: MIT](https://img.shields.io/github/license/7aman/ezsub.svg)](https://github.com/7aman/ezsub/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/7aman/ezsub.svg?branch=master)](https://travis-ci.org/7aman/ezsub)

`ezsub` downloads subtitles from [subscene.com](https://subscene.com/) and its persian clones
such as [subf2m.co](https://subf2m.co/).  
For more details see [How ezsub Works](./wiki/How-ezsub-Works.md).

<hr/>

## Table of Contents

* [Install](#install)
* [How to use](#how-to-use)
  * [Download: `ezsub dl`](#download)
  * [Extract Previously Downloaded Subtitles: `ezsub unzip`](#extract-previously-downloaded-subtitles)
  * [Login: `ezsub login`](#login)
  * [Info: `ezsub info`](#info)
  * [Config: `ezsub config`](#config)
  * [Clean: `ezsub clean`](#Clean)
  * [Update: `ezsub update`](#Update)
  * [Backup: `ezsub backup`](#Backup)
* [Report Errors](#report-errors)

<hr/>

## Install

Dependencies:

* python3.7+
* unrar [optional]

Install latest published release using pip3

```shell
# linux and mac
python3 -m pip install --user --upgrade ezsub

# windows
python -m pip install --user --upgrade ezsub
```

For installing latest in progress version from github (not recommended) use this command:

```shell
python3 -m pip install --user --upgrade https://github.com/7aman/ezsub/archive/master.zip

# windows
python -m pip install --user --upgrade https://github.com/7aman/ezsub/archive/master.zip
```

See [here](./wiki/Install.md) for more details.

<hr/>

## How to Use

### Download

```shell
ezsub dl -t|-T TITLE -l LNG1 [LANG2 ...] -d DESTINATION -s SITE1 [SITE2 ...] -a|-A -o|-O -S -g|G
```

For details on each switch see [this](./wiki/Download.md#Switches)

Examples:

```shell
# if search keywords are distinctive enough, use auto select (-a)
ezsub dl -t riverdale third season -l fa -a

# determine site. If site is not responding, ezsub will choose first responding site automatically.
ezsub dl -t game of thrones -s subscene

# movies, tv series, video musics are not different.
ezsub dl -t how to train your dragon

# if you know exact title used in url use this -T
# for example subscene page for first season of "the end of the f***ing world" is:
# https://subscene.com/subtitles/the-end-of-the-fing-world
#so:
ezsub dl -T the-end-of-the-fing-world

# extract here and relative to here (both windows and unix)
ezsub dl -t aquaman -d .
ezsub dl -t aquaman -d ./children/to/here
ezsub dl -t aquaman -d ../sibling/to/here

# absolute and relative path (unix)
ezsub dl -t aquaman -d /absolute/path/to/a/destination
ezsub dl -t aquaman -d ~/relative/path/to/home/directory

# absolute path (windows)
ezsub dl -t aquaman -d 'D:\Movies\Aquaman\'
```

### Extract Previously Downloaded Subtitles

```shell
ezsub unzip -t|-T Title of Movie or TV Series -l LNG1 [LNG2 ...] -d DESTINATION -a|-A -o|-O -g|-G
```

switches are same as `ezsub dl` [switches](#download) except there is no `-s` and `-S`. `ezsub` searches through `"cache"` folder. Rest is same as the download process.

[More Details](./wiki/Unzip.md)

### Login

Since June 2019, subscene added google re-captcha. If user logs in, this captcha will not be required anymore.  
At now (October 2019) it is easy to get a token even without user and password. Also persian mirrors such as 'hastisub' and 'subf2m' do not require login.

### Info

```shell
ezsub info
ezsub info -v {-t|-s|-n}
```

prints some useful information such as version and cache folder details.  
With `-v` lists all downloaded titles with size and number of files sorted by title (`-t`). for sorting based on size (s) and number of files (n) use `-s` and `-n`.

### Config

```shell
ezsub config show
ezsub config set OPTION VALUE
```

command to show or change default values.

[More Details](./wiki/Config.md)

```shell
ezsub config set Defaults.site hastisub
# to reset to default
ezsub config set Defaults.languages -
```

### Clean

```shell
ezsub clean -t|-T TITLE -l LNG1 [LNG2 ...] [-0] -a|-A
```

searches cache directory for given title and language. then:

* with `-0` or `--zero` it will replace each downloaded files with empty zip files.
* without `-0` it will delete downloaded files completely.

### Update

```shell
ezsub update
```

Check if there is a new version of ezsub available. If user confirms, new version will be installed.  
Also if last check was before 7 days ago, at next call it warns user to check for update.

### Backup

Create a zip archive from cache folder. It accepts `-d` option for destination and `-o|-O` for opening destination folder after backup is completed.

<hr/>

## Report Errors

`ezsub` logs some messages that could be found in `ROOT/ezsub.log` file.  
If you getting error, you can run each `ezsub` command with `--loglevel=Debug` switch. Get `ezsub.log` content and create an issue [here](https://github.com/7aman/ezsub/issues) to report.
