import httpx

async def get_artwork_from_api(external_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)

            if response.status_code == 200:
                data = response.json().get("data", {})

                # Формуємо URL зображення, якщо воно є
                image_id = data.get("image_id")
                image_url = None
                if image_id:
                    image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

                return {
                    "external_id": external_id,
                    "title": data.get("title", "No Title"),
                    "artist": data.get("artist_display", "Unknown Artist"),
                    "image_url": image_url
                }
        except Exception as e:
            print(f"API Error: {e}")
            return None
    return None