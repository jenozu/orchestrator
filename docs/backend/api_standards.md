# Backend API Standards

## REST API Guidelines

### Endpoints

- Use resource-based URLs: `/api/users`, `/api/users/{id}`
- Use HTTP methods appropriately:
  - GET: Retrieve resources
  - POST: Create resources
  - PUT: Update entire resource
  - PATCH: Partial update
  - DELETE: Remove resources

### Request/Response Format

- Use JSON for data exchange
- Include proper HTTP status codes
- Return consistent error formats

### Error Handling

```python
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": {...}
    }
}
```

## FastAPI Best Practices

- Use Pydantic models for request/response validation
- Document endpoints with docstrings
- Use dependency injection for shared logic
- Implement proper error handlers

## Security

- Always validate input
- Use authentication/authorization
- Sanitize user inputs
- Follow OWASP API Security Top 10

