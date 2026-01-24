import time
import logging
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - Completed in {process_time:.4f}s")
        response.headers["X-Process-Time"] = str(process_time)
        return response

def setup_middleware(app):
    # add Logging Middleware
    app.add_middleware(LoggingMiddleware)
    
    # add CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
