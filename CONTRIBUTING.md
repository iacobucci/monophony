## Editing code and other text files

Before making any changes, make sure that your editor supports [EditorConfig](https://editorconfig.org/).

## Debugging

The following environment variables are available:
- `MONOPHONY_DEBUG`: Print memory information to help with finding leaks (unset by default)
- `MONOPHONY_LOG_LEVELS`: Only print log messages of specified levels (`INFO,WARN,ERRO` by default)

When running the app, environment variables can be set with `--env`:

```sh
flatpak run --env=LOG_LEVELS=WARN,ERRO io.gitlab.zehkira.Monophony
```

## Translation

Standard translation files are located in `source/locales`. 
