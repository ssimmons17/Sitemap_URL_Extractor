import os
import re
import requests
import csv

# regex to extract Sitemap URL
# sitemap = 'Sitemap: \W*.*'
sitemap = r'[S|s]itemap: \W*.*'
sitemap2 = r'[S|s]itemap:'
# find_urls = 'http[s]://.*'
# find_urls = r'(https?://\S+)'

# regex to extract urls
find_urls = '(http[s].*?)<'
# extract_urls = ['https://', 'https://']
xml_urls = []
final_links = []
sitemap_container = []

# combine base url with robots.txt
def create_path(base_url: str):
    try:
        base_url_path = base_url
        full_url = os.path.join(base_url_path, 'robots.txt')
        print('\n')
        # print(full_url)
        return full_url
    except TypeError:
        print("Website url must be entered as a string. Please enter the website in the correct format.")


# check robots.txt to confirm existence of sitemap.xml
def confirm_sitemap_exists(full_url):
    deduped_sitemap_container = []
    try:
        page_content = requests.get(full_url)
        sitemap_url = re.findall(sitemap, page_content.text.strip(), re.IGNORECASE)
        if sitemap_url is not None:
            for item in sitemap_url:
                # must replace Sitemap OR sitemap!!
                item = re.sub(sitemap2, '', str(item))
                # item = str(item).replace("Sitemap: ", '',)
                # print(f'This website contains a sitemap: {item}')
                print('\n')
                # print(item)
                sitemap_container.append(item)
                deduped_sitemap_container = [*set(sitemap_container)]
            # print(sitemap_container)
            #print(deduped_sitemap_container)
            # return sitemap_container
            return deduped_sitemap_container
        else:
            # print(page_content)
            print('\n')
            print("This site does not currently have a sitemap listed! Please enter another site or check"
                  " back again later to see if the sitemap has been added.")
    except Exception as error:
        print(error)


# if sitemap.xml exists then parse xml
def xml_parser():
    for link in sitemap_container:
        xml_sitemap_page = requests.get(link).text
        # print(xml_sitemap_page)
        urls = re.findall(find_urls, xml_sitemap_page.strip())
        # if bool(urls):
        for url in urls:
            xml_urls.append(url)
            print(url)
        return xml_urls


def get_final_links():
    try:
        for file in xml_urls:
            pages = requests.get(file).text
            #print(pages)
            urls = re.findall(find_urls, pages.strip())
            # if bool(urls):
            for item in urls:
                print(item)
                final_links.append(item)
                # xml_urls.append(item)
        return final_links
            #print(final_links)
    except Exception as error:
        print(error)


def csv_export():
    # xml_data = xml_urls
    csv_headers = ["Extracted_URLS"]
    with open("Sitemap_URLs.csv", 'w', encoding='utf-8', newline='') as my_file:
        writer = csv.writer(my_file)
        # header for csv
        writer.writerow(csv_headers)
        for url in xml_urls:
            # for url in xml_urls:
            writer.writerow([url])
        my_file.close()
    # print("The parsing is complete. Check CSV file")


def csv_export_additional_links():
    # xml_data = xml_urls
    csv_headers = ["Extracted_URLS"]
    with open("Sitemap_URLs.csv", 'w', encoding='utf-8', newline='') as my_file:
        writer = csv.writer(my_file)
        # header for csv
        writer.writerow(csv_headers)
        for url in final_links:
            # for url in xml_urls:
            writer.writerow([url])
        my_file.close()
    # print("The parsing is complete. Check CSV file")


def main_func(website):
    my_url = create_path(website)
    confirmation = confirm_sitemap_exists(my_url)
    if confirmation:
        # for sitemap_link in confirmation:
        xml_parsing = xml_parser()
        for file in xml_parsing:
            if str(file).endswith('.xml'):
                get_final_links()
                csv_export_additional_links()
            elif not str(file).endswith('.xml'):
                # xml_parsing
                csv_export()
            # print(xml_urls)
            else:
                print("No sitemap XML was found for this website.")
            pass
    # quit()


def main_func_two(website):
    my_url = create_path(website)
    confirmation = confirm_sitemap_exists(my_url)
    if confirmation is not None:
        xml_parsing = xml_parser()
        get_final_links()
        csv_export()
        print(xml_urls)
    else:
        print("No sitemap XML was found for this website.")
        pass
    # quit()


# main_func('https://weather.com/')
# main_func('https://regex101.com/')
# main_func('https://cloudzy.com/')
# main_func('https://www.udemy.com/')
# main_func('https://resumegenius.com/')
# main_func('https://www.allmusic.com/')
# main_func('https://soundcloud.com/')
# main_func_two('https://www.allmusic.com/')
main_func('https://hoplark.com/')
"""
app = Flask(__name__, template_folder='/home/stephen/PycharmProjects/Sitemap_Locator/templates')

#default page
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        website = request.form.get("website")
        main_func(website)
        return render_template("Sitemap_Extractor_Results_COPY.html", final_links = final_links)
    return render_template("Sitemap_Extractor.html")
"""

"""
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        website = request.form.get("website")
        main_func(website)

"""

# app.run(debug=True)
