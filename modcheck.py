#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import requests
import sys
import json
import os
from requests.auth import HTTPBasicAuth

API_BASE_URL = "https://api.modrinth.com/v2"
#TOKEN_URL = "https://api.example.com/oauth2/token"
#CLIENT_ID = "your_client_id"
CLIENT_SECRET = "mrp_Vs3hYwW8KKh00deTHyx9ukhcuFZAXqznYjoKeowkTIolfXBHsZxFmkvC1gTB"
USER_AGENT = "flugasak/ModCheck/0.1"
MODS_FILE = 'modlist.json'

def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]

def check_value(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

def find_projects_by_name(name, headers, token=CLIENT_SECRET):
    endpoint = f"/search?query={name}&limit=10"
    facets = f'["project_type:mod"],["versions:1.21.5"],["index:downloads"]'
    headers = {**headers, "facets": f"[{facets}]"}
    response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
    response.raise_for_status()
    hits = response.json().get("hits", [])
    return [(hit.get("project_id"), hit.get("slug")) for hit in hits]

# ModChecker class to encapsulate functionality   
class ModChecker:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": USER_AGENT,
        }
        self.mods = []

    # Standard OK message output
    def output_OK(self, message):
        print(f"\033[92m{message}\033[0m")

    # Standard error message output
    def output_error(self, message):
        print(f"\033[91m{message}\033[0m")

    # Load mods from a JSON file
    def load_mods(self, mods_file=MODS_FILE):
        if not os.path.exists(mods_file):
            raise FileNotFoundError(f"Mods file '{mods_file}' not found.")
        with open(mods_file, 'r') as f:
            self.mods = json.load(f)
            #for mod in self.mods:
            #    print("Loaded mod:", mod)

    # Check if a mod has a project ID
    def check_mod(self, mod):
        if mod["project_id"] is None:
            self.output_error(f"Mod {mod} does not have a project ID.")
            return

    #  Check all mods in the list        
    def check_all_mods(self):
        results = {}
        for mod in self.mods:
            #results[mod] = self.check_mod(mod)
            self.check_mod(mod)
        #return results

def main():
    #parser = argparse.ArgumentParser(description="Check values from the online API.")
    
    # Create the checker
    checker = ModChecker(CLIENT_SECRET)
    
    # Load the mods from the JSON file
    try:
        checker.load_mods()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Check all mods
    checker.check_all_mods()

    # try:
    #     response=find_projects_by_name("audioplayer", headers=headers)
    #     print(response)
    # except requests.RequestException as e:
    #     print(f"Error: {e}", file=sys.stderr)
    #     sys.exit(1)


if __name__ == "__main__":
    main()