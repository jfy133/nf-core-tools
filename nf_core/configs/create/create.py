import json

from nf_core.configs.create.utils import CreateConfig, generate_config_entry


class ConfigCreate:
    def __init__(self, template_config: CreateConfig):
        self.template_config = template_config

    def construct_params(self, contact, handle, description, url):
        final_params = {}

        if contact != "" or not None:
            if handle != "" or not None:
                config_contact = contact + " (" + handle + ")"
            else:
                config_contact = contact
            final_params["config_profile_contact"] = config_contact
        elif handle != "" or not None:
            final_params["config_contact"] = handle
        else:
            pass

        if description != "" or not None:
            final_params["config_profile_description"] = description

        if url != "" or not None:
            final_params["config_profile_url"] = url

        return final_params

    def write_to_file(self):
        ## File name option
        print(self.template_config)
        filename = self.template_config.general_config_name + ".conf"

        ## Collect all config entries per scope, for later checking scope needs to be written
        validparams = self.construct_params(
            self.template_config.config_profile_contact,
            self.template_config.config_profile_handle,
            self.template_config.config_profile_description,
            self.template_config.config_profile_url,
        )

        with open(filename, "w+") as file:

            ## Write params
            if any(validparams):
                file.write("params {\n")
                for entry_key, entry_value in validparams.items():
                    if entry_value is not None:
                        file.write(generate_config_entry(self, entry_key, entry_value))
                    else:
                        continue
                file.write("}\n")
