# Backend Error Handling Patterns

## Error Types

### Client Errors (4xx)
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing/invalid auth
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Validation error

### Server Errors (5xx)
- 500 Internal Server Error: Unexpected error
- 502 Bad Gateway: Upstream service error
- 503 Service Unavailable: Temporary unavailability

## Error Response Format

```python
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable message",
        "details": {
            "field": "specific error details"
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

## Best Practices

- Log all errors with context
- Don't expose internal details to clients
- Provide actionable error messages
- Use consistent error codes
- Include request IDs for tracking

