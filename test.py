import subprocess, threading
from datetime import datetime
import re

payment = '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="Brenny" data-color="#ffffff" data-emoji="☕" data-font="Inter" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#FFDD00" ></script>'

def get_display_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def generate_page():
    def linkify(content):
        return re.sub(
            r"\n(.+)\n  https://(..)\.usembassy\.gov/covid-19-information/",
            "\n<a href=\"https://\g<2>.usembassy.gov/covid-19-information/\">\g<1></a>",
            content
        )

    def remove_empty_entries(content):
        return re.sub(
        r"(<a.+a>)\n\n(<a.+a>)",
        "\g<2>",
        content)

    f = open("country-status.txt", "r")
    file_contents = f.read()
    file_contents.split('\n')
    page_contents = "<html><body><pre>\nLast updated: " + get_display_datetime() + "\n\n" + payment + "\n\n" + file_contents + "</pre></body></html>"
    page_contents = linkify(page_contents)
    new_page_contents = remove_empty_entries(page_contents)
    while new_page_contents != page_contents:
        page_contents = new_page_contents
        new_page_contents = remove_empty_entries(new_page_contents)
    index = open("index.html", "w")
    index.write(page_contents)
    
generate_page()