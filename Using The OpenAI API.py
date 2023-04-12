import openai
openai.api_key = ""


def audio_to_string(audio_file):
    audio_file = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)['text']
    return transcript

class Memory:


    def __init__(self, information):
        self.transcript = audio_to_string(information)

        self. prompt =  'make a table of the following, do not make a new line' + self. transcript + '| Location | name | Issue | In class | Help sent'
        self.response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.prompt,
            temperature=0,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        text = ( self.response['choices'][0]['text'])
        text = text.split('|')
        text = [s for s in text if s.isalnum() or " " in s and s!= ' ']
        self.all = text
        self.location = text[0]
        self.professor = text[1]
        self.problem = text[2]
        self.in_class = text[3]
        self.runner_sent = text[4]


    def __str__(self):
        return f"| Location: {self.location} | name: {self.professor} | Issue: {self.problem} | In class: {self.in_class} | Help sent: {self.runner_sent} |all_info {self.all}"


ticket1 = Memory("Peet's Coffee.m4a")

print(ticket1)