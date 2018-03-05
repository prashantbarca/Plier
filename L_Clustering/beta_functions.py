import tensorflow as tf
import numpy as np

#hexdump = ["48","54","54","50","2f","31","2e","31","20","33","30","33","20","53","65","65","20","4f","74","68","65","72","0d","0a","4c","6f","63","61","74","69","6f","6e","3a","20","68","74","74","70","3a","2f","2f","31","30","2e","30","2e","35","30","2e","35","32","2f","6c","6f","67","6f","75","74","2e","68","74","6d","6c","0d","0a","43","6f","6e","74","65","6e","74","2d","4c","65","6e","67","74","68","3a","20","30","0d","0a","0d","0a"]
DEBUG=1

def create_hex_sample(hexdumps):
    slices = []
    centroids = []
    if DEBUG:
        print("HEXDUMPS")
        print(hexdumps)
    dump = 0
    for hexdump in hexdumps:
        hexdump_by_byte = [hexdump[i:i+2] for i in range(0, len(hexdump), 2)]
        annotated_hexdump = []
        position = 0
        for byte in hexdump_by_byte:
            if False and DEBUG:
                annotated_hexdump.append([position+(.1*dump), int(byte,16)])
            else:
                annotated_hexdump.append([position, int(byte,16), dump])
            position += 1
        name = "cluster_" + `dump`
        dump += 1
        tensor = tf.convert_to_tensor(np.array(annotated_hexdump, dtype=np.float32), dtype=tf.float32, name=name)
        tensor_centroid = np.array([[dump,position]], dtype=np.float64)
        if DEBUG:
            print("HEXDUMP")
            print(hexdump)
            print("ANNOTATED HEXDUMP")
            print(annotated_hexdump)
            print("NAME")
            print(name)
            print("CENTROID")
            print(tensor_centroid)
        centroids.append(tensor_centroid)
        slices.append(tensor)
    samples = tf.concat(axis=0, values=slices, name='samples')
    centroids = tf.concat(axis=0, values=centroids, name='centroids')
    if DEBUG:
        print("SLICES")
        print(slices)
        print("CENTROIDS")
        print(centroids)
        print("SAMPLES")
        print(samples)
    return centroids, samples

def create_samples(n_clusters, n_samples_per_cluster, n_features, embiggen_factor, seed):
    annotated_hexdump = []
    position = 0
    for byte in hexdump:
        annotated_hexdump.append([position, int(byte,16)])
        position = position + 1
    if DEBUG:
        print("HEXDUMP")
        print(hexdump)
        print("ANNOTATED HEXDUMP")
        print(annotated_hexdump)
    np.random.seed(seed)
    slices = []
    centroids = []
    #for i in range(n_clusters):
        #samples = tf.random_normal((n_samples_per_cluster, n_features), mean=0.0, stddev=5.0, dtype=tf.float32, seed=seed, name="cluster_{}".format(i))
        #print("SAMPLES")
        #print(samples)
        #current_centroid = (np.random.random((1, n_features)) * embiggen_factor) - (embiggen_factor/2)
        #print("CURRENT CENTROID")
        #print(current_centroid)
        #centroids.append(current_centroid)
        #samples += current_centroid
        #slices.append(samples)
    # Create a big "samples" dataset
    tensor = tf.convert_to_tensor(np.array(annotated_hexdump, dtype=np.float32), dtype=tf.float32, name="cluster_3")
    tensor_centroid = np.array([[0,0]], dtype=np.float64)
    centroids.append(tensor_centroid)
    slices.append(tensor)

    if DEBUG:
        print("TENSOR")
        print(tensor)
        print("SLICES")
        print(slices)
        print("CENTROIDS")
        print(centroids)
    samples = tf.concat(axis=0, values=slices, name='samples')
    centroids = tf.concat(axis=0, values=centroids, name='centroids')
    return centroids, samples

def plot_clusters(all_samples, centroids):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    # Plot out the different clusters
    # Choose a different colour for each cluster
    plt.axes(projection='3d')
    #colour = plt.cm.rainbow(np.linspace(0,1,len(centroids)))
    colour=['b','r','g']
    if DEBUG:
        print("CENTROIDS")
        print(centroids)
        print("ALL SAMPLES")
        print(all_samples)
        print("LEN CENTROIDS")
        print(len(centroids))
        print("COLOUR")
        print(colour)
    start_index = 0
    
    for i, centroid in enumerate(centroids):
        end_index = start_index+int(centroid[1])
        # Grab just the samples fpr the given cluster and plot them out with a new colour
        #samples = all_samples[i*n_samples_per_cluster:(i+1)*n_samples_per_cluster]
        samples = all_samples[start_index:end_index]
        if DEBUG:
            print("INNER LOOP")
            print(i)
            print(centroid)
            print(int(centroid[1]))
            print("SAMPLES")
            print(samples)
        start_index = end_index
        #plt.scatter(samples[:,0], samples[:,1], c=colour[i])
        print("CHECKING COORDS")
        print(type(samples[:,0]))
        print(samples[:,0])
        print(type(samples[:,1]))
        print(samples[:,1])
        z = np.array( [i] * len(samples), dtype=np.float32 )
        print(type(z))
        print(z)
        plt.scatter(samples[:,0], samples[:,1], zs=z, s=4**2, c=colour[i])

        # Also plot centroid
        #plt.plot(centroid[0], centroid[1], markersize=35, marker="x", color='k', mew=10)
        #plt.plot(centroid[0], centroid[1], markersize=30, marker="x", color='m', mew=5)
    #print("DEBUG")
    min(all_samples, key=lambda x: x[1])[1]
    ax = plt.gca()
    plt.xticks(np.arange(min(all_samples, key=lambda x: x[0])[0], max(all_samples, key=lambda x: x[0])[0], 1.0))
    plt.yticks(np.arange(min(all_samples, key=lambda x: x[1])[1], max(all_samples, key=lambda x: x[1])[1], 16.0))
    labels = [item.get_text() for item in ax.get_yticklabels()]
    for i, label in enumerate(labels):
        labels[i]=hex(i*16)
    ax.set_yticklabels(labels)
    ax.set_zlim(-1,3)
    plt.show()

def choose_random_centroids(samples, n_clusters, seed=None):
    # Step 0: Initialisation: Select `n_clusters` number of random points
    n_samples = tf.shape(samples)[0]
    random_indices = tf.random_shuffle(tf.range(0, n_samples), seed=seed)
    begin = [0,]
    size = [n_clusters,]
    size[0] = n_clusters
    centroid_indices = tf.slice(random_indices, begin, size)
    initial_centroids = tf.gather(samples, centroid_indices)
    return initial_centroids

def assign_to_nearest(samples, centroids):
    # Finds the nearest centroid for each sample

    # START from http://esciencegroup.com/2016/01/05/an-encounter-with-googles-tensorflow/
    expanded_vectors = tf.expand_dims(samples, 0)
    expanded_centroids = tf.expand_dims(centroids, 1)
    distances = tf.reduce_sum( tf.square( tf.subtract(expanded_vectors, expanded_centroids)), 2)
    mins = tf.argmin(distances, 0)
    # END from http://esciencegroup.com/2016/01/05/an-encounter-with-googles-tensorflow/
    nearest_indices = mins
    return nearest_indices

def update_centroids(samples, nearest_indices, n_clusters):
    # Updates the centroid to be the mean of all samples associated with it.
    nearest_indices = tf.to_int32(nearest_indices)
    partitions = tf.dynamic_partition(samples, nearest_indices, n_clusters)
    new_centroids = tf.concat(axis=0, values=[tf.expand_dims(tf.reduce_mean(partition, 0), 0) for partition in partitions])
    #new_centroids = tf.concat([tf.expand_dims(tf.reduce_mean(partition, 0), 0) for partition in partitions], 0)
    return new_centroids

def nearest_centroid(sample, centroids):
    # Compute distance to each centroid
    k = tf.shape(centroids)[0]
    d = tf.reduce_sum(tf.pow(tf.subtract(tf.tile(sample, (k, 1)), centroids), 2))
    return tf.argmin(d)
