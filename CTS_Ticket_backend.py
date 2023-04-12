
import openai
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
r = sr.Recognizer()
openai.api_key = ""


def audio_to_string(audio_file):# openai audio to string is better but costs some money ish, use if necesary
    audio_file = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)['text']
    return transcript


def audio_from_file(file): # opensource audio to string, works alright

    with sr.AudioFile(file) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return (text)


def audio_from_microphone(garbage):
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            print('start')
            audio_data = r.listen(source, timeout=10000,phrase_time_limit=None)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data, )
            return (text)


class Info_From_File:


    def __init__(self, audio_file,function_for_audio):
        txt = function_for_audio(audio_file)
        self.function_for_audio = function_for_audio
        print(txt)
        self.all = []
        self.tokenized = sent_tokenize(txt)
        self.question_answer = []
        self.questions_asked = []
        self.location = []
        self.Grammer = []
        self.name = []
        for i in range(len(self.tokenized)):
            # Word tokenizers is used to find the words
            # and punctuation in a string
            wordsList = nltk.word_tokenize(self.tokenized[i])

            # removing stop words from wordList

            #  Using a Tagger. Which is part-of-speech
            # tagger or POS-tagger.
            self.tagged = nltk.pos_tag(wordsList)
            self.all.extend(self.tagged[::])
            if self.analyze(self.tagged):
                self.Grammer.append(self.analyze((self.tagged)))
            self.location.extend(self.get_location(self.tagged))
            did_questions_increment = len(self.questions_asked)
            self.questions_asked.extend(self.get_questions(self.tagged))
            if did_questions_increment != len(self.questions_asked) and i + 1 < len(self.tagged):
                self.question_answer.append(nltk.pos_tag(nltk.word_tokenize(self.tokenized[i + 1])))
            self.name.extend(self.get_name(self.tagged))
            # print(tagged)
            #self.grab_sandwitch('NN','VBZ',self.tagged)
            #self.grab_bagel('N','VB','VBG',self.tagged)
    def get_words(self,tagged):
        return [e[0] for e in tagged]

    def get_location(self,tagged):
        location = []
        #most_recent_noun = [i for i in range(len(tagged)) if 'N' in tagged[i][1]]
        location.extend(tagged[k - 1:k + 1] for k in range(len(tagged)) if 'CD' in tagged[k][1])
        if location:
            if self.function_for_audio is audio_to_string:
                return (location)
            else:
                return location[0]
        return location

    def get_questions(self,tagged):

        question = []

        for w in tagged:

            if '?' in w[0]:
                question.extend(tagged)
        # print(a,b)
        return question

    def get_name(self,tagged):
        name = []
        name.extend(tagged[k:k + 2] for k in range(len(tagged)) if 'prof' in tagged[k][0].lower() or 'mr' \
                    in tagged[k][0].lower() or 'ms' in tagged[k][0].lower() or 'mrs' in tagged[k][0].lower())
        if self.function_for_audio is audio_to_string:
            return name
        else:
            return name[0]

    def get_in_class(self,tagged):
        inclass = []
        inclass.extend(tagged[k:k + 3] for k in range(len(tagged)) if 'class' == tagged[k][0].lower() or 'lecture' \
                    == tagged[k][0].lower() or 'instruction' == tagged[k][0].lower() or 'lab' == tagged[k][0].lower())
        if self.function_for_audio is audio_to_string:
            return inclass
        else:
            return inclass[0]

    def grab_sandwitch(self,ends,middle,tagged):
        end_indexes = [i for i in range(len(tagged)) if ends in tagged[i][1] ]
        middle_indexes = [i for i in range(len(tagged)) if middle in tagged[i][1]]
        watch_this = end_indexes + middle_indexes
        watch_this.sort()
        watch_this = [[watch_this[e-1],watch_this[e+1]] for e in range(len(watch_this)) if watch_this[e] in middle_indexes and e-1 >0 and e+1 <len(watch_this)]
        #print([[tagged[e[0]:e[1]]] for e in watch_this])

    def grab_bagel(self, start, middle, end, tagged):
        middle_index = [i for i in range(len(tagged)) if middle in tagged[i][1] ]
        grab = []
        for mid in middle_index:
            for back in range(4):
                if start in tagged[mid-back][1]:
                    for forward in range(4):
                        if end in tagged[mid+forward][1] or start in tagged[mid+forward][1]:
                            grab.extend(tagged[back:forward])
       # print(grab)
    def analyze(self,sentence):
        noun_to_article = []
        for word_index in range(len(sentence)):
            if 'VB' in (sentence[word_index][1]):
                noun_to_article.extend(
                    [sentence[e::] for e in range(len(sentence[0:word_index])) if 'N' in sentence[e][1]])
                # print(sentence[word_index - 1:word_index
        if noun_to_article:
            return (noun_to_article[-3])
        return noun_to_article
    def __str__(self):
        return 'Closing Summary: ' + str([self.get_words(g) for g in self.Grammer]) + 'Location: ' + str(self.get_words(self.location)) \
        + 'Name: ' + str(self.get_words(self.get_name(self.tagged))) +'In Class: ' + str(str(self.get_words(self.get_in_class(self.tagged))))

#ticket1 = Info_From_File("Peet's Coffee.m4a",audio_to_string)
#print(ticket1)
ticket2 = Info_From_File('Peet_s-Coffee-_1_.wav',audio_from_file)
print(ticket2)
