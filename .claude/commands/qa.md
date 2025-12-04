# QA / Verification Protocol

**Goal:** Verify system integrity and "Nocturne" design compliance.

**Protocol:**
1.  **Design System Audit:**
    - Scan recently modified `.tsx` or `.css` files.
    - **FAIL** if any arbitrary HEX codes (e.g., `#333`) are found. Only `tailwind.config.ts` classes are allowed.
2.  **Backend Safety:**
    - Execute: `python3 manage.py check --deploy`
3.  **Visual Regression:**
    - Execute: `python3 analyze_page.py`
4.  **Report:**
    - Output a concise PASSED/FAILED summary based on the above.
