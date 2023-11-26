# 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

from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

core_memory = ""

def get_prompt(user_prompt):
    global core_memory

    prompt = "[Previous interaction summary] {" + core_memory + "}\n"
    prompt += "[Prompt. You must answer this] " + user_prompt + "\n"
    prompt += "[Summarize] After answering the prompt, you must summarize this interaction along with the previous summary within 100 words " \
              "total. You must contain this summary inside the summary block: [Summary]{*here}. This is to preserve " \
              "memory.\n"
    prompt += "[Example] User: Hi! / GPT: Hello! How can I assist you?\n[Summary]{Basic greetings from user.}" + "\n"
    prompt += "[Language] If the user asks in Korean, you must answer + summarize in Korean. Likewise for English. " \
              "But keep [Tags] in English for consistency.\n"

    return prompt

def ask_GPT(user_prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content


def main():
    # used for testing
    global core_memory

    while True:

        user_prompt = input("input (type 'exit' to exit): ")
        if user_prompt == "exit":
            break

        response = ask_GPT(get_prompt(user_prompt))


        # Failsafe ###########################################################
        attempts = 1
        while ("{" not in response or "}" not in response) and attempts < 3:
            print("Error: Summary block not returned. Re-prompting...")
            response = ask_GPT(get_prompt(user_prompt))
            attempts += 1

        if attempts == 3:
            print("ERROR: Summary not included")
        ######################################################################

        print("Response: " + response)

        core_memory = response[response.index("{")+1:response.index("}")]
        print("Saved memory: " + core_memory)


# main()

def get_response(user_prompt):
    global core_memory

    response = ask_GPT(get_prompt(user_prompt))

    # Failsafe ###########################################################
    attempts = 1
    # This works assuming that { and } is only included at the summary block
    while ("{" not in response or "}" not in response) and attempts < 3:
        print("Error: Summary block not returned. Re-prompting...")
        response = ask_GPT(get_prompt(user_prompt))
        attempts += 1

    if attempts == 3:
        print("ERROR: Summary not included")
    ######################################################################

    # print("Response: " + response)

    core_memory = response[response.index("{") + 1:response.index("}")]
    # print("Saved memory: " + core_memory)

    # This works assuming that [ is only included at the summary block
    pure_response = response[:response.index("[")]

    return pure_response