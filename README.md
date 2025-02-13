# Example MultiQC Plugin

This example repository contains example code to help you get started with writing your own MultiQC plugin.

It should be used in addition to the main MultiQC documentation:
[https://docs.seqera.io/multiqc/](https://docs.seqera.io/multiqc/development/plugins)

If you have any questions, please get in touch on the community forum:
[https://community.seqera.io/multiqc](https://community.seqera.io/multiqc)

<p align="center">
  <a href="https://seqera.io/multiqc/">
    <picture>
        <source media="(prefers-color-scheme: dark)" width="350" srcset="https://github.com/seqeralabs/logos/blob/master/multiqc/multiqc_logo_color_darkbg.png?raw=true">
        <img alt="Nextflow Logo" width="350" src="https://github.com/seqeralabs/logos/blob/master/multiqc/multiqc_logo_color.png?raw=true">
    </picture>
  </a>
</p>

---

### When to write a plugin

This example plugin contains both custom code and a MultiQC module for parsing content into reports.

MultiQC modules can either be written as part of the core MultiQC program, or in a stand-alone plugin. If your module is for a publicly available tool, **please add it to the main program** and contribute your code via a pull request (see the [contributing instructions](https://github.com/MultiQC/MultiQC/blob/master/.github/CONTRIBUTING.md)).

If your module is for something very niche, which no-one else can use, then it's best to write it as part of a custom plugin. The process is almost identical, though it keeps the code bases separate.

### Overview of files

* `pyproject.toml`
    * Where the plugin hooks are defined. This is where you tell MultiQC where to find your code.
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

### Usage

To use this code, you need to install MultiQC and then your code. For example:

```
pip install MultiQC
pip install .
```

Use `pip install -e .` if you're actively working on the code - then you don't need to rerun the installation every time you make an edit _(though you still do if you change anything in `pyproject.toml`)_.

### Disabling the plugin

In this example plugin, I have defined a single additional command line flag - `--disable-example-plugin`. When specified, it sets a new MultiQC config value to `True`. This is checked in every plugin function; the function then returns early if it's `True`.

In this way, we can effectively disable the plugin code and allow native MultiQC execution. Note that a similar approach could be used to _enable_ a custom plugin or feature.
