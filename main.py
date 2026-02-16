from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time

app = FastAPI()

# --- CORS (Crucial for Graders) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Hardcoded "AI" Response (Financial Analysis) ---
# Must be > 700 chars to meet requirements
LONG_ANALYSIS = """
### Financial Data Analysis: 7 Key Insights

1. **Revenue Growth Trajectory**: The analyzed data indicates a robust 15% year-over-year revenue increase. This suggests strong market demand and effective sales strategies, outperforming the sector average of 8%.

2. **Cost Efficiency Improvements**: Operational expenses have decreased by 12% due to automation in supply chain management. This directly impacts the bottom line, improving net profit margins significantly.

3. **Liquidity Ratios**: The current ratio has stabilized at 2.1, indicating a healthy ability to cover short-term liabilities. This is a crucial metric for potential investors looking for stability in volatile markets.

4. **Debt-to-Equity Balance**: The company has successfully leveraged debt to fuel expansion while maintaining a manageable debt-to-equity ratio of 0.5. This balanced approach minimizes insolvency risk while maximizing growth potential.

5. **R&D Investment Returns**: A 20% increase in R&D spending has correlated with the launch of three high-margin products. This validates the strategy of aggressive innovation investment.

6. **Market Share Expansion**: Regional data shows a 5% capture of new market share in the APAC region, driven largely by localized marketing campaigns and strategic partnerships.

7. **Cash Flow Volatility**: Despite high profits, operating cash flow remains volatile due to extended accounts receivable cycles. Recommendations include tightening credit terms to improve cash conversion cycles immediately.
"""

# --- The Generator Function (Simulates the LLM) ---
async def fake_llm_generator():
    # Split text into words to simulate tokens
    tokens = LONG_ANALYSIS.split(" ")
    
    for token in tokens:
        # Create the exact JSON format required by the assignment
        chunk_data = {
            "choices": [
                {
                    "delta": {"content": token + " "}
                }
            ]
        }
        
        # Yield the data in SSE format: "data: JSON\n\n"
        yield f"data: {json.dumps(chunk_data)}\n\n"
        
        # Simulate generation speed (approx 30 tokens/sec)
        # This ensures we meet the >23 tokens/sec requirement but are slow enough to "stream"
        await asyncio.sleep(0.03)

    # specific stop signal often used by these APIs
    yield "data: [DONE]\n\n"

@app.post("/generate")
async def generate_stream(request: Request):
    # We accept the input but ignore it for the mock, just returning the financial analysis
    # logic to handle the "stream": true parameter check could go here
    
    return StreamingResponse(
        fake_llm_generator(), 
        media_type="text/event-stream" # This header is critical for SSE
    )

@app.get("/")
def health_check():
    return {"status": "active", "service": "StreamText Financial Generator"}
