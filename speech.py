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
    speeches = []
    for speech in speech_start:
        speeches.append(split_protospeech(speech))
    return speeches

def get_speech_names(name_speech, names):
    words = name_speech.split(' ')
    return set(words).intersection(set(names))


def name_speech(data, names):
    speeches = read_speech(data)
    named_speeches = []
    for speech in speeches:
        speech_names = []
        for token in speech:
            if len(speech_names) > 0:
                break
            if (not token["isChar"]):
                speech_names = list(get_speech_names(token["txt"], names))
        name = None
        if len(speech_names) > 0:
            name = speech_names[0]
        named_speeches.append({ "speeker": name, "speech_tokens": speech})
    return named_speeches


# read_speech(read_hary_potter());
names = ["Harry", "Ron", "Hagrid"]

for a in name_speech(read_hary_potter(), names):
    print a