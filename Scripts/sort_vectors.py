def sort_and_output():
    import csv
    
    with open("vectors.txt", 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
        
    for row in data:
        for i in range(1, len(row)):
            row[i] = int(row[i])
        
    
    data.sort(key=lambda x: (x[1], x[2], x[3], x[4], x[5], x[6], x[7]))

    with open("sorted_vectors.txt", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def sort_vectors_intelligently():
    import csv
    import numpy as np
    from sklearn.cluster import KMeans

    # Read the data from the file
    with open('vectors.txt', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header
        data = list(reader)

    # Convert the data to integers and extract the vectors
    indices = [row[0] for row in data]
    vectors = [list(map(int, row[1:])) for row in data]

    # Convert vectors to numpy array
    vectors_np = np.array(vectors)

    # Determine the number of clusters (you can adjust this number)
    num_clusters = 5

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(vectors_np)
    labels = kmeans.labels_

    # Combine the labels with the original data
    labeled_data = list(zip(labels, indices, vectors))

    # Sort the data by cluster labels and then by vectors within each cluster
    labeled_data.sort(key=lambda x: (x[0], x[2]))

    # Write the sorted data back to the file
    with open('sorted_vectors_intelligently.txt', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        for label, index, vector in labeled_data:
            writer.writerow([index] + vector)

sort_vectors_intelligently()