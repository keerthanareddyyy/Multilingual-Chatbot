import urllib.request
import urllib.parse
import json

def transliterate(text, lang_code):
    url = "https://inputtools.google.com/request"
    params = {
        "text": text,
        "itc": f"{lang_code}-t-i0-und",
        "num": 5,
        "cp": 0,
        "cs": 1,
        "ie": "utf-8",
        "oe": "utf-8",
        "app": "demopage"
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data[0] == 'SUCCESS':
                results = data[1][0][1]
                return results
        return [text]
    except Exception as e:
        return [text, str(e)]

if __name__ == "__main__":
    print("Hindi for 'namaste':", transliterate("namaste", "hi"))
    print("Telugu for 'namaskaram':", transliterate("namaskaram", "te"))
    print("Tamil for 'vanakkam':", transliterate("vanakkam", "ta"))
