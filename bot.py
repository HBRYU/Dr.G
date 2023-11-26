import gptAPI

try:
    import yaml
except:
    import os

    os.system("pip install pyyaml")
    os.system("pip install --upgrade pyyaml")
    import yaml

try:
    file = open("yml/greetings.yml")
    testing_file = yaml.safe_load(file)
    file.close()
except:
    os.system("pip install --upgrade pyyaml")
    import yaml


# Memory testing
# print(gptAPI.get_response("Hello"))
# print(gptAPI.get_response("Would you say the glass is half full or half empty?"))
# print(gptAPI.get_response("What did we talk about?"))

def get_yaml_prompts(yaml_file):
    return [pair[0] for pair in yaml_file['conversations']]


def get_yaml_responses(yaml_file):
    return [pair[1] for pair in yaml_file['conversations']]

def get_prompts_and_responses(directory):
    file = open(directory)
    loaded_file = yaml.safe_load(file)
    prompts = get_yaml_prompts(loaded_file)
    resposes = get_yaml_responses(loaded_file)
    file.close()
    return dict({'prompts': prompts, 'responses': resposes})


greetings = get_prompts_and_responses("yml/greetings.yml")
address = get_prompts_and_responses("yml/address.yml")
inquiry = get_prompts_and_responses("yml/inquiry.yml")
bye = get_prompts_and_responses("yml/bye.yml")

def send_text(text):
    topic = ""
    message = ""
    response = ""
    #1. Simple Yaml prompt
    if text in greetings['prompts']:
        topic = "greetings"
        response = greetings['responses'][greetings['prompts'].index(text)]
    elif text in address['prompts']:
        topic = "address"
        response = address['responses'][address['prompts'].index(text)]
    elif text in inquiry['prompts']:
        topic = "inquiry"
        response = inquiry['responses'][inquiry['prompts'].index(text)]
    elif text in bye['prompts']:
        topic = "bye"
        response = bye['responses'][bye['prompts'].index(text)]
    else:
        #2. Inquire GPT-4

        with open('knowledge.txt', 'r', encoding='utf-8') as knowledge:
            response = gptAPI.get_response(text, knowledge.read())
        response += "\n(GPT-4)"

    return response
