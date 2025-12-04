# CLAUDE.md - Croody Orchestration & Context

## 🧠 Project Architecture & Principles
- **System:** "Croody" Ecosystem (AI Training & E-commerce).
- **Visual Truth:** NO MOCKUPS. The code in `/app` and `/components` is the absolute truth.
- **Design System ("Nocturne"):**
  - Dark background with noise, subtle neon accents.
  - Typography: 'Baloo 2' (Headers), 'Inter' (Body).
  - **Strict Rule:** DO NOT use arbitrary HEX codes (e.g., #333). Use defined Tailwind classes (e.g., `bg-croody-dark`) from `tailwind.config.ts`.
- **Component Reuse:** Check `/components/ui` before creating new UI. Reuse existing components (e.g., `Button.tsx`).

## 📚 Knowledge Base
- **Documentation Index:** `/docs/README.md` (Start here for specific feature details).
- **Architecture:** `/docs/01-ARQUITECTURA`
- **Backend Models:** `/docs/02-BACKEND/modelos`
- **Design System Specs:** `/docs/03-FRONTEND/design-system`

## 🛠 Build, Test & Verification Commands
- **Backend (Django):** `python3 manage.py runserver`
- **Frontend (Next.js):** `npm run dev`
- **Lint/Check:** `python3 manage.py check --deploy`
- **Visual Audit (QA Agent):** `python3 analyze_page.py`

## 🤖 Agent Workflow & Orchestration
This project uses a "Plan-Execute-Verify-Evolve" loop driven by custom commands.

1.  **Plan Phase (`/clarify`):**
    - Use `/clarify [task]` to initiate the Technical PM protocol.
2.  **Execute Phase (Builder):**
    - Consult `CLAUDE.md` and `/docs/` first.
    - Use `claude generate` templates for new components.
3.  **Verify Phase (`/qa`):**
    - Use `/qa` to run the automated verification suite.
4.  **Evolve Phase (`/evolve`):**
    - Run `/evolve` periodically to let the agent analyze session history and self-optimize this file or create new tools.

## 📝 Style Guidelines
- **Python:** PEP 8 standards. Type hints are encouraged.
- **TypeScript/React:** Functional components, strict typing.
- **Language:** Code comments in English; User-facing text in Spanish (unless i18n specified).
