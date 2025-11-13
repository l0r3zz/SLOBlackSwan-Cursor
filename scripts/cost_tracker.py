#!/usr/bin/env python3
"""Track API costs across providers."""

import os
from datetime import datetime
import json

class CostTracker:
    # Approximate costs per 1M tokens (as of Nov 2025)
    COSTS = {
        "claude-sonnet-4": {"input": 3.00, "output": 15.00},
        "claude-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
        "perplexity": {"request": 0.005}  # per request
    }
    
    def estimate_monthly(self, usage_pattern):
        """
        Estimate monthly costs based on usage pattern.
        
        usage_pattern = {
            "claude-sonnet-4": {"input_tokens": 1000000, "output_tokens": 500000},
            "gpt-4o": {"input_tokens": 500000, "output_tokens": 200000},
            ...
        }
        """
        total = 0
        breakdown = {}
        
        for model, usage in usage_pattern.items():
            if model not in self.COSTS:
                continue
            
            if "input_tokens" in usage:
                cost = (
                    (usage["input_tokens"] / 1_000_000) * self.COSTS[model]["input"] +
                    (usage["output_tokens"] / 1_000_000) * self.COSTS[model]["output"]
                )
            elif "requests" in usage:
                cost = usage["requests"] * self.COSTS[model]["request"]
            else:
                cost = 0
            
            breakdown[model] = round(cost, 2)
            total += cost
        
        return {
            "total": round(total, 2),
            "breakdown": breakdown
        }

# Example usage
if __name__ == "__main__":
    tracker = CostTracker()
    
    # Moderate book writing usage
    moderate_usage = {
        "claude-sonnet-4": {
            "input_tokens": 5_000_000,   # Reading research, context
            "output_tokens": 2_000_000    # Drafting
        },
        "gpt-4o": {
            "input_tokens": 2_000_000,   # Reading drafts
            "output_tokens": 500_000      # Critiques
        },
        "gemini-2.5-pro": {
            "input_tokens": 1_000_000,   # Technical validation
            "output_tokens": 300_000
        },
        "perplexity": {
            "requests": 200              # Research queries
        }
    }
    
    estimate = tracker.estimate_monthly(moderate_usage)
    
    print("=== Monthly Cost Estimate ===")
    print(f"Total: ${estimate['total']}")
    print("\nBreakdown:")
    for model, cost in estimate['breakdown'].items():
        print(f"  {model}: ${cost}")
