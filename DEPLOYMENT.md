# Deployment Guide

Complete deployment instructions for the BMC3 Sandbox RMF Package.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Scripts](#running-the-scripts)
4. [Jira Configuration](#jira-configuration)
5. [Confluence Setup](#confluence-setup)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### Required Software

- **Python 3.7 or later**
  - Windows: Download from [python.org](https://www.python.org/downloads/)
  - Linux: `sudo apt install python3` or `sudo yum install python3`
  - macOS: `brew install python3`

- **Git**
  - Windows: [Git for Windows](https://gitforwindows.org/)
  - Linux: `sudo apt install git`
  - macOS: `brew install git`

### Optional Software

- **GitHub CLI** (for repository management)
  ```bash
  # Windows
  winget install GitHub.cli
  
  # Linux
  sudo apt install gh
  
  # macOS
  brew install gh
  ```

### Access Requirements

- **Jira**: Admin or project admin access for bulk import
- **Confluence**: Space admin access for XML import
- **Internet Access**: For downloading DISA CCI mappings (optional - falls back to sample data)

## Installation

### Option 1: Clone from GitHub

```bash
git clone https://github.com/hochster71-oss/hochster71-oss.git
cd hochster71-oss
```

### Option 2: Download ZIP

1. Go to: https://github.com/hochster71-oss/hochster71-oss
2. Click "Code" → "Download ZIP"
3. Extract to your desired location
4. Open terminal/PowerShell in the extracted folder

### Verify Installation

```bash
# Check Python version
python --version  # or python3 --version

# List project files
ls  # or dir on Windows
```

## Running the Scripts

### Windows (PowerShell)

```powershell
# Navigate to project directory
cd path\to\hochster71-oss

# Run the automation
.\run_all.ps1
```

### Linux/macOS (Bash)

```bash
# Navigate to project directory
cd path/to/hochster71-oss

# Make script executable
chmod +x run_all.sh

# Run the automation
./run_all.sh
```

### Manual Execution (All Platforms)

If you prefer to run scripts individually:

```bash
# Step 1: Fetch CCI mappings
python fetch_cci_mapping.py

# Step 2: Build flowchart
python build_rmf_flowchart.py

# Step 3: Generate Jira CSVs
python generate_jira_csv.py
```

### Expected Output

After successful execution, you'll have:

```
hochster71-oss/
├── controls_rev4.csv       # 180 NIST controls
├── BMC3_RMF_Rev4.mmd       # Mermaid flowchart (~85KB)
├── jira_epics.csv          # 180 Jira Epics
├── jira_stories.csv        # 540 Jira Stories
└── (original source files)
```

## Jira Configuration

### Step 1: Prepare Jira Project

1. **Create or select a project**
   - Go to Jira → Projects → Create Project
   - Choose "Scrum" or "Kanban" template
   - Name it "BMC3 RMF" or similar

2. **Verify project configuration**
   - Ensure "Epic" issue type is enabled
   - Ensure "Story" issue type is enabled
   - Check that required fields exist

### Step 2: Import Epics

1. **Navigate to import**
   - Go to Settings (⚙️) → System
   - Find "External System Import"
   - Select "CSV"

2. **Import epic file**
   - Choose `jira_epics.csv`
   - Map columns:
     - Issue Type → Issue Type
     - Summary → Summary
     - Description → Description
     - Priority → Priority
     - Epic Name → Epic Name
     - Labels → Labels
     - Component/s → Component/s

3. **Validate import**
   - Check for errors
   - Verify 180 Epics were created
   - Review a few Epics to ensure data is correct

### Step 3: Import Stories

1. **Import story file**
   - Repeat import process
   - Choose `jira_stories.csv`
   - Map columns including "Epic Link"

2. **Validate import**
   - Check that 540 Stories were created
   - Verify Stories are linked to correct Epics
   - Check Story Points are populated

### Step 4: Configure Board

1. **Create RMF board**
   ```
   Backlog → In Progress → In Review → Done
   ```

2. **Set up swimlanes**
   - By Epic (to see control families)
   - By Priority (to focus on critical controls)

3. **Configure filters**
   - Control family (AC, AU, SC, etc.)
   - RMF step (Implement, Assess, Authorize)
   - Priority level

## Confluence Setup

### Step 1: Create Space

1. **Option A: Import XML (Recommended)**
   - Go to Space Tools → Content Tools → Import
   - Select "Space import"
   - Upload `confluence_export.xml`
   - Choose "Import as new space"

2. **Option B: Manual Setup**
   - Create new space "BMC3 RMF"
   - Copy pages from template manually

### Step 2: Add Mermaid Plugin

The flowchart requires a Mermaid plugin to display properly:

1. **Install plugin**
   - Go to Settings → Find new apps
   - Search "Mermaid"
   - Install "Mermaid Diagrams for Confluence" or similar

2. **Alternative: Use external viewer**
   - Visit https://mermaid.live
   - Paste contents of `BMC3_RMF_Rev4.mmd`
   - Export as SVG/PNG
   - Embed image in Confluence

### Step 3: Embed Flowchart

1. **Edit the "Complete RMF Flow Diagram" page**
2. **Add Mermaid macro**
   - Type `/mermaid`
   - Paste contents of `BMC3_RMF_Rev4.mmd`
3. **Save and view**

### Step 4: Link to Jira

1. **Add Jira macros**
   - Use "Jira Issues" macro
   - Filter by label: `RMF`
   - Show Epic progress

2. **Create dashboard**
   - Embed Jira filters
   - Show control implementation status
   - Add charts and metrics

## Troubleshooting

### Python Not Found

**Symptom:** `'python' is not recognized as an internal or external command`

**Solution:**
- Verify Python is installed: `python --version`
- Try `python3` instead of `python`
- Add Python to PATH (Windows)
- Reinstall Python with "Add to PATH" checked

### CCI Download Fails

**Symptom:** `HTTP Error 404: Not Found` when fetching CCI list

**Solution:**
- This is expected - the DISA URL may change
- Script automatically falls back to sample data
- Sample data includes 180 controls (18 families × 10 controls)
- For production, manually download CCI list from cyber.mil

### Jira Import Errors

**Symptom:** "Epic Link not found" or similar errors

**Solution:**
1. Import Epics BEFORE Stories
2. Verify Epic Name matches Epic Link values
3. Check that issue types exist in project
4. Ensure custom fields are mapped correctly

### PowerShell Execution Policy

**Symptom:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single session
PowerShell -ExecutionPolicy Bypass -File .\run_all.ps1
```

### Mermaid Diagram Too Large

**Symptom:** Confluence/browser freezes when viewing diagram

**Solution:**
- View diagram at https://mermaid.live instead
- Export as SVG and embed image
- Split into multiple smaller diagrams
- Filter by control family

## Advanced Configuration

### Customizing Control List

Edit `fetch_cci_mapping.py` to filter controls:

```python
# Add after line that creates controls dict
controls = {k: v for k, v in controls.items() if v['family'] in ['AC', 'AU', 'IA']}
```

### Adjusting Jira Fields

Edit `generate_jira_csv.py` to add custom fields:

```python
# Add to Epic or Story dictionary
'Custom Field': 'Custom Value',
'Due Date': '2025-12-31',
```

### Modifying Flowchart

Edit `build_rmf_flowchart.py`:

- Change colors in `COLORS` dict
- Modify node shapes
- Add custom relationships
- Filter controls by family

### Environment Variables

Create `.env` file for configuration:

```bash
# DISA CCI URL (if different)
CCI_URL=https://custom.url/cci_list.xml

# Output file names
CONTROLS_CSV=my_controls.csv
FLOWCHART_MMD=my_flowchart.mmd
```

## Support

- **Issues**: https://github.com/hochster71-oss/hochster71-oss/issues
- **Discussions**: GitHub Discussions tab
- **Email**: See repository contact information

## Security Notes

- **CUI Warning**: Generated files may contain Controlled Unclassified Information (CUI)
- **Access Control**: Restrict Jira/Confluence access appropriately
- **Data Handling**: Follow your organization's data handling procedures
- **Audit Trail**: Enable audit logging in Jira and Confluence

## Next Steps

After successful deployment:

1. **Customize controls** for your specific system
2. **Assign owners** to each Epic in Jira
3. **Set due dates** based on your RMF timeline
4. **Begin implementation** following RMF steps
5. **Track progress** using Jira boards and Confluence
6. **Update regularly** as controls are implemented

---

**Version:** 1.0  
**Last Updated:** 2025-12-10  
**License:** MIT
