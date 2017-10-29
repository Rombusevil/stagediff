# stagediff
Git utility to diff-add-commit faster

![alt tag](https://github.com/Rombusevil/gg/blob/master/docs/gg_screenshot.png)

### Clone repo
`git clone https://github.com/Rombusevil/stagediff.git --recursive`

don't forget --recursive flag to pull the submodule.

### Description
stagediff makes basic and most used git features as easy and fast as possible.
- Lists all the files that have modifications or are not added to the repo while allowing you to navigate the list with arrow keys  
- Run the diff tool on the selected file
- Revert changes on the selected file  
- Mark files to stage
- Write your commit message and commit.

It relies on external applications, "git d" configured to a diff tool and your configured text editor for "git commit" command.


### Requirements:
* Python2.7
* "git d" aliased to difftool.
* Linux (haven't tested on other platforms).

### difftool
I like to use vimdiff as my difftool. 
Here's how you can do the same:
```shell
git config --global diff.tool vimdiff
git config --global difftool.prompt false
git config --global alias.d difftool
```

### Usage
`./stagediff.py <path of git project>`
