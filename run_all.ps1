# --------------------------------------------------------------
# run_all.ps1
# 
# Master automation script for BMC3 RMF package generation (Windows)
# Runs all components in the correct order:
#   1. Fetch DISA CCI mappings
#   2. Build RMF flowchart
#   3. Generate Jira CSVs
# --------------------------------------------------------------

$ErrorActionPreference = "Stop"

Write-Host "========================================================================" -ForegroundColor Blue
Write-Host "  BMC3 Sandbox RMF Package Generator" -ForegroundColor Blue
Write-Host "  DoD Risk Management Framework (NIST SP 800-37 Rev 2)" -ForegroundColor Blue
Write-Host "========================================================================" -ForegroundColor Blue
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "[OK] $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python 3 is not installed. Please install Python 3.7 or later." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 1: Fetch CCI Mappings
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host "Step 1: Fetching DISA CCI -> NIST 800-53 Mappings" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Yellow
python fetch_cci_mapping.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to fetch CCI mappings" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Build RMF Flowchart
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host "Step 2: Building RMF Flowchart (Mermaid)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Yellow
python build_rmf_flowchart.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to build flowchart" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Generate Jira CSVs
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host "Step 3: Generating Jira Bulk-Import CSVs" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Yellow
python generate_jira_csv.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to generate Jira CSVs" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Summary
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "[SUCCESS] All Components Generated Successfully!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Generated Files:" -ForegroundColor Blue
Write-Host "  [FILE] controls_rev4.csv       - NIST 800-53 Rev 4 control list"
Write-Host "  [FILE] BMC3_RMF_Rev4.mmd       - Complete RMF flowchart (Mermaid format)"
Write-Host "  [FILE] jira_epics.csv          - Jira Epics (one per control)"
Write-Host "  [FILE] jira_stories.csv        - Jira Stories (implementation tasks)"
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Blue
Write-Host "  1. View flowchart at: https://mermaid.live"
Write-Host "     (Copy contents of BMC3_RMF_Rev4.mmd)"
Write-Host ""
Write-Host "  2. Import Jira CSVs:"
Write-Host "     a. Import jira_epics.csv first"
Write-Host "     b. Import jira_stories.csv second"
Write-Host ""
Write-Host "  3. Import Confluence space:"
Write-Host "     * Import confluence_export.xml via Space Tools -> Import"
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
