import subprocess
import os
import csv
import json
from django.conf import settings

BIN_PATH = os.path.join(settings.BASE_DIR, 'telemetry', 'bin', 'CICFlowMeter.jar')

class CICFlowMeterWrapper:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run_analysis(self):
        """
        Runs CICFlowMeter on the input directory (containing .pcap) 
        and outputs CSVs to output_dir.
        """
        if not os.path.exists(BIN_PATH):
            raise FileNotFoundError(f"CICFlowMeter JAR not found at {BIN_PATH}")
        
        # command: java -jar CICFlowMeter.jar <input_dir> <output_dir>
        cmd = ['java', '-jar', BIN_PATH, self.input_dir, self.output_dir]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"CICFlowMeter failed: {result.stderr}")
        
        return self._get_latest_results()

    def _get_latest_results(self):
        """
        Parses the generated CSV files and returns a list of flows.
        """
        results = []
        if not os.path.exists(self.output_dir):
            return results

        for filename in os.listdir(self.output_dir):
            if filename.endswith('.csv'):
                path = os.path.join(self.output_dir, filename)
                with open(path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results.append(row)
        return results

def get_mock_traffic_data():
    """Returns mock data if real analysis fails or for testing."""
    return [
        {"src_ip": "192.168.1.5", "dst_ip": "8.8.8.8", "protocol": "UDP", "length": 120},
        {"src_ip": "192.168.1.10", "dst_ip": "10.0.0.1", "protocol": "TCP", "length": 500},
    ]
