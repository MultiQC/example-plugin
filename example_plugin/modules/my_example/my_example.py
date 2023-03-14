#!/usr/bin/env python

""" MultiQC example plugin module """

from __future__ import print_function
from collections import OrderedDict
import logging

from multiqc import config
from multiqc.plots import table, linegraph
from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the main MultiQC logger
log = logging.getLogger("multiqc")


class MultiqcModule(BaseMultiqcModule):
    def __init__(self):

        # Halt execution if we've disabled the plugin
        if config.kwargs.get("disable_plugin", True):
            return None

        # Initialise the parent module Class object
        super(MultiqcModule, self).__init__(
            name="My Example",
            target="my_example",
            anchor="my_example",
            href="https://github.com/MultiQC/example-plugin",
            info=" is an example module to show how the MultiQC plugin system works.",
        )

        # Find and load any input files for this module
        self.my_example_data = dict()
        for f in self.find_log_files("my_example/key_value_pairs"):
            self.my_example_data[f["s_name"]] = dict()
            for l in f["f"].splitlines():
                key, value = l.split(None, 1)
                self.my_example_data[f["s_name"]][key] = value

        for f in self.find_log_files("my_example/mzml"):
            if f["s_name"] not in self.my_example_data:
                self.my_example_data[f["s_name"]] = dict()
            for l in f["f"].splitlines():
                if "\t" not in l:
                    continue
                key, value = l.split("\t", 1)
                if key in [
                    "number of spectra",
                    "total number of peaks",
                    "number of MS1 spectra",
                    "number of MS2 spectra",
                ]:
                    self.my_example_data[f["s_name"]][key] = value

        for f in self.find_log_files("my_example/search"):
            if f["s_name"] not in self.my_example_data:
                self.my_example_data[f["s_name"]] = dict()
            for l in f["f"].splitlines():
                if "\t" not in l:
                    continue
                key, value = l.split("\t", 1)
                if key in [
                    "general: num. of protein hits",
                    "general: num. of matched spectra",
                    "general: num. of modified top-hits",
                    "general: num. of non-redundant peptide hits (only hits that differ in sequence and/or modifications): ",
                ]:
                    key = "search: " + key
                    self.my_example_data[f["s_name"]][key] = value

        for f in self.find_log_files("my_example/fdr"):
            if f["s_name"] not in self.my_example_data:
                self.my_example_data[f["s_name"]] = dict()
            for l in f["f"].splitlines():
                if "\t" not in l:
                    continue
                key, value = l.split("\t", 1)
                if key in [
                    "general: num. of protein hits",
                    "general: num. of matched spectra",
                    "general: num. of modified top-hits",
                    "general: num. of non-redundant peptide hits (only hits that differ in sequence and/or modifications): ",
                ]:
                    key = "fdr: " + key
                    self.my_example_data[f["s_name"]][key] = value

        self.my_example_plot_data = dict()
        for f in self.find_log_files("my_example/plot_data"):
            self.my_example_plot_data[f["s_name"]] = dict()
            for l in f["f"].splitlines():
                key, value = l.split(None, 1)
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
        headers = OrderedDict()
        headers["data_key"] = {
            "title": "# Things",
            "description": "An important number showing something useful.",
            "min": 0,
            "scale": "RdYlGn-rev",
            "format": "{:,.0f}",
        }
        headers["number of spectra"] = {
            "title": "spectra",
            "description": "Total number of MS1 and MS2 spectra.",
            "min": 0,
            "scale": "RdBu",
            "format": "{:,.0f}",
        }
        headers["total number of peaks"] = {
            "title": "peaks",
            "description": "Total number of peaks in all MS1 and MS2 spectra.",
            "min": 0,
            "scale": "RdBu",
            "format": "{:,.0f}",
        }
        headers["number of MS1 spectra"] = {
            "title": "MS1 spectra",
            "description": "Number of MS1 spectra.",
            "min": 0,
            "scale": "RdGy",
            "format": "{:,.0f}",
        }
        headers["number of MS2 spectra"] = {
            "title": "MS2 spectra",
            "description": "Number of MS2 spectra.",
            "min": 0,
            "scale": "RdGy",
            "format": "{:,.0f}",
        }
        headers["fdr: general: num. of matched spectra"] = {
            "title": "PSMs",
            "description": "Number of peptide-spectrum-matches after false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdYlGn",
            "format": "{:,.0f}",
        }
        self.general_stats_addcols(self.my_example_data, headers)

        # Create line plot
        pconfig = {
            "id": "my_example_plot",
            "title": "My Example: An example plot",
            "ylab": "# Other Things",
            "xlab": "Some Values",
        }
        line_plot_html = linegraph.plot(self.my_example_plot_data, pconfig)

        # Add a report section with the line plot
        self.add_section(
            name="Identifications",
            description="Summary statistics of peptide and protein identifications.",
            helptext="""
            This section provides detailed information of the peptide and protein identifications.
            
            * straight out of the search engine
            * after FDR filtering
            * protein inference
            """,
            plot=line_plot_html,
        )

        # construct simple table for IDs
        self.exp_design_table = dict()
        x = dict()
        x["A"] = float(10)
        x["B"] = float(20)
        self.exp_design_table["Fraction_Group"] = x
        y = dict()
        y["A"] = float(30)
        y["B"] = float(40)
        self.exp_design_table["Fraction"] = y
        headers = OrderedDict()
        headers["Fraction_Group"] = {
            "description": "Fraction_Group",
            "bgcols": "Rd",
        }
        headers["Fraction"] = {
            "description": "Fraction identifier",
            "bgcols": "Rd",
        }

        id_table = dict()
        for sample, data in self.my_example_data.items():
            print(sample + "  -->  ")
            id_table[sample] = dict()

            key = "search: general: num. of matched spectra"
            if key in data:
                id_table[sample]["PSMs before FDR"] = float(data[key])

            key1 = "search: general: num. of matched spectra"
            key2 = "number of MS2 spectra"
            if (key1 in data) and (key2 in data):
                id_table[sample]["mapping rate before FDR"] = (
                    100 * float(data[key1]) / float(data[key2])
                )

            key = "search: general: num. of non-redundant peptide hits (only hits that differ in sequence and/or modifications): "
            if key in data:
                id_table[sample]["non-redundant peptide hits before FDR"] = data[key]

            key = "search: general: num. of protein hits"
            if key in data:
                id_table[sample]["protein hits before FDR"] = data[key]

            key1 = "fdr: general: num. of matched spectra"
            key2 = "number of MS2 spectra"
            if (key1 in data) and (key2 in data):
                id_table[sample]["mapping rate after FDR"] = (
                    100 * float(data[key1]) / float(data[key2])
                )

            key = "fdr: general: num. of matched spectra"
            if key in data:
                id_table[sample]["PSMs after FDR"] = data[key]

            key = "fdr: general: num. of non-redundant peptide hits (only hits that differ in sequence and/or modifications): "
            if key in data:
                id_table[sample]["non-redundant peptide hits after FDR"] = data[key]

            key = "fdr: general: num. of protein hits"
            if key in data:
                id_table[sample]["protein hits after FDR"] = data[key]

            for key, value in data.items():
                print("    **" + key + "**  -->  " + value)

        headers = OrderedDict()
        headers["PSMs before FDR"] = {
            "title": "PSMs before FDR",
            "description": "Number of peptide-spectrum-matches straight out of the search engine i.e. before false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdGy",
            "format": "{:,.0f}",
        }
        headers["mapping rate before FDR"] = {
            "title": "mapping rate before FDR",
            "description": "Number of peptide-spectrum-matches / number of MS2 spectra before false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdGy",
        }
        headers["non-redundant peptide hits before FDR"] = {
            "title": "non-redundant peptide hits before FDR",
            "description": "Number of non-redundant peptide sequences (sequences which differ in sequence and/or modifications) before false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdGy",
            "format": "{:,.0f}",
        }
        headers["protein hits before FDR"] = {
            "title": "protein hits before FDR",
            "description": "Number of proteins which have one or multiple peptide hits before false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdGy",
            "format": "{:,.0f}",
        }
        headers["PSMs after FDR"] = {
            "title": "PSMs after FDR",
            "description": "Number of peptide-spectrum-matches straight out of the search engine i.e. after false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdYlGn",
            "format": "{:,.0f}",
        }
        headers["mapping rate after FDR"] = {
            "title": "mapping rate after FDR",
            "description": "Number of peptide-spectrum-matches / number of MS2 spectra after false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdYlGn",
        }
        headers["non-redundant peptide hits after FDR"] = {
            "title": "non-redundant peptide hits after FDR",
            "description": "Number of non-redundant peptide sequences (sequences which differ in sequence and/or modifications) after false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdYlGn",
            "format": "{:,.0f}",
        }
        headers["protein hits after FDR"] = {
            "title": "protein hits after FDR",
            "description": "Number of proteins which have one or multiple peptide hits after false-discovery-rate filtering.",
            "min": 0,
            "scale": "RdYlGn",
            "format": "{:,.0f}",
        }

        self.add_section(
            name="Identifications",
            description="Summary statistics of peptide and protein identifications.",
            helptext="""
            This section provides detailed information of the peptide and protein identifications.

            * straight out of the search engine
            * after FDR filtering
            * protein inference
            """,
            plot=table.plot(id_table, headers),
        )
