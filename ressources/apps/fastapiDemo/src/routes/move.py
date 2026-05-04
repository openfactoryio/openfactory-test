from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/move")
async def move(x: float, y: float, request: Request):
    app = request.app.state.ofa_app
    app.move_axis(x, y)
    return {"message": "moving"}
