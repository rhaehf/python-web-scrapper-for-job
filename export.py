import csv

def save_to_file(jobs, term):
  print("save to file!!")
  file = open(f"./csv/{term}.csv", mode='w', encoding="utf-8")
  
  writer = csv.writer(file)
  writer.writerow(["title", "company", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return