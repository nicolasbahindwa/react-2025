import uvicorn
import logging

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("uvicorn.error")
    
    # Configure reload settings
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_delay=0.25,  # Reduce default reload delay
        reload_includes=["*.py", "*.json", "*.yaml"],  # Specify files to watch
        reload_excludes=[".*", "*.pyc", "__pycache__"],  # Exclude unnecessary files
        workers=1,  # Use single worker in development
        log_level="debug"
    )