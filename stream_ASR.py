####################   Import   ##########################
import queue
import re
import sys
import pyaudio
from google.cloud import speech
from google.protobuf import duration_pb2
import asyncio
import rasaInputOutput


####################   Global parameters   ##############
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


####################   Class setup   ####################

#Class inspired by the Google tutorial code
class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # Google advice of set up
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        """Closes the stream, regardless of whether the connection was lost or not."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ) -> object:
        """Continuously collect data from the audio stream, into the buffer.

        Args:
            in_data: The audio data as a bytes object
            frame_count: The number of frames captured
            time_info: The time information
            status_flags: The status flags

        Returns:
            The audio data as a bytes object
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Generates audio chunks from the stream of audio data in chunks.

        Args:
            self: The MicrophoneStream object

        Returns:
            A generator that outputs audio chunks.
        """
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


####################   Functions   ####################
def listen_print_loop(responses: object) -> str:
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.

    Args:
        responses: List of server responses

    Returns:
        The transcribed text.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

            # # Write to the overwrite file
            # with open("temp_file.txt", "w") as overwrite_file:
            #     overwrite_file.write(transcript)

            # # Write to the concatenating file
            # with open("full_script.txt", "a") as concatenate_file:
            #     concatenate_file.write(transcript)

        else:
            # print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

            # # Write to the overwrite file
            # with open("temp_file.txt", "w") as overwrite_file:
            #     overwrite_file.write(transcript)

            # # Write to the concatenating file
            # with open("full_script.txt", "a") as concatenate_file:
            #     concatenate_file.write(transcript)

            return transcript




def main() -> None:
    """Transcribe speech from audio file."""
    language_code = "en-GB"  
    # set up of the recording
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        rep = listen_print_loop(responses)
        # print(rep)
    return rep



####################   Script   ####################
if __name__ == "__main__":
    liste = rasaInputOutput.generate_voice_order()
    answer_of_rasa = ""
    with open('code/data/full_script.txt', 'w') as fichier:
        for el in liste : 
            fichier.write(el)
            fichier.write(" ")
        fichier.write("\n")
    background_model = rasaInputOutput.get_agent("model_background")
    answer_of_rasa = rasaInputOutput.get_sentence(background_model,"code/data/testRasa")
    rasaInputOutput.retrieve_sentence(liste[0], answer_of_rasa)
    while answer_of_rasa != "That_is_great,_as_you_should_be_aware,_this_job_is_for_people_with_a_technical_background.":
        speech_live = main()
        print(speech_live)
        with open("code/data/last_answer.txt", 'w') as fichier:
            fichier.write(speech_live)
        with open('code/data/full_script.txt', 'a') as fichier:
            fichier.write(answer_of_rasa)
            fichier.write("\n")
            final_sentence = speech_live + "\n\n"
            fichier.write(final_sentence)
        answer_of_rasa = rasaInputOutput.get_sentence(background_model,"code/data/last_answer.txt")
        print("################### answer : ", answer_of_rasa)
        rasaInputOutput.retrieve_sentence(liste[0], answer_of_rasa)

       


        


        