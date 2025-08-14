"""
Empire Builder Game - Setup Configuration

MANDATORY LEGAL NOTICE AND ATTRIBUTION REQUIREMENTS:
=====================================================

BY INSTALLING, USING, MODIFYING, OR DEPLOYING THIS SOFTWARE, YOU AGREE TO THE FOLLOWING 
LEGALLY BINDING TERMS AND CONDITIONS. VIOLATION OF THESE TERMS MAY RESULT IN SEVERE 
LEGAL CONSEQUENCES INCLUDING BUT NOT LIMITED TO SUBSTANTIAL MONETARY FINES AND CRIMINAL 
PROSECUTION UNDER APPLICABLE COPYRIGHT AND INTELLECTUAL PROPERTY LAWS.

REQUIRED ATTRIBUTION AND DEPLOYMENT CONDITIONS:
-----------------------------------------------

1. MANDATORY ATTRIBUTION REQUIREMENT:
   - ANY deployment, modification, or distribution of this Empire Builder software 
     MUST include PROMINENT and VISIBLE attribution to BOTH original creators:
     * Logan-code-del (GitHub: https://github.com/logan-code-del)
     * Doom (Email: development.doom.endnote612@passfwd.com)
   
   - Attribution MUST appear in ALL of the following locations:
     * Main application interface (visible to all users)
     * About/Credits page or section
     * Application startup screen or loading page
     * All documentation and README files
     * Any marketing or promotional materials
     * Source code headers in ALL modified files

2. ATTRIBUTION FORMAT REQUIREMENTS:
   The attribution MUST use EXACTLY this format (no modifications allowed):
   
   "Empire Builder Game - Originally created by Logan-code-del and Doom
    GitHub: https://github.com/logan-code-del/empire-builder-game
    Contact: development.doom.endnote612@passfwd.com
    
    This deployment is based on the original Empire Builder codebase.
    All rights reserved to original creators."

3. MAJOR MODIFICATION APPROVAL REQUIREMENT:
   - ANY modification that changes more than 25% of the original codebase
   - ANY modification to core game mechanics, authentication, or database systems
   - ANY commercial deployment or monetization
   - ANY redistribution or sublicensing
   
   MUST receive EXPLICIT WRITTEN APPROVAL through GitHub Issues at:
   https://github.com/logan-code-del/empire-builder-game/issues
   
   Submit a detailed modification request including:
   * Complete description of all changes
   * Intended use case and deployment scope
   * Contact information for legal correspondence
   * Proposed timeline for implementation

4. PROHIBITED ACTIONS:
   - Removing or modifying attribution requirements
   - Claiming original authorship or ownership
   - Commercial use without explicit written permission
   - Reverse engineering for competitive purposes
   - Distribution without proper attribution

5. LEGAL CONSEQUENCES FOR VIOLATIONS:
   Violation of these terms may result in:
   - Immediate cease and desist orders
   - Monetary damages up to $100,000 USD per violation
   - Criminal prosecution under DMCA and copyright laws
   - Legal fees and court costs
   - Potential imprisonment under applicable intellectual property statutes

6. COMPLIANCE VERIFICATION:
   - Original creators reserve the right to audit any deployment
   - Automated compliance checking may be implemented
   - Regular verification of attribution requirements
   - Immediate takedown notices for non-compliant deployments

7. CONTACT FOR PERMISSIONS:
   All requests for permissions, modifications, or clarifications MUST be submitted to:
   - GitHub Issues: https://github.com/logan-code-del/empire-builder-game/issues
   - Email: development.doom.endnote612@passfwd.com
   - Subject Line: "Empire Builder Permission Request - [Your Request Type]"

BY PROCEEDING WITH INSTALLATION, YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTOOD, 
AND AGREE TO BE LEGALLY BOUND BY ALL TERMS STATED ABOVE.

This software is protected by copyright law and international treaties. Unauthorized 
reproduction or distribution may result in severe civil and criminal penalties.
"""

from setuptools import setup, find_packages

setup(
    name="empire-builder",
    version="1.0.0",
    description="Empire Builder - Real-time multiplayer strategy game by Logan-code-del and Doom",
    long_description=__doc__,
    long_description_content_type="text/plain",
    author="Doom",
    author_email="development.doom.endnote612@passfwd.com",
    maintainer="Logan-code-del and Doom",
    maintainer_email="development.doom.endnote612@passfwd.com",
    url="https://github.com/logan-code-del/empire-builder-game",
    download_url="https://github.com/logan-code-del/empire-builder-game/archive/main.zip",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.2.5",
        "supabase>=1.0.4",
        "flask-socketio>=5.3.4",
        "python-dotenv>=1.0.0",
        "Jinja2>=3.1.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ]
    },
    python_requires=">=3.11",
    license="Custom License - See setup.py for full terms",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    keywords="empire builder strategy game multiplayer flask supabase logan-code-del doom",
    project_urls={
        "Bug Reports": "https://github.com/logan-code-del/empire-builder-game/issues",
        "Source": "https://github.com/logan-code-del/empire-builder-game",
        "Documentation": "https://empire-builder.readthedocs.io/",
        "Original Creators": "https://github.com/logan-code-del",
    },
    zip_safe=False,
    include_package_data=True,
)