#### The 1980 ARPANET Collapse

**Date**: October 27, 1980  
**Duration**: Several hours  
**Impact**: Complete network outage

**Why It Was a Black Swan:**

This was the first major cascade failure in a packet-switched network. Before this, nobody really understood that the mechanisms designed to make networks resilient (packet routing, redundancy) could actually amplify failures under certain conditions.

```python
class ARPANETCollapse:
    """
    The failure mode was genuinely novel.
    """
    
    def what_happened(self):
        return {
            "trigger": "Software bug in IMP (Interface Message Processor)",
            "mechanism": "Packet replication creating exponential growth",
            "cascade": "Each node tried to route around failures, creating more load",
            "novel_aspect": "Network resilience features became attack vectors"
        }
    
    def why_black_swan(self):
        return {
            "precedent": "No prior cascade failures in packet networks",
            "prediction": "Resilience features assumed to only help",
            "models": "No models of positive feedback in routing",
            "transformation": "Fundamentally changed network protocol design"
        }
    
    def what_changed_after(self):
        """The world after this Black Swan."""
        return {
            "tcp_ip_design": "Flow control mechanisms added",
            "congestion_management": "New field of study created",
            "failure_modes": "Cascade awareness in protocol design",
            "testing": "Stress testing of network protocols became standard"
        }
```

**SLO Implication**: No SLO could have predicted this because the failure mode wasn't in the model. The metrics you'd have been tracking (packet loss, latency) wouldn't have shown the problem until it was already cascading.

