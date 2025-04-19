## Documentation for the Travel Assistant

The frontend is located here:

Built with NextJS(frontend) and FastAPI(backend)

### Prerequisites

* Node.js: v18 or higher
* Python: 3.10 or higher
* OpenAI API Key: For LLM Integration

### Setup Backend

1. Clone the repository.

    - cd `pawa-it-gpt-test-backend/`

2. Create virtual environment

    - `pyhton -m venv .venv`

3. Activate the environment
    - `source .venv/bin/activate`

4. Copy `.env.example` to `.env`

    - Fill the OpenAI API key value

5. Add Redis Host, and username for rate limiting configs or comment the ratelimitting decorator
    ```bash
        REDIS_PASSWORD=secret
        REDIS_HOST=host
        REDIS_USERNAME=user
    ```

    or comment

    ```bash
        @app.post("/api/chat", response_model=ChatResponse)
        @rate_limiter(max_calls=1, time_frame=20)
        async def chat(request: Request,payload: ChatRequest):
    ```

6. Run the application
 `vicorn main:app --reload`



### Setup Frontend

1. Clone the repository.

    - cd `pawait-gpt/`

2. Install dependencies
    - `npm install` or `yarn install` or `pnpm install`

3. Copy `.env.example` to `.env.local`

```bash
  NEXT_PUBLIC_ENVIRONMENT=development
  NEXT_PUBLIC_DEV_BACKEND_URL=http://localhost:8000/api
  NEXT_PUBLIC_PROD_BACKEND_URL=https://{your url}/api
```

3. Run the application
    - `npm run dev` or `yarn dev` or `pnpm dev`


4. Open your browser and navigate to `http://localhost:3000` to see the application in action.
