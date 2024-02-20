#!/usr/bin/env python

import os
import sys
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
    if len(options) > 0:
        q_preferredcontainer = questionary.select(
            "We detected the following available software environment and container engines in your machine./n/nWhich would you like to Nextflow to use?",
            choices=options,
        ).ask()
    else:
        q_moving_config = questionary.confirm(
            "No Nextflow compatible software environment or container systems found on your $PATH. Are you writing this config on one machine but for use on another?",
        ).ask()
        if q_moving_config:
            q_preferredcontainer = questionary.select(
                "Which software environment or container system will you use on the machine you'll run Nextflow on?",
                choices=nxf_software_management,
            ).ask()
        else:
            questionary.print(
                "No software environment or container could be found or selected. Please check the Nextflow docs or your installations.",
                style="bold fg:red",
            )
            sys.exit()

    return q_preferredcontainer


def detect_existing_cache_path():
    """
    Detect whether a cache path already exists based on Nextflow environment
    """

    cachedirs = [
        os.getenv("NXF_CHARLIECLOUD_CACHEDIR"),
        os.getenv("NXF_CONDA_CACHEDIR"),
        os.getenv("NXF_SINGULARITY_CACHEDIR"),
        os.getenv("NXF_APPTAINER_CACHEDIR"),
    ]

    return cachedirs


def ask_cache_requested():
    """
    Ask user if they want a cache, if yes ask them where to set, check if exists, if not create
    """

    detected_cachedirs = detect_existing_cache_path().any()

    ## TODO: remove nones, pick first?
    ##guessed_default_cachedir = detected_cachedir

    q_cacherequested = questionary.confirm(
        """Would you like to set a cache directory for your conda environments or container images?
        By doing so, you only have to download each environment once, and thus re-use them across each pipeline run.
        This is recommended to save hard drive space.
        """,
    ).ask()
    if q_cacherequested:
        cache_path = questionary.path(
            "Please specify the path to an existing or new cache directory",  # default=guessed_default_cachedir
        ).ask()

        if os.path.isdir(cache_path):
            q_reuse = questionary.confirm("Existing cache directory detected. Re-use?", default="Yes").ask()
            if q_reuse:
                cache_dir = cache_path
            else:
                ## TODO all below
                configname = questionary.path("What should your new config file be named?", default=configname).ask()

                if os.path.isfile(configname + ".config"):
                    ## TODO find the correct logging package/format
                    questionary.print(
                        "Existing config with that name detected, but you didn't want to overwrite. Please still start again.",
                        style="bold fg:red",
                    )
                    sys.exit()

    return
