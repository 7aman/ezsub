# Download

```shell
ezsub dl -t|-T TITLE | -l LNG1 [LANG2 ...] -d DESTINATION -s SITE1 [SITE2 ...] -a|-A -o|-O -g|G -S
```

## Workflow

- Search `TITLE` through `SITE`.
- Asks user (`-A`) to choose the best matches or selects automatically (`-a`) the first one.
  - Comma separated numbers are valid as answer to download multiple titles at once.
- Apply language filter based on (`LANG1`, `LANG2`, ...).
- Ignore previously downloaded subtitles (stored in `ROOT/subtitles` directory).
- Download remained links and save them in the `ROOT/subtitles` directory.
  - If `--simulation` or `-S` is given then do not download and just make empty zip files for each new subtitle.
- Extract new subtitles to `DESTINATION` directory.
  - If `-g` is given then make directories in `DESTINATION`, based on title and language to extract subtitles to corresponding directories.
  - To help find subtitles easily, name of language is appended to the name of the extracted subtitles.
  - To avoid replacing subtitles in `DESTINATION`, existing one is renamed.
  - Check for duplicates subtitles in `DESTINATION` folder. It compares content of the file using their hash. Name does not matter.
- If `-o` is given then open `DESTINATION`

## Switches

- `-t` is title to search. It is required.  
Also if user knows exact title used in url page, user could give this title by `-T` switch. For example subscene page for first season of *"the end of the f***ing world"* is `https://subscene.com/subtitles/the-end-of-the-fing-world`, so exact title is `the-end-of-the-fing-world`.  
Only one of `-t` and `-T` is allowed.  
Examples:
  - `-t riverdale`
  - `-t riverdale first season`
  - `-t godfather`
  - `-T the-end-of-the-fing-world`

- `-l` is/are "space separated" language(s) that user interested in. It uses abbr.  
Default: `en`  
Examples:
  - `-l en fa it`
  - `-l ar en`
  - `-l en`

- `-d` is determines `DESTINATION` folder which downloaded subtitles will be extracted to. If folder is not exist, it will be created with its parents. It supports `.` as current working directory and also relative paths to current working directory.  
Default: `%USER-DOWNLOADS-FOLDER%/ezsub`  
Examples:
  - `-d .` # extract to current working directory
  - `-d sub` # make a folder in current working directory names "sub" and extract files to this folder

- `-s` is site name, not full url, to search through. Value can be space separated site names in preferred order.  
Default: `subscene`  
Other options:
  - `-s subf2m`
  - `-s hastisub`
  - `-s xyz`

- `-o` or `-O` determines if `ezsub` must open the folder that subtitles are extracted into.  
Default: True (Open)
  - `-o` for open the folder
  - `-O` for do nothing.

- `-a` or `-A` determines if `ezsub` must automatically select best match (first result) from search results.  
Default: False (Ask)
  - `-a` for auto select
  - `-A` for ask user

- `-g` or `-G` determines if `ezsub` must make folders for each title and language in `DESTINATION` folder. It is helpful when user chooses multiple title to download.  
Default: False (extract all in root folder)
  - `-g` for make group
  - `-G` for do nothing

- `-S` or `--simulation`: If you don't want to download all previously uploaded subs and just need to omit them on future download request, use this switch. It creates empty zip files, instead of downloading subtitles. Then later if you search for this title again it will ignore these files because it assumes these subtitles are already downloaded.  
Default: False (download)

## Change switches default values

These default values can be customized via `ezsub config` command. See [this wiki page](./Config.md) about config.

## Examples

```shell
# if search keywords are distinctive enough, use auto select (-a)
ezsub dl -t riverdale third season -l fa -a

# determine site. If site is not responding, ezsub will choose first responding site automatically.
ezsub dl -t game of thrones -s subscene

# movies, tv series, video musics are not different.
ezsub dl -t how to train your dragon

# extract to a custom folder
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

[Back to Home](./ReadMe.md)
