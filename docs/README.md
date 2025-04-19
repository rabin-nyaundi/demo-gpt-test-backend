## Documentation for the Travel Assistant

The frontend is located here:

Built with NextJS(frontend) and FastAPI(backend)

### Prerequisites

* Node.js: v18 or higher
* Python: 3.10 or higher
* OpenAI API Key: For LLM Integration

### Setup Backend

1. Clone the repository.

  + cd `pawait-gpt-backend/`

2. Create virtual environment

    - `pyhton -m venv .venv`

  + Activate the environment
  + `source .venv/bin/activate`

3. Copy `.env.example` to `.env`

  + Fill the OpenAI API key value

4. Run the application
 `vicorn main:app --reload`

  

### Setup Frontend

1. Clone the repository.

  + cd `pawait-gpt/`

2. Install dependencies
  + `npm install` or `yarn install` or `pnpm install`

3. Copy `.env.example` to `.env.local`

  + Fill the OpenAI API key value

  

```bash
    NEXT_PUBLIC_ENVIRONMENT=development
    NEXT_PUBLIC_DEV_BACKEND_URL=http://localhost:8000/api
    NEXT_PUBLIC_PROD_BACKEND_URL=https://{your url}/api
  ```

3. Run the application
  + `npm run dev` or `yarn dev` or `pnpm dev`

  
4. Open your browser and navigate to `http://localhost:3000` to see the application in action.
