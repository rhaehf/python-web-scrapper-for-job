import requests
from bs4 import BeautifulSoup


def get_last_page(url):
  data = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser" )

  trs = soup.find_all("tr", {"class": "job"})
  for index, tr in enumerate(trs):
    try:      
      link = tr["data-url"]      
      company = tr["data-company"]
      td = tr.find("td", {"class": "company_and_position"})
      title = td.find("h2").text

      td_time = tr.find("td", {"class": "time"}).find("a")
      time = td_time.find("time").text
      if "d" in time: #30일 지난 게시물을 거르기 위해서
        print(f"Scrapping RE: Post: ", index)
        link = "https://remoteok.io" + link
        data.append({'title': title, 'company': company, 'link': link})
    except:
      pass
  return data


def get_re_jobs(word):
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  print(url)  
  jobs = get_last_page(url)
  return jobs
