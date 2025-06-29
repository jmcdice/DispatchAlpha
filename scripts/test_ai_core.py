import asyncio
from core_dispatch.services.ai_core import AICore


async def main():
    """
    Main function to test the AICore service.
    """
    print("Initializing AI Core...")
    ai_core = AICore()

    prompt = "What is the mission of Core Dispatch 2.0?"
    print(f"Sending prompt: '{prompt}'")

    response = ai_core.generate_text_response(prompt)

    if response:
        print("\nReceived response:")
        print("--------------------")
        print(response)
        print("--------------------")
    else:
        print("\nFailed to get a response from the AI core.")


if __name__ == "__main__":
    asyncio.run(main())

