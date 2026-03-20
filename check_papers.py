#!/usr/bin/env python3
"""
Cambridge Past Papers Checker
Checks recent past papers for Business English and Geography from
Cambridge International Education (CAIE) and Cambridge English.
"""

import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# --- Configuration -----------------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 15  # seconds
MAX_DISPLAYED_PAPERS = 10  # cap per qualification to keep output readable

# Cambridge International Education past-papers base URL
CAIE_PAPERS_BASE = (
    "https://www.cambridgeinternational.org"
    "/exam-administration/cambridge-exams-officers-guide/"
    "after-the-exam/past-papers/"
)

# Qualifications to check ─────────────────────────────────────────────────────
# Each entry: (display_label, qualification_code, source_url)

SUBJECTS = {
    "Business English": [
        (
            "Cambridge B1 Business Preliminary",
            "9246",
            "https://www.cambridgeenglish.org/exams-and-tests/"
            "b1-business-preliminary/preparation/",
        ),
        (
            "Cambridge B2 Business Vantage",
            "9247",
            "https://www.cambridgeenglish.org/exams-and-tests/"
            "b2-business-vantage/preparation/",
        ),
        (
            "Cambridge C1 Business Higher",
            "9248",
            "https://www.cambridgeenglish.org/exams-and-tests/"
            "c1-business-higher/preparation/",
        ),
    ],
    "Geography": [
        (
            "Cambridge IGCSE Geography (0460)",
            "0460",
            "https://www.cambridgeinternational.org/programmes-and-qualifications/"
            "cambridge-igcse-geography-0460/",
        ),
        (
            "Cambridge O Level Geography (2217)",
            "2217",
            "https://www.cambridgeinternational.org/programmes-and-qualifications/"
            "cambridge-o-level-geography-2217/",
        ),
        (
            "Cambridge International AS & A Level Geography (9696)",
            "9696",
            "https://www.cambridgeinternational.org/programmes-and-qualifications/"
            "cambridge-international-as-and-a-level-geography-9696/",
        ),
    ],
}

# PapaCambridge search URL (well-known mirror with public past-paper index)
PAPACAMBRIDGE_SEARCH = "https://pastpapers.papacambridge.com/?dir=Cambridge%20IGCSE"

# Cambridge International past-paper finder
CAIE_PAST_PAPER_FINDER = (
    "https://www.cambridgeinternational.org/exam-administration/"
    "cambridge-exams-officers-guide/after-the-exam/past-papers/"
)

# Cambridge English sample test materials
CAMBRIDGE_ENGLISH_BASE = "https://www.cambridgeenglish.org"


# --- Helpers -----------------------------------------------------------------

def section(title: str) -> None:
    """Print a prominent section header."""
    width = 65
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def subsection(title: str) -> None:
    """Print a subsection header."""
    print(f"\n  >> {title}")
    print("  " + "-" * 55)


def fetch(url: str) -> BeautifulSoup | None:
    """Fetch a URL and return a BeautifulSoup object, or None on error."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] Cannot reach {url}")
        print("          Please check your internet connection.")
        return None
    except requests.exceptions.HTTPError as exc:
        print(f"  [ERROR] HTTP {exc.response.status_code} for {url}")
        return None
    except requests.exceptions.Timeout:
        print(f"  [ERROR] Request timed out for {url}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"  [ERROR] {exc}")
        return None


def extract_paper_links(soup: BeautifulSoup, base_url: str) -> list[dict]:
    """
    Extract links that look like past-paper resources from a BeautifulSoup page.

    Returns a list of dicts with keys: title, url.
    """
    papers = []
    keywords = (
        "past paper", "specimen paper", "mark scheme", "question paper",
        "sample paper", "insert", "resource list",
    )
    for tag in soup.find_all("a", href=True):
        text = tag.get_text(strip=True).lower()
        href = tag["href"]
        if any(kw in text for kw in keywords):
            full_url = href if href.startswith("http") else urljoin(base_url, href)
            papers.append({"title": tag.get_text(strip=True), "url": full_url})
    return papers


# --- Subject checkers --------------------------------------------------------

def check_business_english() -> None:
    """Fetch and display recent Business English past-paper information."""
    section("BUSINESS ENGLISH — Cambridge English Business Certificates")

    print(
        "\n  Cambridge offers three levels of Business English qualification:\n"
        "    • B1 Business Preliminary  (formerly BEC Preliminary)\n"
        "    • B2 Business Vantage      (formerly BEC Vantage)\n"
        "    • C1 Business Higher       (formerly BEC Higher)\n"
    )

    for label, code, url in SUBJECTS["Business English"]:
        subsection(label)
        print(f"  Qualification code : {code}")
        print(f"  Preparation page   : {url}\n")

        soup = fetch(url)
        if soup is None:
            _print_manual_steps_business(label, code)
            continue

        papers = extract_paper_links(soup, CAMBRIDGE_ENGLISH_BASE)
        if papers:
            print(f"  Found {len(papers)} resource link(s):\n")
            for p in papers[:MAX_DISPLAYED_PAPERS]:  # cap to keep output readable
                print(f"    • {p['title']}")
                print(f"      {p['url']}")
        else:
            print("  No direct download links found on the preparation page.")
            _print_manual_steps_business(label, code)


def _print_manual_steps_business(label: str, code: str) -> None:
    print(
        f"\n  To find recent '{label}' past papers manually:\n"
        f"    1. Go to https://www.cambridgeenglish.org/exams-and-tests/\n"
        f"    2. Search for '{label}' (code {code})\n"
        f"    3. Navigate to 'Preparation' → 'Sample papers'\n"
        f"    4. Download the most recent available set.\n"
    )


def check_geography() -> None:
    """Fetch and display recent Geography past-paper information."""
    section("GEOGRAPHY — Cambridge International Education")

    print(
        "\n  Cambridge offers Geography at multiple levels:\n"
        "    • Cambridge IGCSE Geography               (0460)\n"
        "    • Cambridge O Level Geography              (2217)\n"
        "    • Cambridge International AS & A Level Geography (9696)\n"
    )

    for label, code, url in SUBJECTS["Geography"]:
        subsection(label)
        print(f"  Qualification code : {code}")
        print(f"  Subject page       : {url}\n")

        soup = fetch(url)
        if soup is None:
            _print_manual_steps_geography(label, code)
            continue

        papers = extract_paper_links(
            soup, "https://www.cambridgeinternational.org"
        )
        if papers:
            print(f"  Found {len(papers)} resource link(s):\n")
            for p in papers[:MAX_DISPLAYED_PAPERS]:
                print(f"    • {p['title']}")
                print(f"      {p['url']}")
        else:
            print("  No direct download links found on the subject page.")
            _print_manual_steps_geography(label, code)


def _print_manual_steps_geography(label: str, code: str) -> None:
    print(
        f"\n  To find recent '{label}' past papers manually:\n"
        f"    1. Go to https://www.cambridgeinternational.org\n"
        f"    2. Search for the subject code '{code}'\n"
        f"    3. Open the qualification page → 'Past papers & marking schemes'\n"
        f"    4. Download papers for the most recent examination series\n"
        f"       (e.g. June 2024, November 2023, March 2024).\n"
    )


# --- Summary -----------------------------------------------------------------

def print_summary() -> None:
    """Print a quick-reference summary of where to find past papers."""
    section("QUICK-REFERENCE SUMMARY")

    rows = [
        ("Business English", "B1 Business Preliminary", "9246",
         "https://www.cambridgeenglish.org/exams-and-tests/b1-business-preliminary/preparation/"),
        ("Business English", "B2 Business Vantage",     "9247",
         "https://www.cambridgeenglish.org/exams-and-tests/b2-business-vantage/preparation/"),
        ("Business English", "C1 Business Higher",      "9248",
         "https://www.cambridgeenglish.org/exams-and-tests/c1-business-higher/preparation/"),
        ("Geography",        "IGCSE Geography",         "0460",
         "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-igcse-geography-0460/"),
        ("Geography",        "O Level Geography",       "2217",
         "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-o-level-geography-2217/"),
        ("Geography",        "AS & A Level Geography",  "9696",
         "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-geography-9696/"),
    ]

    print(f"\n  {'Subject':<18} {'Qualification':<30} {'Code':<8} URL")
    print("  " + "-" * 100)
    for subject, qual, code, url in rows:
        print(f"  {subject:<18} {qual:<30} {code:<8} {url}")

    print(
        "\n  Additional resources:\n"
        "  • CAIE School Support Hub  : https://teachers.cie.org.uk\n"
        "  • Cambridge English        : https://www.cambridgeenglish.org\n"
        "  • Cambridge International  : https://www.cambridgeinternational.org\n"
    )


# --- Entry point -------------------------------------------------------------

def main() -> None:
    print("\n" + "#" * 65)
    print("  Cambridge Past Papers Checker")
    print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 65)

    check_business_english()
    check_geography()
    print_summary()

    print("\n" + "=" * 65)
    print("  Done.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
