# Project Rules for Task Management App

## Project Overview
**Project Name:** Task Management App  
**Project Description:** A web application for managing tasks efficiently.  
**Project Type:** Web Application

## 1. Coding Standards

### Backend (FastAPI)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python coding standards.
- Use async/await for all I/O operations.
- Utilize type hints for function definitions to enhance code readability and maintainability.
- Use environment variables for configuration settings (e.g., database URLs, API keys).

### Frontend (React)
- Use [Airbnb's JavaScript style guide](https://github.com/airbnb/javascript) as a reference.
- Component names must be in PascalCase.
- Maintain a functional component structure utilizing hooks instead of class components when possible.
- Ensure proper use of PropTypes or TypeScript for type checking.

### Database (PostgreSQL)
- Use snake_case for table and column names.
- Normalize the database design according to best practices and avoid redundant data.
- Define clear indices for fields often used in search queries.

## 2. Security Best Practices
- Implement OAuth2 for user authentication with secure password storage (e.g., bcrypt).
- Validate and sanitize all user inputs to prevent SQL Injection and XSS attacks.
- Set appropriate CORS policies to restrict frontend access to the API.
- Use HTTPS for all communication between client and server.
- Regularly update dependencies to mitigate vulnerabilities.

## 3. Documentation Requirements
- Create a README.md file with an overview, setup instructions, and usage guidelines.
- Document API endpoints with Swagger or a similar tool using OpenAPI specifications.
- Maintain a CHANGELOG.md to track changes and versions.
- Create a separate directory for technical documentation covering architecture, design decisions, and onboarding guidelines.

## 4. Quality and Testing Expectations
- Write unit tests for both backend and frontend components with a minimum coverage of 80%.
- Use pytest for testing Python code and Jest for React components.
- Conduct code reviews for all pull requests before merging.
- Use linting tools (e.g., ESLint for JavaScript, Flake8 for Python) to enforce coding standards.

## 5. Naming Conventions and File Organization Standards
- Follow a modular structure; keep components, services, and assets in dedicated directories.
- File structure:
  ```
  task-management-app/
  ├── backend/
  │   ├── app/
  │   ├── models/
  │   ├── routers/
  │   ├── tests/
  ├── frontend/
  │   ├── src/
  │   │   ├── components/
  │   │   ├── services/
  │   │   ├── assets/
  │   │   ├── tests/
  ├── docs/
  ├── README.md
  ├── CHANGELOG.md
  ```
- Use descriptive names for files and functions (e.g., `task_service.py`, `TaskList.js`).

## 6. Error Handling and Logging Requirements
- Implement global exception handling in FastAPI to return error messages in a user-friendly format.
- Use logging libraries (e.g., Python's built-in logging, or LogRocket for React) for error tracking and system events.
- Log at least warning and error level events to ensure issues can be monitored and resolved.

---

By adhering to these guidelines, the Task Management App team will maintain a high level of code quality, security, and maintainability throughout the development lifecycle.