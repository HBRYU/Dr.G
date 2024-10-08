# 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
try:
    from openai import OpenAI

except:
    import os
    os.system("pip install openai")
    from openai import OpenAI




client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

core_memory = ""

def generate_prompt(user_prompt, knowledge_string):
    global core_memory

    prompt = "[Here's your background knowledge:]\n" + knowledge_string + "\n"
    prompt += "[Previous interaction summary] {" + core_memory + "}\n"
    prompt += "[Prompt. You must answer this] " + user_prompt

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


# def main():
#     # used for testing
#     global core_memory
#
#     while True:
#
#         user_prompt = input("input (type 'exit' to exit): ")
#         if user_prompt == "exit":
#             break
#
#         response = ask_GPT(generate_prompt(user_prompt))
#
#         # Failsafe ###########################################################
#         # attempts = 1
#         # while ("{" not in response or "}" not in response) and attempts < 3:
#         #     print("Error: Summary block not returned. Re-prompting...")
#         #     response = ask_GPT(generate_prompt(user_prompt))
#         #     attempts += 1
#         #
#         # if attempts == 3:
#         #     print("ERROR: Summary not included")
#         ######################################################################
#
#         print("Response: " + response)
#
#         core_memory = response[response.index("{")+1:response.index("}")]
#         print("Saved memory: " + core_memory)


# main()

def get_response(user_prompt, knowledge):
    global core_memory

    generated_prompt = generate_prompt(user_prompt, knowledge)

    response = ask_GPT(generated_prompt)

    summary_prompt = generated_prompt + "\nResponse: " + response + "\n\nSummarize this interaction within 100 words."

    core_memory = ask_GPT(summary_prompt)

    print("Saved memory: " + core_memory)

    return response