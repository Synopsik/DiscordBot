import aiohttp
import ujson

BASE_URL = "http://100.69.131.125:8000"
ENDPOINT = "/ask/"


async def ask(prompt, logger, show_thoughts=False):
    # Create the payload according to the Query object schema
    payload = {
        "query": prompt,
        "category": "message",
        "attachment": None,
        "show_thoughts": show_thoughts
    }

    try:
        # Create a session with the JSON serializer json_serialize=ujson.dumps
        async with aiohttp.ClientSession() as session:
            # Use the simpler endpoint URL without the path parameter
            post_url = f"{BASE_URL}{ENDPOINT}"
            logger.info(f"Trying POST to URL: {post_url}")

            try:
                headers = {"Content-Type": "application/json"}
                logger.info(f"Sending payload: {payload}")
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
                    elif response.status == 500:
                        status = response.status
                        text = await response.text()
                        logger.error(f"POST failed with status {status}: {text}")
                        return {"error": f"API returned status {status}: {text}"
                                         f"Check to see if Ollama server is running."}
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