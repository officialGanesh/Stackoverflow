import requests, fire
from requests.api import post
from requests_html import HTML


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


def scrape_first_post(tag):
    """ Scraping the very first post on the webpage having searched tag """

    url = f"{stackoverflow}questions/tagged/{tag}"
    r = requests.get(url)

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
            print(data[0])
            
        except Exception as e:
            print("Something went wrong: ",e)

    
def main(tag):
    """ Main Script File """

    scrape_first_post(tag)


if __name__ == "__main__":

    fire.Fire(main)
    print("Code Completed 🔥")