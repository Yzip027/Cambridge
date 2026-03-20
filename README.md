# Cambridge Past Papers Checker

A Python script that checks and lists recent past papers from Cambridge
International Education (CAIE) and Cambridge English for:

- **Business English** — B1 Business Preliminary, B2 Business Vantage, C1 Business Higher
- **Geography** — Cambridge IGCSE (0460), O Level (2217), AS & A Level (9696)

## Requirements

- Python 3.10+
- `requests` and `beautifulsoup4` (see `requirements.txt`)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python check_papers.py
```

The script will:

1. Contact the relevant Cambridge websites and look for past-paper links on
   the preparation/subject pages for each qualification.
2. Print any direct download links it finds.
3. If a page is unavailable (e.g. no internet connection), print step-by-step
   instructions for finding the papers manually.
4. Finish with a quick-reference summary table of all qualifications and their
   official URLs.

## Subjects covered

| Subject | Qualification | Code | Official page |
|---|---|---|---|
| Business English | B1 Business Preliminary | 9246 | [link](https://www.cambridgeenglish.org/exams-and-tests/b1-business-preliminary/preparation/) |
| Business English | B2 Business Vantage | 9247 | [link](https://www.cambridgeenglish.org/exams-and-tests/b2-business-vantage/preparation/) |
| Business English | C1 Business Higher | 9248 | [link](https://www.cambridgeenglish.org/exams-and-tests/c1-business-higher/preparation/) |
| Geography | IGCSE Geography | 0460 | [link](https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-igcse-geography-0460/) |
| Geography | O Level Geography | 2217 | [link](https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-o-level-geography-2217/) |
| Geography | AS & A Level Geography | 9696 | [link](https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-geography-9696/) |

## Finding past papers manually

### Business English

1. Visit <https://www.cambridgeenglish.org/exams-and-tests/>
2. Navigate to the desired qualification level (B1 / B2 / C1 Business).
3. Open **Preparation → Sample papers**.
4. Download the most recent set of sample / past papers.

### Geography

1. Visit <https://www.cambridgeinternational.org>
2. Search for the qualification code (e.g. `0460` for IGCSE Geography).
3. Open the qualification page → **Past papers & marking schemes**.
4. Filter by the most recent examination series (e.g. June 2024, November 2023).
