# Clean

To remove or reduce size of subtitles from cache folder:

```shell
ezsub clean -t|-T TITLE -l LNG1 [LNG2 ...] [-0] -a|-A
ezsub clean --all -l LNG1 [LNG2 ...] [-0] -a|-A
```

It searches cache directory for given title and language. then:

* with `-0` or `--zero` it will replace each downloaded files with empty zip files.
* without `-0` it will delete downloaded files completely.

`--zero` option is useful for future downloadig request for the same titles. `ezsub` is depending on cache folder to determine if a subtitle is new or downloaded before. `ezsub` will not check size of the file for this decision.  

`--all` switch means all subtitles.  

If `-l *` is used it means all available languages.  

[Back to Home](./ReadMe.md)
