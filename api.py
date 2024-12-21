import asyncio
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from neo4j_controller import Neo4jApp
from config import DbConfig
from models import QueryModel

app = FastAPI()


@app.get("/")
async def root():
    """Перенаправляет на страницу с котиками."""
    return RedirectResponse(url="/TheCatsWillBeWellFed")


@app.get("/TheCatsWillBeWellFed")
async def well_fed_cats():
    """Возвращает GIF-файл."""
    gif_path = "wellfedcats.gif"
    if not os.path.exists(gif_path):
        return {"error": "GIF not found"}
    return FileResponse(gif_path, media_type="image/gif")


@app.post("/execute")
async def execute(raw_query: QueryModel):
    """
    Выполняет запрос к базе данных Neo4j.

    Args:
        raw_query (QueryModel): Запрос и параметры.

    Returns:
        list: Результаты выполнения запроса.
    """
    query = raw_query.query
    parameters = raw_query.args  # Получаем параметры запроса

    # Загружаем конфигурацию для подключения
    config = DbConfig.from_env(".env")

    # Открываем и закрываем драйвер только для текущего запроса
    async with Neo4jApp(
            url=config.db_url,
            user=config.user,
            password=config.password
    ) as neo4j_app:
        try:
            result = await neo4j_app.run_query(query, parameters)
            return {"status": "success", "data": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ошибка выполнения запроса: {str(e)}")


async def main():
    """Запускает сервер FastAPI."""
    config = uvicorn.Config(
        app,  # Передаем наше FastAPI приложение
        host="127.0.0.1",  # Слушаем на localhost
        port=8444,
        reload=True  # Перезагружать при изменениях
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
