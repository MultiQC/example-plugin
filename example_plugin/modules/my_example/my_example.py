"""MultiQC example plugin module"""

import logging

from multiqc import config
from multiqc.plots import linegraph
from multiqc.base_module import BaseMultiqcModule
from multiqc.plots.plotly.line import LinePlotConfig

# Initialise the main MultiQC logger
log = logging.getLogger("multiqc")


class MultiqcModule(BaseMultiqcModule):
    def __init__(self):
        # Halt execution if we've disabled the plugin
        if config.kwargs.get("disable_plugin", True):
            return

        # Initialise the parent module Class object
        super(MultiqcModule, self).__init__(
            name="My Example",
            target="my_example",
            anchor="my_example",
            href="https://github.com/MultiQC/example-plugin",
            info=" is an example module to show how the MultQC plugin system works.",
        )

        # Find and load any input files for this module
        self.my_example_data = dict()
        for f in self.find_log_files("my_example/key_value_pairs"):
            self.my_example_data[f["s_name"]] = dict()
            for line in f["f"].splitlines():
                key, value = line.split(None, 1)
                self.my_example_data[f["s_name"]][key] = value

        self.my_example_plot_data = dict()
        for f in self.find_log_files("my_example/plot_data"):
            self.my_example_plot_data[f["s_name"]] = dict()
            for line in f["f"].splitlines():
                key, value = line.split(None, 1)
                self.my_example_plot_data[f["s_name"]][float(key)] = float(value)

        # Filter out samples matching ignored sample names
        self.my_example_data = self.ignore_samples(self.my_example_data)

        # Nothing found - raise a UserWarning to tell MultiQC
        if len(self.my_example_data) == 0:
            log.debug("Could not find any reports in {}".format(config.analysis_dir))
            raise UserWarning

        log.info("Found {} reports".format(len(self.my_example_data)))

        # Write parsed report data to a file
        self.write_data_file(self.my_example_data, "multiqc_my_example")

        # Add a number to General Statistics table
        headers = {
            "data_key": {
                "title": "# Things",
                "description": "An important number showing something useful.",
                "min": 0,
                "scale": "RdYlGn-rev",
                "format": "{:,.0f}",
            }
        }
        self.general_stats_addcols(self.my_example_data, headers)

        line_plot_html = linegraph.plot(
            self.my_example_plot_data,
            LinePlotConfig(
                id="my_example_plot",
                title="My Example: An example plot",
                ylab="# Other Things",
                xlab="Some Values",
            ),
        )

        # Add a report section with the line plot
        self.add_section(
            description="This plot shows some numbers, and how they relate.",
            helptext="""
            This longer description explains what exactly the numbers mean
            and supports markdown formatting. This means that we can do _this_:

            * Something important
            * Something else important
            * Best of all - some `code`

            Doesn't matter if this is copied from documentation - makes it
            easier for people to find quickly.
            """,
            plot=line_plot_html,
        )
