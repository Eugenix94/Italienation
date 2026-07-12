import os
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
ROADMAP_JSON = PROCESSED_DIR / "EXTENDED_OPEN_DATA_RESOURCES_AND_API_ROADMAP.json"

class ExternalOpenDataClient:
    """
    Modular Python query client for extracting, testing, and ingesting external SDMX and REST API endpoints
    cataloged in the Italienation Extended Open Data Resources Roadmap.
    """
    def __init__(self, roadmap_path=ROADMAP_JSON):
        self.roadmap_path = Path(roadmap_path)
        self.resources = self._load_roadmap()
        
    def _load_roadmap(self):
        if not self.roadmap_path.exists():
            print(f"[WARNING] Roadmap not found at {self.roadmap_path}. Run build_extended_open_data_resources_roadmap.py first.")
            return {}
        with open(self.roadmap_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {r["resource_id"]: r for r in data}

    def list_available_resources(self):
        """Returns a summary list of all cataloged open data APIs."""
        print("=== AVAILABLE EXTERNAL OPEN DATA RESOURCES ===")
        for r_id, info in self.resources.items():
            print(f"* [{r_id}]: {info['name_it']}")
            print(f"  -> Endpoint: {info['api_endpoint']}")
        return list(self.resources.keys())

    def get_resource_metadata(self, resource_id):
        """Returns full metadata for a specific resource ID."""
        if resource_id not in self.resources:
            print(f"[ERROR] Resource ID `{resource_id}` not found.")
            return None
        return self.resources[resource_id]

    def test_endpoint_connectivity(self, resource_id, timeout_sec=5):
        """Tests HTTP/HTTPS reachability of the API endpoint."""
        meta = self.get_resource_metadata(resource_id)
        if not meta:
            return False
        url = meta["api_endpoint"]
        print(f"Testing connectivity for `{resource_id}` -> {url}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Italienation-OpenScience-Client/1.0"})
            with urllib.request.urlopen(req, timeout=timeout_sec) as response:
                status = response.getcode()
                print(f"  [SUCCESS] Endpoint reachable (HTTP {status})")
                return True
        except urllib.error.HTTPError as e:
            # Some REST API roots return 400 or 404 without specific query params, but are online
            print(f"  [NOTE] Endpoint responded with HTTP {e.code} (API server is online, requires exact query parameters)")
            return True
        except Exception as e:
            print(f"  [ERROR] Connection failed: {e}")
            return False

if __name__ == "__main__":
    client = ExternalOpenDataClient()
    client.list_available_resources()
