# LLM Prompts Documentation
The Documentation outlines the prompts used with LLM in the Travel Assistant Chatbot

## System Prompt for travel Queries
#### Prompt:
You are a helpful travel assistant. For travel-related queries, provide clear, concise answers including passport requirements, visa requirements, additional documents and any other relevant information like: proof of accommodation, proof of sufficient funds, return ticket, travel insurance, and COVID-19 restrictions. Format your response in a structured way.

#### Purpose:
- Intruct lLLm to act as travel Assistant
- Responses should include travel specific information
- Ensure responses are well formatted in a consistent way


#### Example usage
- User input: "What documents do I need to travel to Malta?"
- The propmpt is prepared before being sent to OpenAI API
- Format the response before given back to the user.
```Example Output
  To travel to Malta, you will need the following documents:

  Visa

  Depending on your nationality, you may need a visa to enter Malta. Please check the visa requirements for your specific country.

  Passport

  Ensure your passport is valid for at least three months beyond your planned stay in Malta.

  Additional documents

  - Return flight ticket: Proof of your return journey.

  - Proof of accommodation: Hotel reservation or invitation letter from a host in Malta.

  - Travel itinerary: Details of your planned activities and places you intend to visit.

  - Sufficient funds: Evidence that you have enough money to cover your expenses during your stay.

  - Travel insurance: It is recommended to have travel insurance that covers medical expenses and repatriation.

  - Other documents: Depending on your circumstances, you may need additional documents such as a letter of invitation, proof of employment, or proof of enrollment in a study program.

  Ensure you have all the necessary documents in order before traveling to Malta to avoid any issues at immigration.
```

The prompt is defined in the `main.py` file within the `/api/chat/` endpoint.
The functon `format_travel_response` in the `utils.py` file formats the response to a disired output.
