import openai
import asyncio
from typing import List, Dict

class LLMHandler:
    def __init__(self, api_key):
        openai.api_key = api_key

    async def generate_response(
        self,
        message,
        persona,
        memories: List,
        context: List[Dict],
        knowledge_base: List,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        try:
            # Build the additional prompt with memory and context information
            additional_prompt = f"""
            You’re an advanced conversational agent with access to user preferences and key goals, which you may use only to make responses more relevant. Avoid unnecessary reliance on memories—prioritize what the user is asking about now.
            This is what you know about the user’s preferences and goals: {memories}
            Remember: only refer to memories when they clearly enhance the immediate conversation. Focus on the user's current needs, and communicate in a human-like, user-aligned style.
            **Current Conversation Context**: {context}
            **Your Knowledge Base**: {knowledge_base}"""

            # Combine persona system prompt with additional prompt
            combined_preamble = f"{persona.system_prompt} , \n{additional_prompt}"
            messages = [
                {"role": "system", "content": combined_preamble},
                {"role": "user", "content": message.content}
            ]

            # Run the OpenAI API request asynchronously
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: openai.chat.completions.create(
                    model="gpt-3.5-turbo",  # Change to "gpt-4" if desired and available
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )

            # Extract and return the response text
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request."