from flask import Flask, send_from_directory
import subprocess, threading
from datetime import datetime
import re
app = Flask(__name__, static_url_path='')

payment = '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="Brenny" data-color="#ffffff" data-emoji="☕" data-font="Inter" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#FFDD00" ></script>'

def get_display_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def query_covid_status():
    print("Querying latest covid travel status")
    subprocess.call("/app/covid.sh")
    print("Status updated")

def generate_page():
    print("Generating new page")
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
    print("Page generated")
    
def update_covid_status_file():
    threading.Timer(86400, update_covid_status_file).start()
    
    current_time = get_display_datetime()
    print("Updating covid travel status at", current_time)

    query_covid_status()    
    generate_page()

print("Starting server")
update_covid_status_file()

@app.route('/')
def serve():
    return send_from_directory('/app/', 'index.html')
