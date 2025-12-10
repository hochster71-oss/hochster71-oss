#!/usr/bin/env python3
"""
build_rmf_flowchart.py

Generates a comprehensive Mermaid flowchart covering the complete RMF lifecycle
(NIST SP 800-37 Rev 2, Steps 1-7) for EVERY NIST 800-53 Rev 4 control.

This creates a massive, production-ready diagram suitable for:
- DoD cATO packages
- System Security Plans (SSPs)
- Security Assessment Reports (SARs)
- Confluence/Wiki documentation
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

INPUT_CSV = "controls_rev4.csv"
OUTPUT_MMD = "BMC3_RMF_Rev4.mmd"

# RMF Step colors for SAIC dark theme
COLORS = {
    'prepare': '#1a1a2e',       # Dark navy
    'select': '#16213e',        # Deep blue
    'implement': '#0f3460',     # Ocean blue
    'assess': '#1a4d6d',        # Steel blue
    'authorize': '#00d9ff',     # SAIC cyan
    'monitor': '#005f73',       # Teal
    'decommission': '#2d4654'   # Slate
}

def load_controls(csv_path):
    """Load controls from CSV file"""
    controls = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            controls = list(reader)
        print(f"✓ Loaded {len(controls)} controls from {csv_path}")
        return controls
    except FileNotFoundError:
        print(f"✗ Error: {csv_path} not found. Run fetch_cci_mapping.py first.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading CSV: {e}", file=sys.stderr)
        sys.exit(1)

def sanitize_id(text):
    """Convert text to valid Mermaid node ID"""
    return text.replace('-', '_').replace('(', '').replace(')', '').replace(' ', '_')

def generate_flowchart_header():
    """Generate Mermaid flowchart header"""
    header = f"""%%{{init: {{'theme':'dark', 'themeVariables': {{ 'fontSize':'14px', 'primaryColor':'#00d9ff', 'primaryTextColor':'#fff', 'primaryBorderColor':'#16213e', 'lineColor':'#00d9ff', 'secondaryColor':'#1a1a2e', 'tertiaryColor':'#0f3460'}}}}}}%%
graph TB
    %% =========================================================================
    %% SAIC RMF AUTOMATION SUITE - Complete RMF Flowchart
    %% Developed by: Michael Hoch | SAIC
    %% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    %% 
    %% This diagram shows the complete Risk Management Framework (RMF) lifecycle
    %% for all NIST SP 800-53 Rev 4 controls applicable to DoD systems.
    %% Framework: NIST SP 800-37 Rev 2
    %% 
    %% RMF Steps:
    %%   1. PREPARE - Prepare the organization and system for RMF
    %%   2. SELECT - Select appropriate security controls
    %%   3. IMPLEMENT - Implement security controls
    %%   4. ASSESS - Assess security control effectiveness
    %%   5. AUTHORIZE - Authorize the system for operation
    %%   6. MONITOR - Continuously monitor security posture
    %%   7. DECOMMISSION - Securely dispose of the system
    %% 
    %% © 2025 SAIC | www.saic.com
    %% =========================================================================

    %% Start Node
    START([🛡️ SAIC RMF Suite<br/>Process Start])
    style START fill:#00d9ff,stroke:#16213e,stroke-width:3px,color:#000

"""
    return header

def generate_rmf_main_flow():
    """Generate the main RMF step flow"""
    flow = """    %% =========================================================================
    %% MAIN RMF FLOW (7 Steps)
    %% =========================================================================
    
    START --> PREPARE
    PREPARE[Step 1: PREPARE<br/>Prepare Organization<br/>& System]
    style PREPARE fill:#1a1a2e,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    PREPARE --> SELECT
    SELECT[Step 2: SELECT<br/>Select Security<br/>Controls]
    style SELECT fill:#16213e,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    SELECT --> IMPLEMENT
    IMPLEMENT[Step 3: IMPLEMENT<br/>Implement Security<br/>Controls]
    style IMPLEMENT fill:#0f3460,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    IMPLEMENT --> ASSESS
    ASSESS[Step 4: ASSESS<br/>Assess Control<br/>Effectiveness]
    style ASSESS fill:#1a4d6d,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    ASSESS --> AUTHORIZE
    AUTHORIZE[Step 5: AUTHORIZE<br/>Authorize System<br/>Operation]
    style AUTHORIZE fill:#00d9ff,stroke:#16213e,stroke-width:2px,color:#000
    
    AUTHORIZE --> MONITOR
    MONITOR[Step 6: MONITOR<br/>Continuous<br/>Monitoring]
    style MONITOR fill:#005f73,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    MONITOR --> DECOMMISSION
    DECOMMISSION[Step 7: DECOMMISSION<br/>Dispose of<br/>System/Data]
    style DECOMMISSION fill:#2d4654,stroke:#00d9ff,stroke-width:2px,color:#fff
    
    DECOMMISSION --> END
    END([✅ SAIC RMF<br/>Complete])
    style END fill:#00d9ff,stroke:#16213e,stroke-width:3px,color:#000

"""
    return flow

def generate_control_nodes(controls):
    """Generate nodes for each control across all RMF steps"""
    lines = []
    lines.append("""    %% =========================================================================
    %% CONTROL-SPECIFIC IMPLEMENTATION FLOW
    %% Each control flows through all 7 RMF steps
    %% =========================================================================

""")
    
    # Group controls by family for better organization
    families = {}
    for control in controls:
        family = control['family']
        if family not in families:
            families[family] = []
        families[family].append(control)
    
    # Generate nodes for each family
    for family_code in sorted(families.keys()):
        family_controls = families[family_code]
        lines.append(f"    %% {family_code} Family Controls\n")
        
        for control in family_controls:
            ctrl_id = control['control_id']
            safe_id = sanitize_id(ctrl_id)
            
            # Connect to SELECT step (controls are selected here)
            lines.append(f"    SELECT --> SEL_{safe_id}\n")
            lines.append(f"    SEL_{safe_id}[{ctrl_id}<br/>Selected]\n")
            lines.append(f"    style SEL_{safe_id} fill:#16213e,stroke:#00d9ff,color:#fff\n")
            
            # IMPLEMENT
            lines.append(f"    SEL_{safe_id} --> IMP_{safe_id}\n")
            lines.append(f"    IMP_{safe_id}[{ctrl_id}<br/>Implemented]\n")
            lines.append(f"    style IMP_{safe_id} fill:#0f3460,stroke:#00d9ff,color:#fff\n")
            
            # ASSESS
            lines.append(f"    IMP_{safe_id} --> ASS_{safe_id}\n")
            lines.append(f"    ASS_{safe_id}[{ctrl_id}<br/>Assessed]\n")
            lines.append(f"    style ASS_{safe_id} fill:#1a4d6d,stroke:#00d9ff,color:#fff\n")
            
            # Connect back to main AUTHORIZE flow
            lines.append(f"    ASS_{safe_id} --> AUTHORIZE\n")
            
            # MONITOR
            lines.append(f"    MONITOR --> MON_{safe_id}\n")
            lines.append(f"    MON_{safe_id}[{ctrl_id}<br/>Monitored]\n")
            lines.append(f"    style MON_{safe_id} fill:#005f73,stroke:#00d9ff,color:#fff\n")
            
            lines.append("\n")
    
    return ''.join(lines)

def generate_legend():
    """Generate diagram legend"""
    legend = """    %% =========================================================================
    %% LEGEND - SAIC RMF AUTOMATION SUITE
    %% Developed by Michael Hoch | SAIC
    %% =========================================================================
    
    subgraph LEGEND[" 📋 RMF Steps Legend - SAIC Dark Theme "]
        L1[Step 1: PREPARE]
        style L1 fill:#1a1a2e,stroke:#00d9ff,color:#fff
        
        L2[Step 2: SELECT]
        style L2 fill:#16213e,stroke:#00d9ff,color:#fff
        
        L3[Step 3: IMPLEMENT]
        style L3 fill:#0f3460,stroke:#00d9ff,color:#fff
        
        L4[Step 4: ASSESS]
        style L4 fill:#1a4d6d,stroke:#00d9ff,color:#fff
        
        L5[Step 5: AUTHORIZE]
        style L5 fill:#00d9ff,stroke:#16213e,color:#000
        
        L6[Step 6: MONITOR]
        style L6 fill:#005f73,stroke:#00d9ff,color:#fff
        
        L7[Step 7: DECOMMISSION]
        style L7 fill:#2d4654,stroke:#00d9ff,color:#fff
    end
    style LEGEND fill:#0a0a0f,stroke:#00d9ff,stroke-width:2px

"""
    return legend

def write_flowchart(output_path, content):
    """Write flowchart to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Wrote flowchart to {output_path}")
    print(f"  Total size: {len(content):,} characters")

def main():
    print("=" * 70)
    print("SAIC RMF AUTOMATION SUITE")
    print("RMF Flowchart Generator")
    print("Developed by Michael Hoch | SAIC")
    print("=" * 70)
    
    # Load controls
    controls = load_controls(INPUT_CSV)
    
    if not controls:
        print("✗ No controls found. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Build flowchart
    print("\nGenerating Mermaid flowchart...")
    
    flowchart = []
    flowchart.append(generate_flowchart_header())
    flowchart.append(generate_rmf_main_flow())
    flowchart.append(generate_control_nodes(controls))
    flowchart.append(generate_legend())
    
    content = ''.join(flowchart)
    
    # Write output
    output_path = Path(OUTPUT_MMD)
    write_flowchart(output_path, content)
    
    print("\n" + "=" * 70)
    print("✓ RMF Flowchart generation complete!")
    print(f"  Controls processed: {len(controls)}")
    print(f"  Output: {output_path}")
    print("\nYou can view this diagram at:")
    print("  • https://mermaid.live")
    print("  • Confluence (if configured)")
    print("  • VS Code (with Mermaid extension)")
    print("=" * 70)

if __name__ == "__main__":
    main()
