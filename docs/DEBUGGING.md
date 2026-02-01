The following environment variables are available for debugging:
- `MONOPHONY_DEBUG`: Print memory information to help with finding leaks (unset by default)
- `MONOPHONY_LOG_LEVELS`: Only print log messages of specified levels (`INFO,WARN,ERRO,SUCC` by default)

When running the app, environment variables can be set with `--env`:

```sh
flatpak run --env=MONOPHONY_LOG_LEVELS=WARN,ERRO io.gitlab.zehkira.Monophony
```
