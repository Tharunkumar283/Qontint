"""
Qontint — API Router
Aggregates all v1 API endpoints.
"""
from fastapi import APIRouter
from app.api.v1 import analyze, predict, generate, recommend, serp, graph, auth, youtube, export

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(analyze.router, tags=["Analysis"])
api_router.include_router(predict.router, tags=["Prediction"])
api_router.include_router(generate.router, tags=["Generation"])
api_router.include_router(recommend.router, tags=["Recommendations"])
api_router.include_router(serp.router, tags=["SERP"])
api_router.include_router(graph.router, tags=["Graph"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(youtube.router, tags=["YouTube"])
api_router.include_router(export.router, tags=["Export"])
