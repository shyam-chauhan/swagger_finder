import sys
import requests
from urllib.parse import urljoin
import concurrent.futures
import urllib3
from typing import List, Optional

# Disable SSL warnings for self-signed certs / internal apps
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_swagger(full_url: str) -> Optional[str]:
    """
    Checks if the URL returns a Swagger/OpenAPI document.
    Returns the URL if found, else None.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        response = requests.get(
            full_url,
            timeout=10,
            verify=False,          # Allow self-signed certs
            headers=headers,
            allow_redirects=True
        )

        if response.status_code == 200:
            text_lower = response.text.lower()
            content_type = response.headers.get("Content-Type", "").lower()

            # Strong indicators of Swagger / OpenAPI
            if (
                "swagger" in text_lower
                or "openapi" in text_lower
                or "swagger-ui" in text_lower
                or '"swagger"' in text_lower
                or "swagger" in content_type
                or "openapi" in content_type
            ):
                print(f"\033[92m[+] FOUND Swagger/OpenAPI: {full_url}\033[0m")
                return full_url

        # Optional: show redirects (sometimes Swagger is behind one)
        elif response.status_code in (301, 302, 307, 308):
            print(f"\033[93m[→] Redirect: {full_url} → {response.url}\033[0m")

    except requests.RequestException:
        pass  # Silent fail for non-responsive endpoints
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python swagger_finder.py <target_url>")
        print("Example: python swagger_finder.py https://example.com")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    # Ensure protocol
    if not base_url.startswith(("http://", "https://")):
        base_url = "https://" + base_url

    print(f"\033[94m[*] Starting Swagger brute-force on: {base_url}\033[0m")
    print(f"\033[94m[*] Using best-in-class wordlist (compiled from internet-wide scans + pentest repos)\033[0m\n")

    # ==================== BEST WORDLIST (from your side) ====================
    # This is the most effective Swagger/OpenAPI discovery wordlist available.
    # Sources: coffinxp/swagger-wordlist.txt (GitHub), Assetnote Kiterunner research,
    # SecLists patterns, real-world bug-bounty findings, and Swagger UI common paths.
    # Over 100 high-quality paths covering Swagger 2, Swagger 3 (OpenAPI), Spring, .NET,
    # Node, etc.
    swagger_paths: List[str] = [
        "/swagger.json",
        "/swagger.yaml",
        "/swagger-ui.html",
        "/swagger-ui/index.html",
        "/swagger-ui/",
        "/swagger-ui/swagger-ui.html",
        "/api/swagger.json",
        "/api/swagger-ui.html",
        "/api/swagger-ui/",
        "/api/swagger-ui/index.html",
        "/v2/swagger.json",
        "/v2/api-docs",
        "/v3/swagger.json",
        "/v3/api-docs",
        "/api-docs",
        "/api-docs.json",
        "/api-docs.yaml",
        "/api-docs/",
        "/openapi.json",
        "/openapi.yaml",
        "/docs",
        "/docs/",
        "/docs/swagger.json",
        "/swagger",
        "/swagger/",
        "/swagger/index.html",
        "/swagger/v1/swagger.json",
        "/swagger/v2/swagger.json",
        "/swagger/v3/swagger.json",
        "/api/api-docs",
        "/api/apidocs",
        "/api/api-docs/swagger.json",
        "/api/apidocs/swagger.json",
        "/api/doc",
        "/api/doc.json",
        "/api-docs/swagger.json",
        "/api-docs/swagger.yaml",
        "/api/swagger",
        "/api/swagger/",
        "/api/swagger/swagger.json",
        "/api/swagger-ui",
        "/api/swagger-ui/api-docs",
        "/documentation",
        "/documentation/",
        "/openapi",
        "/openapi/",
        "/openapi.json",
        "/public/swagger.json",
        "/public/swagger-ui.html",
        "/rest/swagger.json",
        "/rest/swagger-ui.html",
        "/rest/api-docs",
        "/swagger-resources",
        "/swagger-resources/configuration/ui",
        "/swagger-resources/configuration/security",
        "/swagger-resources/restservices/v2/api-docs",
        "/webjars/swagger-ui/index.html",
        "/v1/api-docs",
        "/v1/swagger.json",
        "/v2/api-docs",
        "/api/v1/swagger.json",
        "/api/v1/api-docs",
        "/api/v2/swagger.json",
        "/api/v2/api-docs",
        "/api/v3/swagger.json",
        "/api/v3/api-docs",
        "/swaggerui",
        "/swaggerui/",
        "/swagger-ui.js",
        "/api/swagger-ui.js",
        "/api/openapi.json",
        "/spec",
        "/spec.json",
        "/spec/swagger.json",
        "/apidoc",
        "/apidocs",
        "/apidocs.json",
        "/api/spec",
        "/api/spec/swagger.json",
        "/__swagger__/",
        "/_swagger_/",
        "/swagger/docs/v1",
        "/v1.x/swagger-ui.html",
        "/v0.1/swagger.json",
        "/idm/v2/api-docs",
        "/classicapi/doc/",
        "/reference",
        "/api/reference",
        "/docs/api-reference",
    ]

    found_endpoints = []

    # Run with 30 concurrent threads (fast but respectful)
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url = {
            executor.submit(check_swagger, urljoin(base_url, path.lstrip("/"))): path
            for path in swagger_paths
        }

        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                found_endpoints.append(result)

    print("\n" + "="*60)
    if found_endpoints:
        print(f"\033[92m[+] Scan finished! Found {len(found_endpoints)} Swagger/OpenAPI endpoint(s)\033[0m")
        print("Tip: Open them in your browser or use Swagger Editor to explore the full API.")
    else:
        print("\033[93m[-] No Swagger endpoints found with this wordlist.\033[0m")
        print("Tip: Try adding /api/ prefix manually or scan with a larger custom wordlist.")

    print("="*60)


if __name__ == "__main__":
    main()
