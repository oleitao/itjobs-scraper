import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

BASE_URL = "https://www.itjobs.pt/emprego"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +https://www.example.com/bot)"
}

def get_total_pages():
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    last_page = soup.select_one('ul.pagination li:last-child a')
    if last_page and last_page.text.isdigit():
        return int(last_page.text)
    pages = [int(a.text) for a in soup.select('ul.pagination a') if a.text.isdigit()]
    return max(pages) if pages else 1

def get_jobs_from_page(page):
    url = f"{BASE_URL}?page={page}"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    offers = []

    for li in soup.select("ul.list-unstyled.listing > li"):
        title_elem = li.select_one("div.list-title a.title")
        company_elem = li.select_one("div.list-name a")
        location_elem = li.select_one("div.list-details")

        if not title_elem:
            continue

        title = title_elem.get_text(strip=True)
        job_url = "https://www.itjobs.pt" + title_elem['href']
        company = company_elem.get_text(strip=True) if company_elem else "N/A"
        location = location_elem.get_text(strip=True).replace("\xa0", " ") if location_elem else "N/A"

        job_resp = requests.get(job_url, headers=HEADERS)
        job_soup = BeautifulSoup(job_resp.text, "html.parser")

        tags = [tag.get_text(strip=True) for tag in job_soup.select("div.sidebar-content span.label")]

        content_block = job_soup.select_one("div.content-block")
        description = ""
        if content_block:
            parts = []
            for elem in content_block.find_all(["p", "ul", "ol"]):
                if elem.name in ["ul", "ol"]:
                    items = [f"- {li.get_text(strip=True)}" for li in elem.find_all("li")]
                    parts.extend(items)
                else:
                    parts.append(elem.get_text(strip=True))
            description = "\n".join(parts)

        offers.append({
            "title": title,
            "company": company,
            "location": location,
            "url": job_url,
            "tags": tags,
            "description": description
        })

        time.sleep(0.2)

    return offers


def main():
    total_pages = get_total_pages()
    print(f"Total de páginas: {total_pages}")
    total_jobs = 0

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"itjobs_empregos_{timestamp}.jsonl"

    with open(filename, "w", encoding="utf-8") as f:
        for page in range(1, total_pages + 1):
            print(f"Scraping página {page} de {total_pages}...")
            jobs = get_jobs_from_page(page)
            print(f"  {len(jobs)} ofertas encontradas nesta página.")
            for job in jobs:
                json.dump(job, f, ensure_ascii=False)
                f.write('\n')
                total_jobs += 1
            time.sleep(0.5)

    print(f"\nTotal de ofertas recolhidas: {total_jobs}")
    print("Guardado em itjobs_lista.jsonl")
    print(filename)

if __name__ == "__main__":
    main()
