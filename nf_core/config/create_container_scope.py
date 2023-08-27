#!/usr/bin/env python

import subprocess
import questionary

nxf_software_management = (
    "conda",
    "docker",
    "singularity",
    "charliecloud",
    "podman",
    "sarus",
    "shifter",
    "singularity",
    "apptainer",
)


def check_tool_on_path(tool):
    """
    Simply checks that by running the name of the tool in a shell, that the shell does not return an exit code of 127 (i.e., 'not found' error).
    """
    status = subprocess.getstatusoutput(tool)
    result = status[0] != 127  ## 127 means not found, everything else implies exists, we make assumption it's working
    return result


def create_tool_options(options=nxf_software_management):
    """
    Produces a list of 'valid' entries in a set, i.e., when running check_tool_on_path it will keep everything that has been evaluated to true.

    This reduced list can then be used to offer 'valid' options to the user.
    """
    available = set()
    for i in options:
        if check_tool_on_path(i):
            available.add(i)
    return available


def ask_preferred_container(options):
    """
    Ask the user which container system they wish Nextflow to use.

    Primarily for defining which configuration scope to use.
    """
    q_preferredcontainer = questionary.select(
        "We detected the following available software environment and container engines in your machine./n/nWhich would you like to Nextflow to use?",
        choices=options,
    ).ask()
    return q_preferredcontainer
