import tensorflow as tf
import numpy as np

DEBUG=1

def create_hex_sample(hexdumps):
    slices = []
    centroids = []
    dump = 0
    for hexdump in hexdumps:
        hexdump_by_byte = [hexdump[i:i+2] for i in range(0, len(hexdump), 2)]
        annotated_hexdump = []
        position = 0
        for byte in hexdump_by_byte:
            if False and DEBUG:
                annotated_hexdump.append([position+(.1*dump), int(byte,16)])
            else:
                #annotated_hexdump.append([position, int(byte,16), dump])
                annotated_hexdump.append([position, int(byte,16)])
            position += 1
        name = "cluster_" + `dump`
        dump += 1
        tensor = tf.convert_to_tensor(np.array(annotated_hexdump, dtype=np.float32), dtype=tf.float32, name=name)
        tensor_centroid = np.array([[dump,position]], dtype=np.float64)
        centroids.append(tensor_centroid)
        slices.append(tensor)
    samples = tf.concat(axis=0, values=slices, name='samples')
    centroids = tf.concat(axis=0, values=centroids, name='centroids')
    return centroids, samples

def plot_clusters(all_samples, centroids, filename):
    import matplotlib.pyplot as plt
    # Choose a different colour for each cluster
    colour = plt.cm.rainbow(np.linspace(0,1,len(centroids)))
    start_index = 0
    
    for i, centroid in enumerate(centroids):
        end_index = start_index+int(centroid[1])
        samples = all_samples[start_index:end_index]
        start_index = end_index
        plt.scatter(samples[:,0], samples[:,1], c=colour[i])
    min(all_samples, key=lambda x: x[1])[1]
    ax = plt.gca()
    #plt.xticks(np.arange(min(all_samples, key=lambda x: x[0])[0], max(all_samples, key=lambda x: x[0])[0], 1.0))
    #plt.yticks(np.arange(min(all_samples, key=lambda x: x[1])[1], max(all_samples, key=lambda x: x[1])[1], 16.0))
    plt.yticks(np.arange(0, 257, 16))
    plt.tick_params( axis='x', which='both', bottom='off', top='off', labelbottom='off')
    labels = [item.get_text() for item in ax.get_yticklabels()]
    for i, label in enumerate(labels):
        labels[i]=hex(i*16)
    ax.set_yticklabels(labels)
    #plt.show()
    plt.ylim(ymax = 255+16, ymin = -16)
    plt.savefig(filename+".png")
