#!/usr/bin/env bash
# --------------------------------------------------------------
# run_all.sh
# 
# Master automation script for BMC3 RMF package generation
# Runs all components in the correct order:
#   1. Fetch DISA CCI mappings
#   2. Build RMF flowchart
#   3. Generate Jira CSVs
# --------------------------------------------------------------

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# Color output for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================================================${NC}"
echo -e "${BLUE}  BMC3 Sandbox RMF Package Generator${NC}"
echo -e "${BLUE}  DoD Risk Management Framework (NIST SP 800-37 Rev 2)${NC}"
echo -e "${BLUE}========================================================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed. Please install Python 3.7 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Step 1: Fetch CCI Mappings
echo -e "${YELLOW}========================================================================${NC}"
echo -e "${YELLOW}Step 1: Fetching DISA CCI → NIST 800-53 Mappings${NC}"
echo -e "${YELLOW}========================================================================${NC}"
python3 fetch_cci_mapping.py
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to fetch CCI mappings${NC}"
    exit 1
fi
echo ""

# Step 2: Build RMF Flowchart
echo -e "${YELLOW}========================================================================${NC}"
echo -e "${YELLOW}Step 2: Building RMF Flowchart (Mermaid)${NC}"
echo -e "${YELLOW}========================================================================${NC}"
python3 build_rmf_flowchart.py
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to build flowchart${NC}"
    exit 1
fi
echo ""

# Step 3: Generate Jira CSVs
echo -e "${YELLOW}========================================================================${NC}"
echo -e "${YELLOW}Step 3: Generating Jira Bulk-Import CSVs${NC}"
echo -e "${YELLOW}========================================================================${NC}"
python3 generate_jira_csv.py
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to generate Jira CSVs${NC}"
    exit 1
fi
echo ""

# Summary
echo -e "${GREEN}========================================================================${NC}"
echo -e "${GREEN}✓ All Components Generated Successfully!${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo ""
echo -e "${BLUE}Generated Files:${NC}"
echo "  📄 controls_rev4.csv       - NIST 800-53 Rev 4 control list"
echo "  📊 BMC3_RMF_Rev4.mmd       - Complete RMF flowchart (Mermaid format)"
echo "  📋 jira_epics.csv          - Jira Epics (one per control)"
echo "  📋 jira_stories.csv        - Jira Stories (implementation tasks)"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. View flowchart at: https://mermaid.live"
echo "     (Copy contents of BMC3_RMF_Rev4.mmd)"
echo ""
echo "  2. Import Jira CSVs:"
echo "     a. Import jira_epics.csv first"
echo "     b. Import jira_stories.csv second"
echo ""
echo "  3. Import Confluence space:"
echo "     • Import confluence_export.xml via Space Tools → Import"
echo ""
echo -e "${GREEN}========================================================================${NC}"
