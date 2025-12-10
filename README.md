# hochster71-oss â€“ DoD RMF cATO Package for BMC3 Sandbox

A complete, production-ready artefact set that generates:

* A **full Mermaid flow-chart** (RMF Steps 1-7, 100% completed) for **every** NIST SP 800-53 Rev 4 control.  
* **Jira bulk-import CSVs** (Epics = controls, Stories = Implementation/Test/Verification).  
* A **Confluence space XML** that creates the standard RMF pages and embeds the diagram.  
* Automation script that pulls the authoritative DISA-CCI â†” NIST mapping, builds the diagram, and produces all deliverables.

## Quick start

```bash
chmod +x run_all.sh
./run_all.sh
```

For Windows PowerShell:
```powershell
.\run_all.ps1
```

## What's included

1. **fetch_cci_mapping.py** â€“ Downloads the official DISA CCI â†” NIST mapping from cyber.mil
2. **build_rmf_flowchart.py** â€“ Generates the massive Mermaid diagram
3. **generate_jira_csv.py** â€“ Creates bulk-import CSVs for Jira
4. **confluence_export.xml** â€“ Ready-to-import Confluence space
5. **run_all.sh / run_all.ps1** â€“ One-click automation

## Prerequisites

* Python 3.7+
* Git
* GitHub CLI (gh) â€“ optional, for repo creation
* Jira admin access â€“ for bulk import
* Confluence admin access â€“ for space import

## Usage

1. Clone this repository
2. Run the automation script:
   - Linux/Mac: ./run_all.sh
   - Windows: .\run_all.ps1
3. Import generated CSVs into Jira
4. Import confluence_export.xml into Confluence

## Architecture

The system follows the complete RMF lifecycle (NIST SP 800-37 Rev 2):

* **Step 1: Prepare** â€“ System categorization, control selection
* **Step 2: Select** â€“ Tailor controls based on risk assessment
* **Step 3: Implement** â€“ Deploy security controls
* **Step 4: Assess** â€“ Test control effectiveness
* **Step 5: Authorize** â€“ Issue ATO/cATO
* **Step 6: Monitor** â€“ Continuous monitoring
* **Step 7: Decommission** â€“ Secure system disposal

Each NIST 800-53 Rev 4 control becomes a Jira Epic with child stories for implementation, testing, and verification.

## Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- All scripts are tested on both Linux and Windows
- Documentation is updated

## License

MIT License â€“ see LICENSE file for details

## Support

For issues or questions:
- Open an issue in this repository
- Contact the maintainer

## Acknowledgments

* DISA for the authoritative CCI mappings
* NIST for the 800-53 framework
* The DoD RMF community
