# Example MultiQC Plugin

### A miniature example of a MultiQC plugin

This example repository contains the following code to help you get
started with writing your own MultiQC plugin.

It should be used in addition to the main MultiQC documentation:
http://multiqc.info/docs/#coding-with-multiqc

If you have any questions, please get in touch on Gitter:
https://gitter.im/ewels/MultiQC

---

![MultiQC](MultiQC_logo.png)

---

### Overview of files

* `setup.py`
    * Where the `setuptools` plugin hooks are defined. This is where you tell MultiQC where to find your code.
    * This file also defines how your plugin should be installed, including required python packages.
* `example_plugin/`
    * Installable Python packages are typically put into a directory with the same name.
* `example_plugin/__init__.py`
    * Python packages need an `__init__.py` file in every directory. Here, these are mostly empty (except the one in the `my_example` folder, which contains a shortcut to make the `import` statement shorter).
    * If you prefer, you can put all code in these files and just reference the directory name only.
* `example_plugin/cli.py`
    * Additional command line parameters to add to MultiQC
* `example_plugin/custom_code.py`
    * File to hold custom functions that can tie into the main MultiQC execution flow.
    * In this file, we define some new config defaults, including the search patterns used by the example module
* `example_plugin/modules/my_example/`
    * This folder contains a minimal MultiQC module which will execute along with all other MultiQC modules (as defined by the `setup.py` hook).

### Disabling the plugin

In this example plugin, I have defined a single additional command line flag - `--disable-example-plugin`. When specified, it sets a new MultiQC config value to `True`. This is checked in every plugin function; the function then returns early if it's `True`.

In this way, we can effectively disable the plugin code and allow native MultiQC execution. Note that a similar approach could be used to _enable_ a custom plugin or feature.
