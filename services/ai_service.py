from openai import OpenAI
from openai import APIConnectionError, APIError, APITimeoutError, AuthenticationError, RateLimitError

from prompts.system_prompt import build_messages


class AIServiceError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


class AIService:
    def __init__(self, config):
        self.config = config

    def generate_response(self, message, conversation):
        if not self.config.AI_API_KEY or self.config.AI_API_KEY == "your_api_key_here":
            raise AIServiceError("AI service is not configured. Add a valid AI_API_KEY to .env.", 503)
        try:
            client_options = {"api_key": self.config.AI_API_KEY, "timeout": self.config.AI_TIMEOUT}
            if self.config.AI_BASE_URL:
                client_options["base_url"] = self.config.AI_BASE_URL
            client = OpenAI(**client_options)
            result = client.chat.completions.create(
                model=self.config.AI_MODEL,
                messages=build_messages(message, conversation),
                temperature=0.7,
            )
            content = result.choices[0].message.content if result.choices else None
            if not content:
                raise AIServiceError("The AI returned an empty response.")
            return content.strip()
        except AuthenticationError as error:
            raise AIServiceError("The AI API key was rejected. Check your .env configuration.", 502) from error
        except RateLimitError as error:
            raise AIServiceError("The AI provider rate limit was reached. Please try again shortly.", 429) from error
        except (APITimeoutError, APIConnectionError) as error:
            raise AIServiceError("The AI provider could not be reached. Please try again.", 504) from error
        except APIError as error:
            raise AIServiceError("The AI provider returned an error. Check the model and provider settings.", 502) from error
        except AIServiceError:
            raise
        except Exception as error:
            raise AIServiceError("Unable to generate a response right now.", 502) from error
