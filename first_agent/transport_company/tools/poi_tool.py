import requests, re

def search_pois(place: str, purpose: str, max_results: int = 5):
  """Return up to 5 POIs+snippets for tourism purpose; else []."""
  if purpose.lower() != "tourism": return []
  r = requests.get("https://duckduckgo.com/html/", params={"q": f"{place} top tourist places"}, timeout=20)
  r.raise_for_status()
  html = r.text
  out = []
  for m in re.finditer(r'<a[^>]+class="result__a"[^>]*>(.*?)</a>.*?result__snippet">(.*?)<', html, re.S):
    title = re.sub("<.*?>", "", m.group(1)).strip()
    snip = re.sub("<.*?>", "", m.group(2)).strip()
    out.append({"name": title, "snippet": snip})
    if len(out) >= max_results: break
  return out
