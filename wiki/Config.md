# Config

To change default behaviour and setting:

```shell
# show current config
ezsub config show

# change config
ezsub config set OPTION VALUE


# short version
ezsub cfg ...
```

There is `user.conf` in cache directory. User can change this files manually (not recommended).

By using this command, user can alter the dafault setting for these `OPTION`s:

- `Defaults.open_after`
- `Defaults.auto_select`
- `Defaults.group`
- `Defaults.site`
- `Defaults.lngs`
- `Defaults.destination`
- `Update.remind_every`

Use `-` as `VALUE` to reset an `OPTION` to its default values.

Examples:

```shell
ezsub config set Defaults.site hastisub

# reset default destination
ezsub config set Defaults.destination -
```

[Back to Home](./ReadMe.md)
