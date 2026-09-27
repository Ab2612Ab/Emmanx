from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = FastAPI(title="Python Website SEO Analyzer", version="1.0.0")

class AnalyzeRequest(BaseModel):
    url: HttpUrl

def check_page(url: str):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent":"Python-SEO-Analyzer/1.0"})
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=422, detail=f"Could not fetch website: {exc}")

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    description = soup.find("meta", attrs={"name":"description"})
    viewport = soup.find("meta", attrs={"name":"viewport"})
    canonical = soup.find("link", attrs={"rel":"canonical"})
    h1s = soup.find_all("h1")
    images = soup.find_all("img")
    links = soup.find_all("a", href=True)
    https = urlparse(url).scheme == "https"

    checks = {
        "title": {"pass": 10 <= len(title) <= 60, "value": title, "recommendation": "Use a descriptive title between 10 and 60 characters."},
        "meta_description": {"pass": description is not None and 50 <= len(description.get("content","")) <= 160, "value": description.get("content","") if description else "", "recommendation": "Add a unique meta description between 50 and 160 characters."},
        "single_h1": {"pass": len(h1s) == 1, "value": len(h1s), "recommendation": "Use exactly one clear H1 heading."},
        "viewport": {"pass": viewport is not None, "value": viewport.get("content","") if viewport else "", "recommendation": "Add a responsive viewport meta tag."},
        "canonical": {"pass": canonical is not None, "value": canonical.get("href","") if canonical else "", "recommendation": "Add a canonical URL to help search engines understand the preferred page."},
        "https": {"pass": https, "value": https, "recommendation": "Serve the website over HTTPS."},
        "image_alt": {"pass": all(img.get("alt") for img in images), "value": f"{sum(1 for img in images if img.get('alt'))}/{len(images)} images have alt text", "recommendation": "Add useful alt text to images."},
    }
    passed=sum(1 for c in checks.values() if c["pass"])
    score=round((passed/len(checks))*100)
    return {"url":url,"status_code":response.status_code,"score":score,"checks":checks,
            "summary":{"title_length":len(title),"h1_count":len(h1s),"image_count":len(images),"link_count":len(links)}}

@app.get("/")
def root():
    return {"name":"Website SEO Analyzer","python":True,"framework":"FastAPI","status":"operational","docs":"/docs"}

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.post("/analyze")
def analyze(payload: AnalyzeRequest):
    return check_page(str(payload.url))
