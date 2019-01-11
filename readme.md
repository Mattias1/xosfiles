Cross OS files
===============
Some scripts to automatically copy (config) files to the right places, so that I can put them in one repo and deploy
them easily.


Basic config
-------------
An example of a config that recursively copies everything from the dotfiles' home directory to my real home directory.
This config file should be in the parent directory of this repo. The assumption is that the scripts are called from that
directory as well (`cd parent_dir && python3 xosfiles/src/main.py --setup windows`).

_mapping-windows.json_
```
{
    "dotfiles-dir": "~/Documents/dotfiles/",
    "copies": [
        [ "home/", "~/" ]
    ]
}
```


Advanced config
----------------
You can also use variables to tune your (config) files to each environment.
For example, like this:

_./home/.bash\_aliases_
```
alias dotfilescd="cd ${dotfilespath}"
alias setup="dotfilescd && cd setup && ./setup.sh"

${end}
```

_./mapping-windows.json_
```
{
    "dotfiles-dir": "~/Documents/dotfiles/",
    "substitute-prefix": "substitute-",
    "variable-prefix": "${",
    "variable-suffix": "}",
    "variable-assignment": "=",
    "multiline-open": "{",
    "multiline-close": "}",
    "copies": [
        [ "home/", "~/" ]
    ]
}
```

_./home/substitute-windows/.bash\_aliases_
```
dotfilespath = ~/Documents/dotfiles
end = {
alias game1="C:/Program\ Files\ \(x86\)/studio1/game1.exe"
alias game2="C:/Program\ Files\ \(x86\)/studio2/game2.exe"
}
```

All of the substitute format entries are the default values.
