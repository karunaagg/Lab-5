import asyncio
from transport_company.tools.routing_tool import route_osrm
from transport_company.tools.poi_tool import search_pois

async def plan_parallel(origin: str, destination: str, purpose: str):
    """Run routing and POI search concurrently without blocking the event loop."""
    loop = asyncio.get_running_loop()
    r_task = loop.run_in_executor(None, route_osrm, origin, destination)
    p_task = loop.run_in_executor(None, search_pois, destination, purpose)
    routing, pois = await asyncio.gather(r_task, p_task)
    return {"routing": routing, "pois": pois}
