from fastapi import FastAPI
from fastmcp import FastMCP
import math

# Create MCP server
mcp = FastMCP("strava")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return int(a + b)

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return int(a - b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return int(a * b)

@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)

@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    return int(a ** b)

@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    if a < 0:
        raise ValueError("Cannot take square root of negative number")
    return float(a ** 0.5)

@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    return float(a ** (1/3))

@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    if a < 0:
        raise ValueError("Cannot compute factorial of negative number")
    return int(math.factorial(a))

@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    if a <= 0:
        raise ValueError("Cannot take log of non-positive number")
    return float(math.log(a))

@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers division"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return int(a % b)

@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    return float(math.sin(a))

@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    return float(math.cos(a))

@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    return float(math.tan(a))

# Create ASGI app from MCP server
mcp_app = mcp.http_app(path='/mcp')

# Create FastAPI app with MCP lifespan
app = FastAPI(title="Strava Calculator API", lifespan=mcp_app.lifespan)

# Mount the MCP server
app.mount("/strava", mcp_app)

# Optional: Add some regular FastAPI endpoints
@app.get("/")
async def root():
    """Root endpoint showing available services"""
    return {
        "message": "Strava Calculator API",
        "services": {
            "regular_api": "http://localhost:8000/",
            "mcp_endpoint": "http://localhost:8000/strava/mcp/",
            "docs": "http://localhost:8000/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "strava-calculator"}

# Make sure your main.py has this at the bottom:
if __name__ == "__main__":
    import os
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")