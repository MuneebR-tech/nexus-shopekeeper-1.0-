"""
Nexus Shopkeeper - Support & System Error Tracking Module
Logs and tracks runtime edge cases such as membership card PIN errors,
store credit overdrafts, API mismatches, and hardware exceptions.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
import tempfile
import os
import shutil
from typing import Any, List, Dict

def atomic_write_json(file_path: Any, data: Any):
    """Writes data to a temporary file in the same directory, then renames it atomically."""
    file_path_str = str(file_path)
    dir_name = os.path.dirname(file_path_str)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    temp_fd, temp_path = tempfile.mkstemp(dir=dir_name or '.', suffix='.tmp')
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        # Atomic replacement
        os.replace(temp_path, file_path_str)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

# Configure logging
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "support_errors.log"),
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SupportTracker:
    def __init__(self):
        self.error_ledger_path = LOG_DIR / "error_ledger.json"
        self.errors: List[Dict[str, Any]] = []
        self.load_errors()

    def load_errors(self):
        """Loads logged error data from local storage."""
        if self.error_ledger_path.exists():
            try:
                with open(self.error_ledger_path, "r", encoding="utf-8") as f:
                    self.errors = json.load(f)
            except Exception:
                self.errors = []

    def save_errors(self):
        """Saves current error log to disk."""
        atomic_write_json(self.error_ledger_path, self.errors)

    def log_incident(self, incident_type: str, severity: str, details: str, customer_id: str = "GUEST") -> Dict[str, Any]:
        """
        Logs a system exception or business logic violation.
        Types: 'credit_overdraft', 'invalid_membership_pin', 'database_miss', 'api_timeout', 'hardware_fault'
        """
        timestamp = datetime.now().isoformat()
        incident = {
            "timestamp": timestamp,
            "incident_type": incident_type,
            "severity": severity,
            "customer_id": customer_id,
            "details": details
        }
        
        # In-memory logging
        self.errors.append(incident)
        self.save_errors()

        # Std log file recording
        log_msg = f"[{severity.upper()}] Customer={customer_id} | Type={incident_type} | Details={details}"
        if severity.lower() == "critical":
            logging.critical(log_msg)
        elif severity.lower() == "error":
            logging.error(log_msg)
        else:
            logging.warning(log_msg)

        return incident

    def get_incidents(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns the most recent incidents."""
        return self.errors[-limit:]

    # ── ML Classification tracking ───────────────────────────────────────────

    def log_classification_attempt(
        self, vector: List[float], result_segment: str, confidence: float
    ) -> Dict[str, Any]:
        """
        Logs an ML classification attempt (from the /api/classify endpoint).
        Records the input vector, predicted segment, and confidence score.
        """
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "incident_type": "ml_classification",
            "severity": "info",
            "customer_id": "INFERENCE",
            "details": (
                f"Classified vector as '{result_segment}' "
                f"(confidence={confidence:.4f})"
            ),
            "meta": {
                "vector_length": len(vector) if vector else 0,
                "result_segment": result_segment,
                "confidence": round(confidence, 4),
                "vector_snippet": [round(v, 4) for v in (vector or [])[:4]],
            },
        }
        self.errors.append(entry)
        self.save_errors()
        logging.info(
            f"ML Classification: segment={result_segment} confidence={confidence:.4f}"
        )
        return entry

    def log_pin_failure(self, pin: str) -> Dict[str, Any]:
        """
        Logs a failed membership PIN lookup attempt.
        """
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "incident_type": "invalid_membership_pin",
            "severity": "warning",
            "customer_id": "GUEST",
            "details": f"Failed PIN lookup for pin='{pin}'",
        }
        self.errors.append(entry)
        self.save_errors()
        logging.warning(f"PIN lookup failed: pin={pin}")
        return entry

    def get_error_stats(self) -> Dict[str, Any]:
        """
        Returns aggregate error statistics across all logged incidents.
        Breaks down by incident_type and severity.
        """
        type_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        classification_count = 0
        classification_confidence_sum = 0.0
        pin_failure_count = 0

        for entry in self.errors:
            itype = entry.get("incident_type", "unknown")
            sev = entry.get("severity", "unknown")
            type_counts[itype] = type_counts.get(itype, 0) + 1
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

            if itype == "ml_classification":
                classification_count += 1
                meta = entry.get("meta", {})
                classification_confidence_sum += meta.get("confidence", 0.0)

            if itype == "invalid_membership_pin":
                pin_failure_count += 1

        avg_conf = (
            round(classification_confidence_sum / classification_count, 4)
            if classification_count > 0
            else 0.0
        )

        return {
            "total_incidents": len(self.errors),
            "by_type": type_counts,
            "by_severity": severity_counts,
            "ml_classifications": classification_count,
            "ml_avg_confidence": avg_conf,
            "pin_failures": pin_failure_count,
        }
