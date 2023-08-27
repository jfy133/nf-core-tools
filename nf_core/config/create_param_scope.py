#!/usr/bin/env python

import os
import sys
import psutil
import logging

import questionary

from config_utils import getsysinfo


## Basic config information
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
            configname = questionary.path("What should your new config file be named?", default=configname).ask()

            if os.path.isfile(configname + ".config"):
                ## TODO find the correct logging package/format
                questionary.print(
                    "Existing config with that name detected, but you didn't want to overwrite. Please still start again.",
                    style="bold fg:red",
                )
                sys.exit()

    return configname


def ask_config_type():
    """
    Function to guide what type of profile (and thus which questions to ask) will be built.

    Currently will guide if we have to consider a scheduler or not.
    """
    q_configtype = questionary.select(
        "For which type of infrastructure are you writing a config for?",
        choices=["Laptop/Desktop/Single Node Server", "HPC cluster"],
    ).ask()


## Hardware information
def retrieve_computational_resources():
    """
    Pulls the total number of CPUs and memory of a given unix machine.

    Primarily designed for defining --max_cpus and --max_memory on single-machines.
    """
    cpu = psutil.cpu_count()
    memory = psutil.virtual_memory().total / 1024 / 1024 / 1024
    resources = {"max_cpus": cpu, "max_memory": memory}

    return resources


## User questions
def ask_user_name():
    """
    Asks the name and github handle of the user. Default fall back is the username of the person running the command.

    Primarily for --profile_contact_* parameters.
    """

    username = getattr(psutil.users()[0], "name")

    profile_contact = questionary.text("What is your name", default=username).ask()
    profile_handle = questionary.text("What your internet [Git] handle (optional)", default="").ask()

    contact = {"profile_contact": profile_contact, "profile_handle": profile_handle}

    return contact
