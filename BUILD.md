Monophony can be manually built and installed as a Flatpak for testing purposes.

1. [Set up](https://flathub.org/setup) Flatpak
2. Install [`flatpak-builder`](https://repology.org/project/flatpak-builder/versions) using your distro's package manager
3. Enter the [`source/`](https://gitlab.com/zehkira/monophony/-/tree/master/source) directory
4. Run `make flatpak`

Note that this will automatically add the Flathub repository as a remote and install dependencies from there. See [`source/Makefile`](https://gitlab.com/zehkira/monophony/-/blob/master/source/Makefile) for details.

Once you are done testing, uninstall the app using your system app store or by running `flatpak uninstall -y io.gitlab.zehkira.Monophony` and then reinstall it the normal way so that you can continue receiving updates.
