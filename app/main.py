from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.database.db import init_db
from app.api import You, faculty, courses, enrollments
from app.utils.logger import get_logger

init_db()
logger = get_logger()

app = FastAPI(
    title="CampusHub ERP",
    version="1.0.0",
    description="College Management System backend",
    docs_url=None,
)

for module in (You, faculty, courses, enrollments):
    app.include_router(module.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    """Serve Swagger UI with a restrained, neutral colour palette."""
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
    )
    html = response.body.decode("utf-8")
    custom_css = """
    <style>
      .swagger-ui {
        color: #252a31;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .swagger-ui .info { margin: 28px 0 22px; }
      .swagger-ui .info .title { color: #1f2937; font-weight: 650; }
      .swagger-ui .opblock,
      .swagger-ui .opblock.opblock-get,
      .swagger-ui .opblock.opblock-post,
      .swagger-ui .opblock.opblock-put,
      .swagger-ui .opblock.opblock-delete,
      .swagger-ui .opblock.opblock-patch {
        background: #ffffff !important;
        border: 1px solid #d8dde5 !important;
        border-radius: 6px;
        box-shadow: none !important;
        margin-bottom: 10px;
      }
      .swagger-ui .opblock .opblock-summary {
        padding: 5px 8px;
        border-color: #e5e7eb !important;
      }
      .swagger-ui .opblock .opblock-summary-method {
        background: #e9edf2 !important;
        color: #344054 !important;
        text-shadow: none !important;
        border-radius: 3px;
        box-shadow: none !important;
      }
      .swagger-ui .opblock .opblock-summary-description,
      .swagger-ui .opblock .opblock-summary-path,
      .swagger-ui .opblock .opblock-summary-path__deprecated {
        color: #344054 !important;
      }
      .swagger-ui .opblock-tag {
        color: #252a31;
        border-bottom: 1px solid #e5e7eb;
      }
      .swagger-ui .btn {
        border-radius: 5px;
        box-shadow: none;
      }
      .swagger-ui input,
      .swagger-ui select,
      .swagger-ui textarea {
        border-radius: 4px;
      }
      .swagger-ui .scheme-container {
        padding: 14px 0;
        box-shadow: none;
        background: #f8fafc;
      }
    </style>
    """
    html = html.replace("</head>", custom_css + "</head>")
    return HTMLResponse(content=html, status_code=response.status_code)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    """Serve the CampusHub ERP overview dashboard."""
    dashboard = Path(__file__).parent / "templates" / "dashboard.html"
    return HTMLResponse(dashboard.read_text(encoding="utf-8"))
