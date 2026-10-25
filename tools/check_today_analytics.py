import urllib.request
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "cb9407da402da5e8bc6bc14ad3d0e449")

query = """
query GetTodayBreakdown($zoneTag: String!) {
  viewer {
    zones(filter: {zoneTag: $zoneTag}) {
      countries: httpRequestsAdaptiveGroups(
        limit: 8,
        filter: {datetime_geq: "2026-10-24T00:00:00Z"},
        orderBy: [count_DESC]
      ) {
        count
        dimensions { clientCountryName }
      }
      agents: httpRequestsAdaptiveGroups(
        limit: 8,
        filter: {datetime_geq: "2026-10-24T00:00:00Z"},
        orderBy: [count_DESC]
      ) {
        count
        dimensions { userAgent }
      }
    }
  }
}
"""

payload = {"query": query, "variables": {"zoneTag": ZONE_ID}}
req = urllib.request.Request(
    "https://api.cloudflare.com/client/v4/graphql",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))

print(json.dumps(res, indent=2))
