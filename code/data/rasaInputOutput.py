from rasa.core.agent import Agent
from pathlib import Path
import asyncio
import time
import os
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import random



async def run_chatbot(agent, input_file_path):
    # Load the Rasa agent
    

    # Read input file and process messages
    with open(input_file_path, "r", encoding="utf-8") as file:
        messages = file.readlines()

    # Process each message and obtain responses
    all_responses = []
    for message in messages:
        response = await agent.handle_text(message.strip())
        responses = [r.get('text') for r in response]
        all_responses.extend(responses)
    return all_responses



def get_agent(name):
    path = "code/data/"+name+".tar.gz"
    # Add paths using get_validated_path or direct string paths
    model = Path(path).expanduser()  # Path to the model
    agent =  Agent.load(model_path=model)
    return agent

def get_sentence(agent, input):
    start_time = time.time()
    # Generate the responses using asyncio
    loop = asyncio.get_event_loop()
    chatbot_responses = loop.run_until_complete(run_chatbot(agent, input))
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    response_string = " ".join(chatbot_responses)

    return response_string.replace(" ", "_")





def retrieve_sentence(voice_name, sentence):
    file_path = os.path.join('code/data/voices/', voice_name, sentence + '.wav')
    print(file_path)
    if not os.path.exists(file_path):
        print("do not exist")
        return None
    with open(file_path, 'rb') as file:
        audio_data = file.read()
        print("trouvé")
        audio_segment = AudioSegment.from_wav(BytesIO(audio_data))
        play(audio_segment)
    return audio_data


#### Carefull!!! need to remind to put it on the final file
def generate_voice_order():
    voices_name = ["william","megan","pixie","robot"]
    random.shuffle(voices_name)
    return voices_name


# sentence = get_sentence(get_agent("model_background"))
# print("phrase : ",sentence)
# voices_order = generate_voice_order()
# cpt = 0

# retrieve_sentence(voices_order[cpt],sentence)
# print(new_line)
# if new_line[:-1]=="Thank_you_for_your_answers._Are_you_ready_for_the_marketing_interview?":
#     cpt+=1
# elif new_line[:-1]=="Thank_you_for_your_answers._Are_you_ready_for_the_financial_interview?":
#     cpt+=1
# elif new_line[:-1]=="Thank_you_for_your_answers._Are_you_ready_for_the_last_interview,_the_medical_one?":
#     cpt+=1
# print(cpt)
