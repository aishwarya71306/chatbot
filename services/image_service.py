from openai import OpenAI
from openai import APIConnectionError, APIError, APITimeoutError, AuthenticationError, RateLimitError


class ImageServiceError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


class ImageService:
    def __init__(self, config):
        self.config = config

    def generate_image(self, prompt):
        if not self.config.AI_API_KEY or self.config.AI_API_KEY == "your_api_key_here":
            raise ImageServiceError("Image service is not configured. Add a valid AI_API_KEY to .env.", 503)
        try:
            client_options = {"api_key": self.config.AI_API_KEY, "timeout": self.config.AI_TIMEOUT}
            if self.config.AI_BASE_URL:
                client_options["base_url"] = self.config.AI_BASE_URL
            client = OpenAI(**client_options)
            result = client.images.generate(model=self.config.IMAGE_MODEL, prompt=prompt, size="1024x1024", n=1)
            if not result.data or not result.data[0].url:
                raise ImageServiceError("The image provider returned no image.")
            return result.data[0].url
        except AuthenticationError as error:
            raise ImageServiceError("The AI API key was rejected. Check your .env configuration.", 502) from error
        except RateLimitError as error:
            raise ImageServiceError("The image provider rate limit was reached. Please try again shortly.", 429) from error
        except (APITimeoutError, APIConnectionError) as error:
            raise ImageServiceError("The image provider could not be reached. Please try again.", 504) from error
        except APIError as error:
            raise ImageServiceError("The image provider returned an error. Check the image model.", 502) from error
        except ImageServiceError:
            raise
        except Exception as error:
            raise ImageServiceError("Unable to generate an image right now.", 502) from error
