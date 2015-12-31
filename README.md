# stagediff
Git utility to diff-add-commit faster

![alt tag](https://github.com/Rombusevil/gg/blob/master/docs/gg_screenshot.png)

### Clone repo
`git clone https://github.com/Rombusevil/stagediff.git --recursive`

don't forget --recursive flag to pull the submodule.

### Description
stagediff will list all your git commited files that have modifications not staged for commit yet.

It let's you review the changes using difftool, select files for staging and commit them.

### Requirements:
* Python2.7
* "git d" aliased to difftool.
* Linux (don't know/care if this works on windows).

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
