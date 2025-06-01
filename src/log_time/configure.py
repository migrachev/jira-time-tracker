import re
import os
from ..config import Config
from ..console import demand_choice, demand_prompt

def do(config: Config, is_edit):
    heading = "\033[32mWelcome to configuration.\033[0m"
    if not is_edit:
        heading = """\033[31mIt appears that you are missing configuration to use the tool.\033[0m
\033[32mDo you want to go through configuration now? You can always change it later using --config.\033[0m"""

    # Ask before proceeding
    options: dict[str, str] = { "yes": "Yes, lets do it!", "no": "No, thanks!" }
    proceed = demand_choice(heading, options)

    if proceed == "yes":
        # Get JIRA domain name
        current_jira_domain = config.get("jira_domain_name")
        heading = "We need to know what is you jira domain! (Example: example.jira.com): "
        warn = "The provided domain appears to be invalid. Please try again!"
        jira_domain_name = demand_prompt(heading, warn, is_valid_domain, current_jira_domain)
        config.set("jira_domain_name", jira_domain_name)

        # Get file over pastes preference
        options = {
            "file": "I will use a .txt file to provide logs! (Recommended)",
            "paste": "I prefer to paste data directly without keeping track!"
        }
        heading = "How do you preffer to supply the tool with data?"
        file_over_pastes = demand_choice(heading, options)

        #Get file logs location
        current_logs_location = config.get("default_logs_location")
        if file_over_pastes == "file":
            heading = "Please provide the location of your logs file: "
            warn = "The path you provided appears to be invalid. Please try again!"
            default_logs_location = demand_prompt(heading, warn, os.path.isfile, current_logs_location)
            config.set("default_logs_location", default_logs_location)

        print("\033[32mYou are good to go!\033[0m")
        config.save()
    else:
        print("\033[32mYou can revisit anytime using the --config flag!\033[0m")

def is_valid_domain(domain: str) -> bool:
    if not domain:
        return False
    
    pattern = (
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)'  # Subdomain part
        r'(\.[A-Za-z0-9-]{1,63})*'          # Additional subdomains
        r'\.[A-Za-z]{2,63}$'                # TLD
    )
    
    return bool(re.fullmatch(pattern, domain))