"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs
"""
from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_so_jobs
from wework import get_we_jobs
from remoteok import get_re_jobs
from export import save_to_file

app = Flask("Final Job Scrapper")

db = {} # 검색한 단어의 데이터를 저장해둠

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/search")
def report():
  term = request.args.get('term')
  if term: 
    term = term.lower()
    existingJobs = db.get(term)
    if existingJobs: #db에서 검색한 단어의 데이터가 있다면
      jobs = existingJobs
    else:  
      jobs = get_so_jobs(term) + get_we_jobs(term) + get_re_jobs(term)
      db[term] = jobs
  else: # 단어를 입력하지 않아서 None이면
    return redirect("/") 
  return render_template(
    "search.html", 
    searchingBy = term, 
    resultsNumber = len(jobs),
    jobs = jobs
    )

@app.route("/export")
def export():
  try:
    term = request.args.get('term')
    if not term:
      raise Exception()
    term = term.lower()
    jobs = db.get(term)
    if not jobs:
      raise Exception()
    save_to_file(jobs, term)
    return send_file(f"./csv/{term}.csv", as_attachment=True)
  except:
    return redirect("/") 

@app.after_request
def add_header(rqst):
    rqst.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    rqst.headers["Pragma"] = "no-cache"
    rqst.headers["Expires"] = "0"
    rqst.headers['Cache-Control'] = 'public, max-age=0'
    return rqst

@app.errorhandler(404)
def page_not_found(e):
  app.logger.error(e)
  return render_template("404.html"), 404

@app.errorhandler(500)
def data_not_found(e):
  app.logger.error(e)
  return render_template("500.html"), 500


app.run(host="0.0.0.0") #host="0.0.0.0": repl에서 보기위해서 적어둔것임 