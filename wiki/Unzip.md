
# unzip

To extract previously downloaded subtitles use this command:

```shell
ezsub unzip -t Title of Movie or TV Series -l LNG1 [LNG2 ...] -d DESTINATION -a|-A -o|-O -g|-G
```

Procedure is like [download](./Download.md)

## Switches

- `-t` is title to search. It is required.  
Examples:
  - `-t riverdale`
  - `-t riverdale first season`
  - `-t godfather`

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

[Back to Home](./ReadMe.md)
