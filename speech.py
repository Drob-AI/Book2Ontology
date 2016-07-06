from dataReader import read_hary_potter

def split_protospeech(proto_speech):
    speech_tokens = proto_speech.split('"')
    speech_tokens = [x for x in speech_tokens if x]
    named_tokens = []
    for i in range(0, len(speech_tokens)):
        named_tokens.append({"txt": speech_tokens[i], "isChar": i % 2 == 0});
    return named_tokens

def read_speech(data):
    whole_data = reduce(lambda a,b: a + b, data)
    speech_start = whole_data.split('\n"')
    for speech in speech_start:
        print split_protospeech(speech)

read_speech(read_hary_potter());