import os
import urllib.request
import json
import datetime
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "cb9407da402da5e8bc6bc14ad3d0e449")

def query_graphql(query, variables):
    payload = {
        "query": query,
        "variables": variables
    }
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4/graphql",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_full_report():
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=7)).isoformat()
    end_date = today.isoformat()
    start_time = "2026-10-19T00:00:00Z"
    
    # 1. Daily trend
    q_daily = """
    query GetZoneDaily($zoneTag: String!, $startDate: Date!, $endDate: Date!) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequests1dGroups(
            limit: 10,
            filter: {date_geq: $startDate, date_leq: $endDate},
            orderBy: [date_ASC]
          ) {
            dimensions { date }
            sum { requests bytes cachedRequests cachedBytes threats pageViews }
            uniq { uniques }
          }
        }
      }
    }
    """
    daily_res = query_graphql(q_daily, {"zoneTag": ZONE_ID, "startDate": start_date, "endDate": end_date})
    
    # 2. Country Breakdown
    q_country = """
    query GetCountries($zoneTag: String!, $startTime: String!) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequestsAdaptiveGroups(
            limit: 15,
            filter: {datetime_geq: $startTime},
            orderBy: [count_DESC]
          ) {
            count
            dimensions {
              clientCountryName
            }
          }
        }
      }
    }
    """
    country_res = query_graphql(q_country, {"zoneTag": ZONE_ID, "startTime": start_time})
    
    # 3. HTTP Status Codes
    q_status = """
    query GetStatus($zoneTag: String!, $startTime: String!) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequestsAdaptiveGroups(
            limit: 10,
            filter: {datetime_geq: $startTime},
            orderBy: [count_DESC]
          ) {
            count
            dimensions {
              edgeResponseStatus
            }
          }
        }
      }
    }
    """
    status_res = query_graphql(q_status, {"zoneTag": ZONE_ID, "startTime": start_time})
    
    # 4. Top Request Paths
    q_paths = """
    query GetPaths($zoneTag: String!, $startTime: String!) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequestsAdaptiveGroups(
            limit: 15,
            filter: {datetime_geq: $startTime},
            orderBy: [count_DESC]
          ) {
            count
            dimensions {
              clientRequestPath
            }
          }
        }
      }
    }
    """
    paths_res = query_graphql(q_paths, {"zoneTag": ZONE_ID, "startTime": start_time})

    # 5. Top User Agents / AI Crawlers
    q_ua = """
    query GetUA($zoneTag: String!, $startTime: String!) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequestsAdaptiveGroups(
            limit: 15,
            filter: {datetime_geq: $startTime},
            orderBy: [count_DESC]
          ) {
            count
            dimensions {
              userAgent
            }
          }
        }
      }
    }
    """
    ua_res = query_graphql(q_ua, {"zoneTag": ZONE_ID, "startTime": start_time})

    return {
        "daily": daily_res,
        "countries": country_res,
        "status": status_res,
        "paths": paths_res,
        "user_agents": ua_res
    }

if __name__ == "__main__":
    report = fetch_full_report()
    print(json.dumps(report, indent=2))
