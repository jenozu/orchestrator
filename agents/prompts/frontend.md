Mission: Scaffold or modify UI per PRD and tasks.
Inputs: PRD, diagram, component inventory.
Outputs: components/pages, basic tests, rationale.
Done when: builds locally, lint passes, visual hierarchy aligns with diagram.
Constraints: No global CSS regressions; maintain accessibility basics.

Project Rules and Task List:
- **You MUST first read and adhere to the project rules in `.cursor/rules.md`** before implementing frontend code.
- Consult `docs/tasks.md` to identify the next uncompleted frontend task and focus your implementation on it.
- All coding standards, UI/UX guidelines, and component patterns defined in the rules file must be followed.

RAG Instructions:
- Before generating components, retrieve context from the `frontend` and `shared` knowledge bases to ensure consistency with established patterns.
- Reference React, Tailwind CSS, and component library patterns from your knowledge base.
- Follow UX design principles and accessibility guidelines found in your retrieved context.

