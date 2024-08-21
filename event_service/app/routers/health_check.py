from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
from app.database import get_db
from fastapi import Depends

router = APIRouter()

@router.get("/health", summary="Health Check Endpoint", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    **Health Check Endpoint**

    This endpoint is used to check the health of the application.

    - **status**: Indicates the overall status of the application.
    - **db_status**: Shows the database connection status.
    - **error**: Provides error details if the application or database is unhealthy.

    Returns:
        - 200: Healthy status if the application and database are working properly.
        - 500: Unhealthy status if the application cannot connect to the database.
    """
    try:
        db.execute(sql_text("SELECT 1"))
        return {"status": "healthy", "db_status": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "unhealthy", "db_status": "disconnected", "error": str(e)}
        )
