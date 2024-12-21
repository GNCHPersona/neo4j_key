from neo4j import AsyncGraphDatabase

class Neo4jApp:
    def __init__(self, url, user, password):
        self.driver = AsyncGraphDatabase.driver(url, auth=(user, password))

    async def close(self):
        """Закрывает драйвер."""
        await self.driver.close()


    async def is_open(self):
        """Проверяет, открыт ли драйвер."""
        return self.driver.session().closed is False

    async def run_query(self, query, parameters=None):
        """Выполняет запрос к базе данных."""
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            return [record async for record in result]

    async def __aenter__(self):
        """Инициализация контекстного менеджера."""
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Закрытие драйвера при выходе из контекста."""
        await self.close()
