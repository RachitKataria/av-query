import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory("wav", [".wav"])

	# Recognize first query
	songs = djv.recognize(FileRecognizer, "query/first.wav")
	print "From first query we recognized: %s\n" % songs

	# Recognize second query
	songs = djv.recognize(FileRecognizer, "query/second.wav")
	print "From second query we recognized: %s\n" % songs

	# Recognize third query
	songs = djv.recognize(FileRecognizer, "query/ellen.wav")
	print "From third query we recognized: %s\n" % songs
