#!/usr/bin/env python

import os
import psutil

import questionary

from config_utils import getsysinfo

## Check for existing config file to ensure no unwanted overwrite


def ask_config_name(configname="custom"):
    """
    Function to ask user to define name of config.

    Includes validity check that a config with the same name doesn't exist.
    """
    configname = questionary.path("What should your new config file be named?", default=configname).ask()

    if os.path.isfile(configname + ".config"):
        q_overwrite = questionary.select(
            "Existing config detected. Overwrite?", choices=["Yes", "No"], default="No"
        ).ask()
        if q_overwrite == "Yes":
            os.remove(configname + ".config")
        else:
            pass

    return configname


## Context to build for to guide which type of config to build
def ask_config_type():
    q_configtype = questionary.select(
        "For which type of infrastructure are you writing a config for?",
        choices=["Laptop/Desktop/Single Node Server", "HPC cluster"],
    ).ask()


def retrieve_computational_resources():
    cpu = psutil.cpu_count()
    memory = psutil.virtual_memory().total / 1024 / 1024 / 1024
    resources = {"max_cpus": cpu, "max_memory": memory}

    return resources


## User information
def ask_user_name():
    username = getattr(psutil.users()[0], "name")

    profile_contact = questionary.text("What is your name", default=username).ask()
    profile_handle = questionary.text("What your GitHub handle (optional)", default="").ask()

    contact = {"profile_contact": profile_contact, "profile_handle": profile_handle}

    return contact
