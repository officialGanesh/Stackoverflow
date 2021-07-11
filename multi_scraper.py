
from genericpath import exists
import requests, fire
import json, os
import pandas as pd
from requests_html import HTML
from time import sleep

stackoverflow = "https://stackoverflow.com/"


def filter_data(text,keyname = None):
    """ Cleaning some data """
    if keyname == "Votes":
        text = text.replace("\nvotes","")
    elif keyname == "Answers":
        text = text.replace("answers","")
    elif keyname == "Views":
        text = text.replace(" views","")
    
    elif keyname == "User":
        text = text.split("\n")

    return text


def scrape_posts(tag):
    """ Scraping  every post on the webpage having searched tag """

    for page_number in range(1,11):
        parameters = {
            "tab":"newest",
            "page":page_number,
            "pagesize":15
        }
        url = f"{stackoverflow}questions/tagged/{tag}"
        r = requests.get(url,params=parameters)

        if r.status_code in range(200,299):

            try:
                html_str = r.text
                html = HTML(html=html_str)
                
                post = html.find(".question-summary")
                # post_details = list(post.text.split("\n"))
                
                classes = [".vote",".status",".views",".question-hyperlink",".excerpt",".tags",".user-details"]
                key_names = ["Votes","Answers","Views","Question","Summary","Tags","User"]
                data = []

                for ques_elem in post:
                    post_details = {}
                    for i,search_class in enumerate(classes):
                        element = ques_elem.find(search_class,first=True)
                        keyname = key_names[i]
                        post_details[keyname] = filter_data(element.text,keyname=keyname)
                    data.append(post_details)
                
                with open(os.path.join("Outputs\Multi-Scraper\jsonFiles",f"post{page_number}.json"),"w") as f:
                    f.write(json.dumps(data,indent=2))

                with open(os.path.join("Outputs\Multi-Scraper\csvFiles",f"post{page_number}.csv"),"w") as f:
                    df = pd.DataFrame(data)
                    df.to_csv(f,index=False)

            except Exception as e:
                print("Something went wrong: ",e)

        sleep(1.5)

def main(tag):
    """ Main Script File """

    scrape_posts(tag)


if __name__ == "__main__":

    fire.Fire(main)
    print("Code Completed 🔥")