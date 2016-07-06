from dataReader import read_hary_potter
from dataOperations import person_list

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

def get_speech_name(name_speech, names):
    words = name_speech.split(' ')
    for name in names:
        name_parts = set(name.split(' '));
        intersection = set(words).intersection(set(name_parts))
        if (len(intersection) > 0) :
            return name
    return None


def name_speech(data, names):
    speeches = read_speech(data)
    named_speeches = []
    for speech in speeches:
        name = None
        for token in speech:
            if name:
                break
            if (not token["isChar"]):
                name = get_speech_name(token["txt"], names)
        named_speeches.append({ "speeker": name, "speech_tokens": speech})
    return named_speeches

for a in name_speech(read_hary_potter(), person_list):
    print a