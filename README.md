# fylr-lib-plugin-python3
collection of python3 classes and functions for fylr plugins

## include library in python plugins

> python package names can not include `-`. make sure to rename the submodule folder if you import it

In python plugin folder (e.g. `src/server`):

```!shell
git submodule add git@github.com:programmfabrik/fylr-lib-plugin-python3.git fylr_lib_plugin_python3
```

In python code:

```!python
import fylr_lib_plugin_python3.util as util
```
