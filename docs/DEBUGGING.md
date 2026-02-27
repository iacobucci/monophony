The following environment variables are available for debugging:
- `MONOPHONY_DEBUG`: Print memory information to help with finding leaks (unset by default)
- `MONOPHONY_LOG_LEVELS`: Only print log messages of specified levels (`Info,Warning,Error,Success` by default)

When running the app, environment variables can be set with `--env`:

```sh
flatpak run --env=MONOPHONY_LOG_LEVELS=Warning,Error io.gitlab.zehkira.Monophony
```
