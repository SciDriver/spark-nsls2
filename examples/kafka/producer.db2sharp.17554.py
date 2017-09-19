from kafka import KafkaProducer

from datetime import timedelta, datetime, tzinfo

import numpy as np
import pickle

from SharpReader import SharpReader

# Define the SharpReader experiment-specific parameters

from SharpReader import SharpReader

sid = 17554
fields = ['dssx','dssy']

sharpReader = SharpReader()
# x_c, y_c, xn, yn, threshold
sharpReader.init(60, 66, 100, 100, 2)

# Get metadata from databroker

print("getting fnames, points from db ...");
t1 = datetime.now();
fnames, ic = sharpReader.get_merlin1_fnames(sid)
xs, ys = sharpReader.get_points(sid, fields)
t2 = datetime.now();
print ("processing time: ", (t2 - t1), ", fnames: ", len(fnames),
       ", ic: ", len(ic), ", xs: ", len(xs), ", ys: ", len(ys));

# Load files

print("loading files ...");
t1 = datetime.now();
frames = sharpReader.load_files(sid, fnames, ic)
t2 = datetime.now();
print ("processing time: ", (t2 - t1), "frames: ", len(frames));

# Send to Kafka

topic = "topic-d"

n = 1000 # number of msgs (Kafka max msg size is 1 MB)
ns = np.int(len(frames)/n)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

print("sending frames and scan points to Kafka ...");
t1 = datetime.now();

producer.send(topic, pickle.dumps([n]))

for i in range(0, n):
    n1 = i*ns
    n2 = (i+1)*ns
    msg = pickle.dumps([i, frames[n1:n2], xs[n1:n2], ys[n1:n2]])
    producer.send(topic, msg)

t2 = datetime.now();
print ("processing time: ", (t2 - t1))





