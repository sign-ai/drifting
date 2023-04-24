## Releasing process

> :warning: **NOTE:** This is work in progress.

Create branch from `main` with a name that starts with `release` string.

Locally, run `make bump` that will update versions automatically, update 
CHANGELOG.md and will add github tag.

After the merge, the new version will be released to pypi 
[here](https://pypi.org/project/drifting/).
