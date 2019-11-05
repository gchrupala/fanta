import json
import multiprocessing as mp
import logging
try:
    import gentle
except ModuleNotFoundError:
    import sys
    sys.path.append('/roaming/gentle')
    import gentle
    
resources = gentle.Resources()
 
def on_progress(p):
    for k,v in p.items():
        logging.debug("%s: %s" % (k, v))

def align_many(audiopaths, transcripts):
    with mp.Pool(mp.cpu_count()) as pool:
        result = pool.map(align, zip(audiopaths, transcripts))
    return result
    
def align(args): 
    audiopath, transcript = args                     
    with gentle.resampled(audiopath) as wavfile:
        logging.info("Audio file: {}".format(audiopath))
        logging.info("Transcript: <{}...>".format(transcript[:40]))
        aligner = gentle.ForcedAligner(resources, transcript, nthreads=1, disfluency=False, 
                                   conservative=False)
        result = json.loads(aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging).to_json())
        result['audiopath'] = audiopath
        return result
    
