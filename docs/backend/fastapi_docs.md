# FastAPI Documentation

Source: Context7 - FastAPI Library Docs
Topic: API endpoints, routing, dependencies

---

### Configure APIRouter with Prefix and Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

Sets up an APIRouter for item-related endpoints. It configures a common prefix '/items', assigns 'items' tag, defines default responses, and applies a shared 'X-Token' dependency to all routes within this router.

```Python
from fastapi import APIRouter, Depends, HTTPException

from .dependencies import get_x_token

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_x_token)]
)


@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}
```

---

### Apply Dependencies in FastAPI WebSocket Route

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md

Shows how to integrate FastAPI's dependency injection system (e.g., `Depends`, `Query`, `Cookie`, `Path`) directly into a WebSocket endpoint's signature. This allows for validation and extraction of request data before the WebSocket connection is fully established and messages are handled, enhancing security and functionality.

```python
from fastapi import WebSocket, Depends, Query, Cookie, WebSocketException, status

# Example dependency function (assumed to be defined elsewhere)
async def get_cookie_or_token(
    websocket: WebSocket,
    session: str | None = Cookie(None),
    token: str | None = Query(None),
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket("/ws/{item_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    # ... WebSocket handling logic ...
    pass
```

---

### FastAPI Dependency Injection for Reusable Logic

Source: https://context7.com/fastapi/fastapi/llms.txt

This section showcases FastAPI's dependency injection system, allowing common logic to be shared across multiple endpoints. It demonstrates creating a dependency function for common query parameters (`common_parameters`) and a dependency for managing a database connection (`get_db`), including proper cleanup using `try...finally`. Dependencies are injected using `Annotated` and `Depends`.

```python
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

# Dependency function
async def common_parameters(
    q: Union[str, None] = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

# Using dependency in multiple endpoints
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"params": commons, "items": ["item1", "item2"]}

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"params": commons, "users": ["user1", "user2"]}

# Database dependency with cleanup
async def get_db():
    db = {"connection": "active"}
    try:
        yield db
    finally:
        db["connection"] = "closed"

@app.get("/query/")
async def query_data(db: Annotated[dict, Depends(get_db)]):
    return {"database": db, "data": "query results"}
```

---

### Create Basic FastAPI Application with GET Endpoints

Source: https://github.com/fastapi/fastapi/blob/master/README.md

This snippet demonstrates how to create a minimal FastAPI application in Python, defining `GET` endpoints for a root path and an item path with parameters. It includes both synchronous and asynchronous implementations for the same functionality, showing flexibility in handling I/O operations.

```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

### Define Path Operations with APIRouter in FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

Shows how to define path operations (routes) using an APIRouter instance in FastAPI. This allows grouping related endpoints, such as user-related operations, into a dedicated module.

```Python
from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def read_users():
    return {"message": "Users list"}


@router.post("/")
def create_user():
    return {"message": "Create user"}
```

---

### FastAPI: Reusing Annotated Dependencies in Path Operations

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to effectively reuse an `Annotated` dependency type alias (like `CurrentUser`) across multiple FastAPI path operation functions. This approach significantly reduces code duplication compared to explicitly using `Depends()` for each endpoint, while still providing full type-checking and editor support.

```python
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/items/")
def read_items(user: CurrentUser):
    ...


@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    ...


@app.get("/items/{item_id}")
def read_item(user: CurrentUser, item_id: int):
    ...


@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    ...
```

---

### Implement FastAPI PUT Endpoints for Updates (Python)

Source: https://context7.com/fastapi/fastapi/llms.txt

Shows how to create PUT endpoints to update existing resources. This example uses both path parameters to identify the resource and a Pydantic `BaseModel` to validate the request body containing the updated data, ensuring robust data handling.

```python
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item_name": item.name,
        "item_price": item.price,
        "is_offer": item.is_offer
    }
```

---

### Define FastAPI GET Endpoints (Python)

Source: https://context7.com/fastapi/fastapi/llms.txt

Illustrates defining GET endpoints to retrieve data. This includes examples for simple root endpoints, path parameters with type validation, query parameters with default values, and a combination of both, showcasing FastAPI's automatic request validation and response serialization.

```python
from typing import Union
from fastapi import FastAPI

app = FastAPI()

# Simple GET endpoint
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Path parameters with type validation
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Query parameters with defaults
@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Combined path and query parameters
@app.get("/items/{item_id}/details")
async def get_item_details(item_id: int, q: Union[str, None] = None):
    result = {"item_id": item_id}
    if q:
        result["q"] = q
    return result
```

---

### Importing FastAPI Request Parameter Functions

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/parameters.md

Demonstrates how to import all special functions for declaring request parameters directly from the 'fastapi' library. These functions are essential for defining how your API endpoints receive data.

```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

---

### Initialize FastAPI with Top-Level Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to initialize a FastAPI application with global dependencies that apply to all path operations. It defines an asynchronous dependency function and passes it to the `FastAPI` constructor's `dependencies` parameter to ensure it runs for every request.

```python
from fastapi import FastAPI, Depends


async def some_dependency():
    return


app = FastAPI(dependencies=[Depends(some_dependency)])
```

