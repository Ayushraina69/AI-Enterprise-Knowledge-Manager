import asyncio

from agents import Runner

from agent_modules.orchestrator_agent import orchestrator_agent


async def main():

    try:
        question = input(
            "Ask the Enterprise Knowledge Manager: "
        ).strip()

        if not question:
            print("\nPlease enter a valid question.")
            return

        result = await Runner.run(
            orchestrator_agent,
            question
        )

        print("\nAI RESPONSE")
        print("=" * 60)

        if result.final_output:
            print(result.final_output)
        else:
            print(
                "Sorry, I could not generate a response."
            )

    except KeyboardInterrupt:
        print("\n\nProgram stopped by user.")

    except Exception as error:
        print(
            "\nAn error occurred while processing "
            "your request."
        )
        print(f"Error details: {error}")


if __name__ == "__main__":
    asyncio.run(main())
    