import aiohttp
import ujson
import os
import dotenv
dotenv.load_dotenv()

BASE_URL = os.getenv("API_URL")
ENDPOINT = "/ask/"

async def ask(logger, prompt):
    # Create the payload according to the Query object schema
    payload = {
        "query": prompt,
        "category": "message",
        "attachment": [],  # Empty list instead of None
        "show_thoughts": False
    }
    
    try:
        # Create a session with the JSON serializer
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            # Now try the proper POST endpoint with the query in the URL path
            # The API expects: POST /ask/{query} with Query object in the body
            post_url = f"{BASE_URL}{ENDPOINT}{prompt}"
            logger.info(f"Trying POST to URL: {post_url}")
            
            try:
                headers = {"Content-Type": "application/json"}
                async with session.post(post_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        logger.info(f"API response (POST): {response_data}")
                        
                        # Make sure we're returning a dictionary
                        if isinstance(response_data, dict):
                            # If the API returns a "reply" field, use that as the response
                            if "reply" in response_data:
                                return {"response": response_data["reply"]}
                            # Return the full dictionary as-is
                            return response_data
                        else:
                            # If it's not a dictionary, wrap it in one
                            return {"response": str(response_data)}
                    else:
                        status = response.status
                        text = await response.text()
                        logger.error(f"POST failed with status {status}: {text}")
                        return {"error": f"API returned status {status}: {text}"}
            except Exception as e:
                logger.error(f"Error with POST request: {e}")
                return {"error": f"POST request failed: {str(e)}"}
                
    except Exception as e:
        logger.error(f"Session creation error: {e}")
        return {"error": f"Failed to create session: {str(e)}"}