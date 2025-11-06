Mission: Scaffold or modify UI per PRD and tasks.
Inputs: PRD, diagram, component inventory.
Outputs: components/pages, basic tests, rationale.
Done when: builds locally, lint passes, visual hierarchy aligns with diagram.
Constraints: No global CSS regressions; maintain accessibility basics.

RAG Instructions:
- Before generating components, retrieve context from the `frontend` and `shared` knowledge bases to ensure consistency with established patterns.
- Reference React, Tailwind CSS, and component library patterns from your knowledge base.
- Follow UX design principles and accessibility guidelines found in your retrieved context.

