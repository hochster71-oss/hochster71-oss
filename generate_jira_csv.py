#!/usr/bin/env python3
"""
generate_jira_csv.py

Generates Jira bulk-import CSV files for the complete RMF implementation.

Creates:
- Epics: One per NIST 800-53 control
- Stories: Implementation, Assessment, and Verification tasks for each control

This allows rapid project setup in Jira with proper RMF task tracking.
"""

import csv
import sys
from pathlib import Path
from datetime import datetime, timedelta

INPUT_CSV = "controls_rev4.csv"
OUTPUT_EPICS_CSV = "jira_epics.csv"
OUTPUT_STORIES_CSV = "jira_stories.csv"

# Jira issue type mappings
ISSUE_TYPE_EPIC = "Epic"
ISSUE_TYPE_STORY = "Story"

# Priority levels
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"

# Story point estimates
STORY_POINTS = {
    'implement': 8,
    'assess': 5,
    'verify': 3
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

def get_priority_by_family(family):
    """Determine priority based on control family"""
    high_priority = ['AC', 'AU', 'IA', 'SC', 'SI']  # Critical security families
    medium_priority = ['CM', 'CP', 'IR', 'RA', 'CA']
    
    if family in high_priority:
        return PRIORITY_HIGH
    elif family in medium_priority:
        return PRIORITY_MEDIUM
    else:
        return PRIORITY_LOW

def get_family_name(family_code):
    """Get full family name from code"""
    families = {
        'AC': 'Access Control',
        'AU': 'Audit and Accountability',
        'AT': 'Awareness and Training',
        'CM': 'Configuration Management',
        'CP': 'Contingency Planning',
        'IA': 'Identification and Authentication',
        'IR': 'Incident Response',
        'MA': 'Maintenance',
        'MP': 'Media Protection',
        'PS': 'Personnel Security',
        'PE': 'Physical and Environmental Protection',
        'PL': 'Planning',
        'PM': 'Program Management',
        'RA': 'Risk Assessment',
        'CA': 'Security Assessment and Authorization',
        'SC': 'System and Communications Protection',
        'SI': 'System and Information Integrity',
        'SA': 'System and Services Acquisition'
    }
    return families.get(family_code, 'Other')

def generate_epics(controls):
    """Generate Epic CSV for Jira import"""
    epics = []
    
    for control in controls:
        ctrl_id = control['control_id']
        family = control['family']
        family_name = get_family_name(family)
        priority = get_priority_by_family(family)
        
        epic = {
            'Issue Type': ISSUE_TYPE_EPIC,
            'Summary': f"[{ctrl_id}] {family_name}",
            'Description': f"""# NIST 800-53 Rev 4 Control: {ctrl_id}

**Control Family:** {family_name}

**RMF Steps:**
1. ✅ PREPARE - Control identified and selected
2. 🔄 IMPLEMENT - Deploy control requirements
3. 🔄 ASSESS - Test control effectiveness
4. 🔄 AUTHORIZE - Document and approve
5. 🔄 MONITOR - Continuous assessment

**CCIs Mapped:** {control.get('cci_count', 'N/A')}

**Sample Text:** {control.get('sample_text', 'No description available')}

---
*This Epic tracks the complete RMF lifecycle for control {ctrl_id}.*
*Create child Stories for Implementation, Assessment, and Verification tasks.*
""",
            'Priority': priority,
            'Epic Name': f"{ctrl_id}",
            'Labels': f"RMF,NIST-800-53,{family},{ctrl_id.replace('-', '_')}",
            'Component/s': family_name
        }
        
        epics.append(epic)
    
    return epics

def generate_stories(controls):
    """Generate Story CSV for Jira import"""
    stories = []
    
    for control in controls:
        ctrl_id = control['control_id']
        family = control['family']
        family_name = get_family_name(family)
        priority = get_priority_by_family(family)
        epic_name = ctrl_id
        
        # Story 1: Implementation
        stories.append({
            'Issue Type': ISSUE_TYPE_STORY,
            'Summary': f"[{ctrl_id}] Implement Control Requirements",
            'Description': f"""# Implementation Task for {ctrl_id}

**Objective:** Implement all technical and procedural requirements for {ctrl_id}.

## Tasks:
- [ ] Review control requirements from NIST 800-53 Rev 4
- [ ] Identify technical implementation approach
- [ ] Deploy necessary security controls
- [ ] Configure systems per control specifications
- [ ] Document implementation details
- [ ] Update System Security Plan (SSP)

## Acceptance Criteria:
- All control requirements are deployed
- Configuration is documented
- Implementation evidence is collected
- SSP is updated with implementation details

## RMF Step: 3 - IMPLEMENT
""",
            'Priority': priority,
            'Story Points': STORY_POINTS['implement'],
            'Epic Link': epic_name,
            'Labels': f"RMF,Step3-Implement,{ctrl_id.replace('-', '_')}",
            'Component/s': family_name
        })
        
        # Story 2: Assessment
        stories.append({
            'Issue Type': ISSUE_TYPE_STORY,
            'Summary': f"[{ctrl_id}] Assess Control Effectiveness",
            'Description': f"""# Assessment Task for {ctrl_id}

**Objective:** Test and validate the effectiveness of control {ctrl_id}.

## Tasks:
- [ ] Develop test procedures
- [ ] Execute control testing
- [ ] Interview relevant personnel
- [ ] Review technical configurations
- [ ] Examine documentation
- [ ] Document assessment findings
- [ ] Identify any weaknesses or deficiencies

## Acceptance Criteria:
- All assessment procedures completed
- Findings documented in Security Assessment Report (SAR)
- Evidence collected and stored
- Any deficiencies are tracked

## RMF Step: 4 - ASSESS
""",
            'Priority': priority,
            'Story Points': STORY_POINTS['assess'],
            'Epic Link': epic_name,
            'Labels': f"RMF,Step4-Assess,{ctrl_id.replace('-', '_')}",
            'Component/s': family_name
        })
        
        # Story 3: Verification & Documentation
        stories.append({
            'Issue Type': ISSUE_TYPE_STORY,
            'Summary': f"[{ctrl_id}] Verify and Document Control",
            'Description': f"""# Verification Task for {ctrl_id}

**Objective:** Verify control implementation and complete authorization documentation.

## Tasks:
- [ ] Review assessment results
- [ ] Verify remediation of findings
- [ ] Compile evidence artifacts
- [ ] Update authorization package
- [ ] Obtain AO approval/acceptance
- [ ] Document in POA&M if needed

## Acceptance Criteria:
- Control is verified as effective
- All required evidence is documented
- AO has reviewed and accepted
- Authorization package is complete

## RMF Step: 5 - AUTHORIZE
""",
            'Priority': priority,
            'Story Points': STORY_POINTS['verify'],
            'Epic Link': epic_name,
            'Labels': f"RMF,Step5-Authorize,{ctrl_id.replace('-', '_')}",
            'Component/s': family_name
        })
    
    return stories

def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    output_path = Path(filename)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ Wrote {len(data)} items to {output_path}")

def main():
    print("=" * 70)
    print("Jira CSV Generator for RMF Controls")
    print("=" * 70)
    
    # Load controls
    controls = load_controls(INPUT_CSV)
    
    if not controls:
        print("✗ No controls found. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Generate Epics
    print("\nGenerating Epics...")
    epics = generate_epics(controls)
    epic_fields = ['Issue Type', 'Summary', 'Description', 'Priority', 'Epic Name', 'Labels', 'Component/s']
    write_csv(OUTPUT_EPICS_CSV, epics, epic_fields)
    
    # Generate Stories
    print("\nGenerating Stories...")
    stories = generate_stories(controls)
    story_fields = ['Issue Type', 'Summary', 'Description', 'Priority', 'Story Points', 'Epic Link', 'Labels', 'Component/s']
    write_csv(OUTPUT_STORIES_CSV, stories, story_fields)
    
    print("\n" + "=" * 70)
    print("✓ Jira CSV generation complete!")
    print(f"  Epics created: {len(epics)}")
    print(f"  Stories created: {len(stories)}")
    print(f"\nImport files:")
    print(f"  1. {OUTPUT_EPICS_CSV} (import first)")
    print(f"  2. {OUTPUT_STORIES_CSV} (import after Epics)")
    print("\nImport steps:")
    print("  1. Go to Jira → Settings → System → External System Import")
    print("  2. Select 'CSV' as import type")
    print("  3. Import Epics CSV first")
    print("  4. Import Stories CSV second (ensures Epic Links work)")
    print("=" * 70)

if __name__ == "__main__":
    main()
