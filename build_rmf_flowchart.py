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

# RMF Step colors for visual distinction
COLORS = {
    'prepare': '#E8F4F8',      # Light blue
    'select': '#FFF4E6',        # Light orange
    'implement': '#E8F5E9',     # Light green
    'assess': '#FFF9C4',        # Light yellow
    'authorize': '#F3E5F5',     # Light purple
    'monitor': '#FFE0B2',       # Light amber
    'decommission': '#FFCDD2'   # Light red
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
    header = f"""%%{{init: {{'theme':'base', 'themeVariables': {{ 'fontSize':'14px'}}}}}}%%
graph TB
    %% =========================================================================
    %% BMC3 Sandbox - Complete RMF Flowchart (NIST SP 800-37 Rev 2)
    %% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    %% 
    %% This diagram shows the complete Risk Management Framework (RMF) lifecycle
    %% for all NIST SP 800-53 Rev 4 controls applicable to the SDA BMC3 Sandbox.
    %% 
    %% RMF Steps:
    %%   1. PREPARE - Prepare the organization and system for RMF
    %%   2. SELECT - Select appropriate security controls
    %%   3. IMPLEMENT - Implement security controls
    %%   4. ASSESS - Assess security control effectiveness
    %%   5. AUTHORIZE - Authorize the system for operation
    %%   6. MONITOR - Continuously monitor security posture
    %%   7. DECOMMISSION - Securely dispose of the system
    %% =========================================================================

    %% Start Node
    START([🚀 BMC3 Sandbox<br/>RMF Process Start])
    style START fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff

"""
    return header

def generate_rmf_main_flow():
    """Generate the main RMF step flow"""
    flow = """    %% =========================================================================
    %% MAIN RMF FLOW (7 Steps)
    %% =========================================================================
    
    START --> PREPARE
    PREPARE[Step 1: PREPARE<br/>Prepare Organization<br/>& System]
    style PREPARE fill:#E8F4F8,stroke:#0277BD,stroke-width:2px
    
    PREPARE --> SELECT
    SELECT[Step 2: SELECT<br/>Select Security<br/>Controls]
    style SELECT fill:#FFF4E6,stroke:#EF6C00,stroke-width:2px
    
    SELECT --> IMPLEMENT
    IMPLEMENT[Step 3: IMPLEMENT<br/>Implement Security<br/>Controls]
    style IMPLEMENT fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    
    IMPLEMENT --> ASSESS
    ASSESS[Step 4: ASSESS<br/>Assess Control<br/>Effectiveness]
    style ASSESS fill:#FFF9C4,stroke:#F9A825,stroke-width:2px
    
    ASSESS --> AUTHORIZE
    AUTHORIZE[Step 5: AUTHORIZE<br/>Authorize System<br/>Operation]
    style AUTHORIZE fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px
    
    AUTHORIZE --> MONITOR
    MONITOR[Step 6: MONITOR<br/>Continuous<br/>Monitoring]
    style MONITOR fill:#FFE0B2,stroke:#E65100,stroke-width:2px
    
    MONITOR --> DECOMMISSION
    DECOMMISSION[Step 7: DECOMMISSION<br/>Dispose of<br/>System/Data]
    style DECOMMISSION fill:#FFCDD2,stroke:#C62828,stroke-width:2px
    
    DECOMMISSION --> END
    END([✅ RMF Process<br/>Complete])
    style END fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff

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
            lines.append(f"    style SEL_{safe_id} fill:#FFF4E6,stroke:#EF6C00\n")
            
            # IMPLEMENT
            lines.append(f"    SEL_{safe_id} --> IMP_{safe_id}\n")
            lines.append(f"    IMP_{safe_id}[{ctrl_id}<br/>Implemented]\n")
            lines.append(f"    style IMP_{safe_id} fill:#E8F5E9,stroke:#2E7D32\n")
            
            # ASSESS
            lines.append(f"    IMP_{safe_id} --> ASS_{safe_id}\n")
            lines.append(f"    ASS_{safe_id}[{ctrl_id}<br/>Assessed]\n")
            lines.append(f"    style ASS_{safe_id} fill:#FFF9C4,stroke:#F9A825\n")
            
            # Connect back to main AUTHORIZE flow
            lines.append(f"    ASS_{safe_id} --> AUTHORIZE\n")
            
            # MONITOR
            lines.append(f"    MONITOR --> MON_{safe_id}\n")
            lines.append(f"    MON_{safe_id}[{ctrl_id}<br/>Monitored]\n")
            lines.append(f"    style MON_{safe_id} fill:#FFE0B2,stroke:#E65100\n")
            
            lines.append("\n")
    
    return ''.join(lines)

def generate_legend():
    """Generate diagram legend"""
    legend = """    %% =========================================================================
    %% LEGEND
    %% =========================================================================
    
    subgraph LEGEND[" 📋 RMF Steps Legend "]
        L1[Step 1: PREPARE]
        style L1 fill:#E8F4F8,stroke:#0277BD
        
        L2[Step 2: SELECT]
        style L2 fill:#FFF4E6,stroke:#EF6C00
        
        L3[Step 3: IMPLEMENT]
        style L3 fill:#E8F5E9,stroke:#2E7D32
        
        L4[Step 4: ASSESS]
        style L4 fill:#FFF9C4,stroke:#F9A825
        
        L5[Step 5: AUTHORIZE]
        style L5 fill:#F3E5F5,stroke:#6A1B9A
        
        L6[Step 6: MONITOR]
        style L6 fill:#FFE0B2,stroke:#E65100
        
        L7[Step 7: DECOMMISSION]
        style L7 fill:#FFCDD2,stroke:#C62828
    end
    style LEGEND fill:#FAFAFA,stroke:#9E9E9E,stroke-width:2px

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
    print("RMF Flowchart Generator")
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
