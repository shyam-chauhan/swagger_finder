# Swagger/OpenAPI Endpoint Finder

A fast, multi-threaded tool to discover Swagger/OpenAPI documentation endpoints on a target web server.

## Overview

This script brute-forces common Swagger and OpenAPI endpoint paths to identify API documentation endpoints. It uses concurrent HTTP requests to efficiently scan a target URL against a curated wordlist of 100+ common Swagger paths.

## Features

- **Multi-threaded scanning**: Uses 30 concurrent worker threads for fast results
- **Comprehensive wordlist**: Covers Swagger 2, OpenAPI 3, and framework-specific paths (Spring, .NET, Node.js, etc.)
- **Self-signed certificate support**: Allows testing against internal apps with HTTPS
- **Redirect detection**: Identifies HTTP redirects to Swagger endpoints
- **Clean output**: Color-coded terminal output for easy reading

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or manually install:
   ```bash
   pip install requests urllib3
   ```

## Usage

```bash
python swagger_finder.py <target_url>
```

### Examples

```bash
# Scan with HTTPS (default)
python swagger_finder.py https://api.example.com

# Scan with HTTP
python swagger_finder.py http://api.example.com

# Scan without protocol (defaults to HTTPS)
python swagger_finder.py api.example.com

# Scan localhost
python swagger_finder.py http://localhost:8080
```

## Output

The script will display:
- **Green `[+]`**: Found Swagger/OpenAPI endpoint
- **Yellow `[→]`**: HTTP redirect detected
- **Blue `[*]`**: Scan progress messages

### Example Output

```
[*] Starting Swagger brute-force on: https://api.example.com
[*] Using best-in-class wordlist (compiled from internet-wide scans + pentest repos)

[+] FOUND Swagger/OpenAPI: https://api.example.com/v2/api-docs
[+] FOUND Swagger/OpenAPI: https://api.example.com/swagger.json

============================================================
[+] Scan finished! Found 2 Swagger/OpenAPI endpoint(s)
Tip: Open them in your browser or use Swagger Editor to explore the full API.
============================================================
```

## Wordlist Sources

The included wordlist is compiled from:
- **coffinxp/swagger-wordlist.txt** (GitHub)
- **Assetnote Kiterunner** research
- **SecLists** common patterns
- Real-world bug-bounty findings
- Swagger UI common paths across frameworks

Covers endpoints for:
- Generic Swagger paths (`/swagger.json`, `/swagger-ui.html`)
- API versioned paths (`/v1/`, `/v2/`, `/v3/`)
- Framework-specific patterns (Spring Boot, .NET, Node.js)
- Documentation endpoints (`/docs`, `/documentation`, `/api-reference`)

## How It Works

1. Takes a base URL as input
2. Constructs full URLs by appending each path from the wordlist
3. Sends concurrent HTTP GET requests (30 workers max)
4. Checks response for Swagger/OpenAPI indicators:
   - HTTP 200 status code
   - "swagger" or "openapi" in response body
   - "swagger" or "openapi" in Content-Type header
   - Specific JSON structure patterns
5. Returns all discovered endpoints

## Requirements

- Python 3.6+
- `requests` - HTTP library
- `urllib3` - HTTP client (dependency of requests)

## SSL/HTTPS Notes

The script automatically:
- Accepts self-signed certificates (useful for internal apps)
- Suppresses SSL warnings for testing
- Follows HTTP redirects automatically

For production security scanning, consider enabling certificate verification by modifying the `verify=False` parameter in the `check_swagger()` function.

## Tips & Troubleshooting

**No endpoints found?**
- Try adding `/api/` prefix manually to the target URL
- Some APIs may require authentication headers
- Check if the target has Swagger enabled
- Try expanding the wordlist with custom paths

**Slow scanning?**
- Increase `max_workers` from 30 to 50-60 for faster scanning (if target allows)
- Decrease timeout from 10 to 5 seconds for unresponsive servers

**Permission denied?**
- Some targets may block brute-force scanning
- Respect rate limits and terms of service
- Use appropriate authorization headers if needed

## License

This tool is provided as-is for security research and testing purposes only. Use responsibly and only on systems you own or have permission to test.
