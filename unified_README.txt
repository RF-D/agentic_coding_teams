
# UnifiedApis Class

The `UnifiedApis` class provides a unified interface for interacting with various AI providers (OpenAI, Anthropic, and OpenRouter).

## Key Attributes

- `provider`: The AI service provider (e.g., "openai", "anthropic", "openrouter")
- `model`: The specific AI model to use
- `json_mode`: Whether to return responses in JSON format (OpenAI only)
- `stream`: Whether to stream the response
- `use_async`: Whether to use asynchronous methods
- `max_history_words`: Maximum number of words to keep in conversation history
- `max_words_per_message`: Maximum words per message (if set)
- `use_cache`: Whether to use caching (gpt-4o-2024-08-06 only)

## Main Methods

### Initialization

- `__init__()`: Initializes the UnifiedApis object with specified parameters
- `_get_api_key()`: Retrieves the API key for the selected provider
- `_initialize_client()`: Sets up the appropriate client based on the provider and async setting

### Message Handling

- `set_system_message()`: Sets the system message for the conversation
- `add_message()`: Adds a message to the conversation history
- `clear_history()`: Clears the conversation history
- `trim_history()`: Removes old messages to stay within `max_history_words`

### Chat Interaction

- `chat()`: Sends a user message and gets a response
- `get_response()`: Generates a response from the AI model

### Asynchronous Versions

Async versions of the main methods are available with `_async` suffix (e.g., `chat_async()`, `get_response_async()`).

## Usage Notes

- Set `use_async=True` when using asynchronous methods
- Set `json_mode=True` for JSON responses (OpenAI only)
- Describe the desired JSON structure in the system message when using JSON mode
- For Claude (Anthropic), instruct the model to return structured content in `<>` tags for easier parsing