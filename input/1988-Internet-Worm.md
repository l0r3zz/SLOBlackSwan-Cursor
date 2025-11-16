#### The 1988 Morris Worm

**Date**: November 2, 1988  
**Impact**: ~10% of internet-connected computers infected  
**Duration**: Days to fully contain

**Why It Was a Black Swan:**

This was the first major internet worm. The category didn't exist before. Self-replicating programs weren't in the threat model.

```python
class MorrisWorm:
    """The event that created cybersecurity as we know it."""
    
    def failure_characteristics(self):
        return {
            "vector": "Exploited known vulnerabilities (sendmail, finger, rsh)",
            "novel_aspect": "Self-replicating across network autonomously",
            "speed": "Spread faster than humans could respond",
            "impact": "Brought down major academic and military networks"
        }
    
    def why_unpredictable(self):
        """Why this was genuinely unprecedented."""
        return {
            "threat_model": "Individual hacks, not autonomous programs",
            "scale": "Network-wide infection had no precedent",
            "speed": "Replication rate exceeded human response",
            "conception": "Most admins didn't think this was possible"
        }
    
    def transformation(self):
        """What changed in computing after this event."""
        return [
            "CERT (Computer Emergency Response Team) created",
            "Incident response as a discipline emerged",
            "Security patches and update mechanisms developed",
            "Malware became a recognized category of threat",
            "Network monitoring fundamentally changed"
        ]
```
**SLO Implication**: Your availability SLOs measured uptime. But this wasn't downtime in any traditional sense. Systems were "up" but compromised. The metric you needed didn't exist yet.
