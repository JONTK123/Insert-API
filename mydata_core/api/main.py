"""
FastAPI application for data generation API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mydata_core.core.models import GenerationRequest, GenerationResponse
from mydata_core.core.generator import generate_and_insert

app = FastAPI(
    title="MyData Synthetic Data Generation API",
    description="API for generating and inserting synthetic data into PostgreSQL and MongoDB databases",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "MyData Synthetic Data Generation API",
        "version": "0.1.0",
        "description": "Generate and insert synthetic data into PostgreSQL and MongoDB",
        "endpoints": {
            "POST /generate": "Generate and insert synthetic data",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate", response_model=GenerationResponse)
async def generate_data(request: GenerationRequest):
    """
    Generate and insert synthetic data into the specified database.
    
    Args:
        request: Generation request with database connection and entity specifications
        
    Returns:
        Generation response with insertion counts and status
    """
    try:
        response = generate_and_insert(request)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.message)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
