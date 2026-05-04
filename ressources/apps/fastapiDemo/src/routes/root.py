from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def root(request: Request):
    app = request.app.state.ofa_app
    return {"status": app.status.value}
