from google.adk.agents import Agent
from transport_company.tools.config_tool import get_config
from transport_company.tools.routing_tool import route_osrm
from transport_company.tools.poi_tool import search_pois
from transport_company.tools.cost_tool import estimate_cost
from transport_company.tools.parallel_tools import plan_parallel
from transport_company.tools.schema_tool import validate_final_json
# from transport_company.callbacks.monitor import MonitorCallback
from transport_company.review_agent import reviewer_agent

INSTRUCTION = (
  "You are a transport planner. Parse inputs: origin, destination, vehicle, purpose, days.\n"
  "Use tools to gather facts and compute costs:\n"
  "- route_osrm(origin, destination)\n"
  "- search_pois(destination, purpose)  # only when purpose=='tourism'\n"
  "- estimate_cost(distance_km, days, vehicle, purpose)\n"
  "You may call plan_parallel(origin, destination, purpose) to do routing+POIs concurrently.\n"
  "Maintain short memory summaries in session state.\n"
  "Return a FINAL JSON exactly with keys: {spec, routing, pois, cost, itinerary, notes}.\n"
  'spec: {origin, destination, vehicle, purpose, days}; routing: {distance_km, duration_hr};\n'
  'pois: list[{name, snippet}]; cost: {fuel, distance_charge, tolls, driver, night_halt, food, misc, total};\n'
  "itinerary: list of 1–5 concise day strings; notes: brief safety/assumptions.\n"
  "After forming JSON, call validate_final_json(json_obj). Finally, ask reviewer_agent to reply 'OK' or issues."
)

root_agent = Agent(
  name="transport_company",
  model="gemini-2.0-flash",
  description="Transport planner with memory, parallel tools, validation, and structured JSON.",
  instruction=INSTRUCTION,
  tools=[get_config, route_osrm, search_pois, estimate_cost, plan_parallel, validate_final_json],
  # callbacks=[MonitorCallback()],
  # subagents=[reviewer_agent],
)
