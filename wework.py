import requests
from bs4 import BeautifulSoup


def extract_job(url):
  data = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser" )
  ul = soup.find("section", {"id": "category-2"}).find("article").find("ul")

  lis = ul.find_all("li")
  for index, li in enumerate(lis):
    print(f"Scrapping WE: Post: ", index)
    all_a = li.find_all("a")
    for a in all_a:
      link = a["href"]
      try:
        company = a.find("span", {"class": "company"}).text
        title = a.find("span", {"class": "title"}).text
        link = "https://weworkremotely.com" + link
        data.append({'title': title, 'company': company, 'link': link})
      except:
        pass
  return data


def get_we_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  print(url)  
  jobs = extract_job(url)
  return jobs
