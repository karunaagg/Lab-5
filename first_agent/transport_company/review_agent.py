from google.adk.agents import Agent

reviewer_agent = Agent(
  name="reviewer",
  model="gemini-2.0-flash",
  description="Validator that sanity-checks the final JSON.",
  instruction=(
    "Input is a JSON with keys spec, routing, pois, cost, itinerary, notes.\n"
    "Check: days>=1; distance_km>0; total ≈ sum of parts; POIs only for tourism; night_halt>0 if days>1.\n"
    "Reply ONLY 'OK' or a short bullet list of concrete issues."
  ),
)
