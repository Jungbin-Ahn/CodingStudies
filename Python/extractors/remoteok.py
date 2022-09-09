from bs4 import BeautifulSoup
import requests


def extract_remoteok_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        result = []
        jobs = soup.find_all('td',
                             class_="company position company_and_position")
        del jobs[0]
        for job_selection in jobs:
            company = job_selection.find("h3")
            position = job_selection.find("h2")
            location = job_selection.find("div")
            location = location.string
            if "$" in location:
                location = ""
            anchor = job_selection.find("a")
            link = anchor['href']
            job_data = {
                'company': company.string.replace('\n', '').replace(',', ''),
                'position': position.string.replace('\n', ''),
                'location': location,
                'link': 'https://remoteok.com/' + link
            }

            result.append(job_data)
    else:
        print("Can't get jobs.")
    return result
