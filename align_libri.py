from forced_align import align_many
import glob
import os.path
import json
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    audiopaths = []
    transcripts = []
    for wav in glob.glob("librispeech_val/wav/*.wav"):
        bare = os.path.split(os.path.splitext(wav)[0])[-1]
        transcripts.append(open("librispeech_val/txt/{}.txt".format(bare)).read().lower())
        audiopaths.append(wav)
    with open("librispeech_val.fa.json", "w") as out:
        for item in align_many(audiopaths, transcripts):
            out.write(json.dumps(item))
            out.write("\n")
            
            
main()
