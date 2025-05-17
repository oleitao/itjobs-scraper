import requests
from bs4 import BeautifulSoup
import time
import json

BASE_URL = "https://www.itjobs.pt/emprego"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +https://www.example.com/bot)"
}

def get_job_links(page):
    url = f"{BASE_URL}?page={page}"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = soup.select('a[href^="/emprego/"]')
    job_links = []
    for job in jobs:
        href = job['href']
        if href.startswith('/emprego/') and href.count('/') == 2 and href not in job_links:
            job_links.append(href)
    return job_links

def get_job_details(job_url):
    url = f"https://www.itjobs.pt{job_url}"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.select_one('h1')
    title = title.get_text(strip=True) if title else "N/A"

    company = soup.select_one('.job-details .company > a')
    if not company:
        company = soup.select_one('.job-details .company')
    company = company.get_text(strip=True) if company else "N/A"

    location = soup.select_one('.job-details .location')
    location = location.get_text(strip=True) if location else "N/A"

    description = soup.select_one('.job-description')
    description = description.get_text(separator="\n", strip=True) if description else "N/A"

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "url": url
    }

def get_total_pages():
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    last_page = soup.select_one('ul.pagination li:last-child a')
    if last_page and last_page.text.isdigit():
        return int(last_page.text)
    pages = [int(a.text) for a in soup.select('ul.pagination a') if a.text.isdigit()]
    return max(pages) if pages else 1

def main():
    total_pages = get_total_pages()
    print(f"Total de páginas: {total_pages}")
    total_jobs = 0

    with open("itjobs_empregos.jsonl", "w", encoding="utf-8") as f:
        for page in range(1, total_pages + 1):
            print(f"Scraping página {page} de {total_pages}...")
            job_links = get_job_links(page)
            print(f"  {len(job_links)} ofertas encontradas nesta página.")
            for job_link in job_links:
                job = get_job_details(job_link)
                print(f"    - {job['title']} @ {job['company']}")
                json.dump(job, f, ensure_ascii=False)
                f.write('\n')
                total_jobs += 1
                time.sleep(0.5)  # Seja gentil com o site

    print(f"\nTotal de ofertas recolhidas: {total_jobs}")
    print("Guardado em itjobs_empregos.jsonl")

if __name__ == "__main__":
    main()
