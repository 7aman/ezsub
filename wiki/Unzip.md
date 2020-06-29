
# unzip

To extract previously downloaded subtitles from cache folder:

```shell
ezsub unzip -t|-T Title of Movie or TV Series -l LNG1 [LNG2 ...] -d DESTINATION -a|-A -o|-O -g|-G

# x and ex are short version
ezsub x -t ...
exsub ex -t ...
```

Procedure is like what happens in [download](./Download.md)

## Switches

- `-t` is title to search. It is required.  
Also if user knows exact title used in url page, user could give this title by `-T` switch.  
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

- `-d` determines `DESTINATION` folder which downloaded subtitles will be extracted to. If folder does not exist, it will be created with its parents. It supports `.` as current working directory and also relative paths to current working directory.  
Default: `%USER-DOWNLOADS-FOLDER%/ezsub`  
Examples:
  - `-d .` # extract to current working directory
  - `-d sub` # make a folder, named "sub", in current working directory and extract files to this folder

- `-o` or `-O` determines if `ezsub` must open the folder that subtitles are extracted into.  
Default: True (Open)
  - `-o` for open the folder
  - `-O` for do nothing

- `-a` or `-A` determines if `ezsub` must automatically select best match (first result) from search results.  
Default: False (Ask)
  - `-a` for auto select
  - `-A` for ask user

- `-g` or `-G` determines if `ezsub` must make folders for each title and language in `DESTINATION` folder. It is helpful when user chooses multiple title to download.  
Default: True (make `TITLE/LANGUAGE/` folders)
  - `-g` for make group
  - `-G` for do nothing

[Back to Home](./ReadMe.md)
