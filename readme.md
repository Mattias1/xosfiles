Cross OS files
===============
Some scripts to automatically copy (config) files to the right places, so that I can put them in one repo and deploy
them easily.

Config
-------
An example of a config that recursively copies everything (except directories starting with 'append-') from the
dotfiles' home directory to my real home directory.
This config file should be in the parent directory of this repo. The assumption is that the scripts are called from that
directory as well (`cd parent_dir && xosfiles/src/main.py --setup windows`).

_mapping-windows.json_
```
{
    "dotfiles-dir": "~/Documents/dotfiles/",
    "append-prefix": "append-",
    "copies": [
        [ "home/", "~/" ]
    ]
}
```
