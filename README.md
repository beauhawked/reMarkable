# reMarkable

This repo contains utilities for my reMarkable Tablet.

## NYT Top Stories Script

`nyt_to_remarkable.py` downloads the latest New York Times top stories, converts them to PDFs, and uploads them to the reMarkable using [`rmapi`](https://github.com/juruen/rmapi).

### Requirements
- Python 3
- `requests`, `pdfkit`, `readability-lxml`, and `beautifulsoup4` Python packages
- [`wkhtmltopdf`](https://wkhtmltopdf.org/) for PDF generation
- `rmapi` configured with your reMarkable account

### Environment Variables
- `NYT_API_KEY` – your New York Times API key (required)
- `NYT_SECTION` – section to fetch (default: `home`)
- `MAX_ARTICLES` – number of articles to download (default: `5`)
- `OUTPUT_DIR` – directory for generated PDFs (default: `nyt_pdfs`)

### Usage
```bash
./nyt_to_remarkable.py
```
This will create PDFs in the output directory and upload them to your tablet.

### Scheduling Daily Runs
Add a cron entry to run the script every morning at 6 AM:
```cron
0 6 * * * /usr/bin/python3 /path/to/nyt_to_remarkable.py >> /path/to/nyt_sync.log 2>&1
```
Make sure the environment variables above are set for the cron job.
