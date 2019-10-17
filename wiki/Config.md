# Config

```shell
ezsub config {set|show}
ezsub config set OPTION VALUE
```

set default values for `open_after`, `auto_select`, `group`, `site`, `languages` and `destination`. It reads and writes to `ROOT/user.conf` file.  
Use `-` as VALUE to reset an OPTION to its default values.

```shell
ezsub config set  Defaults.site hastisub
ezsub config set Defaults.destination -
```

[Back to Home](./ReadMe.md)
