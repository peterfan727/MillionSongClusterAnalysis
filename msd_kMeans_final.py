import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions, types
from pyspark.ml import Pipeline
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler, Word2Vec, MinMaxScaler, Tokenizer, PCA
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from msd_kMeans_ETL import feature_cols

spark = SparkSession.builder.appName('msd-kMeans-short').getOrCreate()
assert spark.version >= '3.2' # make sure we have Spark 3.2+
spark.sparkContext.setLogLevel('WARN')


""" Transformers for string type columns """
artist_id_tf = Pipeline(stages=[
    Tokenizer(inputCol='artist_id', outputCol='artist_id_words'),
    Word2Vec(inputCol='artist_id_words', outputCol='artist_id_vec', minCount=1),
    MinMaxScaler(inputCol='artist_id_vec', outputCol='artist_id_scaled')
])
artist_name_tf = Pipeline(stages=[
    Tokenizer(inputCol='artist_name', outputCol='artist_name_words'),
    Word2Vec(inputCol='artist_name_words', outputCol='artist_name_vec', minCount=1),
    MinMaxScaler(inputCol='artist_name_vec', outputCol='artist_name_scaled')
])
title_tf = Pipeline(stages=[
    Tokenizer(inputCol='title', outputCol='title_words'),
    Word2Vec(inputCol='title_words', outputCol='title_vec', minCount=1),
    MinMaxScaler(inputCol='title_vec', outputCol='title_scaled')
])

######################################################################################

""" Transformers for string array type columns """
similar_artists_tf = Pipeline(stages=[
    Word2Vec(inputCol='similar_artists', outputCol='similar_artists_vec', minCount=1),
    MinMaxScaler(inputCol='similar_artists_vec', outputCol='similar_artists_scaled')
])

######################################################################################

""" Transformers for float/int type columns """
artist_familiarity_tf = Pipeline(stages=[
    VectorAssembler(inputCols=['artist_familiarity'], outputCol='artist_familiarity_vec'),
    MinMaxScaler(inputCol='artist_familiarity_vec', outputCol='artist_familiarity_scaled')
])
artist_hotttnesss_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['artist_hotttnesss'], outputCol='artist_hotttnesss_vec'),
    MinMaxScaler(inputCol='artist_hotttnesss_vec', outputCol='artist_hotttnesss_scaled')
])

# artist_latitude_tf = MinMaxScaler(inputCol='artist_latitude', outputCol='artist_latitude_scaled')
# artist_longitude_tf = MinMaxScaler(inputCol='artist_longitude', outputCol='artist_longitude_scaled')
# danceability_tf = Pipeline(stages=[ 
#     VectorAssembler(inputCols=['danceability'], outputCol='danceability_scaled'),
#     # MinMaxScaler(inputCol='danceability_vec', outputCol='danceability_scaled')
# ])
# energy_tf = Pipeline(stages=[ 
#     VectorAssembler(inputCols=['energy'], outputCol='energy_scaled'),
#     # MinMaxScaler(inputCol='energy_vec', outputCol='energy_scaled')
# ])
# end_of_fade_in_tf = Pipeline(stages=[ 
#     VectorAssembler(inputCols=['end_of_fade_in'], outputCol='end_of_fade_in_vec'),
#     MinMaxScaler(inputCol='end_of_fade_in_vec', outputCol='end_of_fade_in_scaled')
# ])
# start_of_fade_out_tf = Pipeline(stages=[ 
#     VectorAssembler(inputCols=['start_of_fade_out'], outputCol='start_of_fade_out_vec'),
#     MinMaxScaler(inputCol='start_of_fade_out_vec', outputCol='start_of_fade_out_scaled')
# ])
# key_confidence_tf = Pipeline(stages=[ 
#     VectorAssembler(inputCols=['key_confidence'], outputCol='key_confidence_vec'),
#     MinMaxScaler(inputCol='key_confidence_vec', outputCol='key_confidence_scaled')
# ])
key_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['key'], outputCol='key_vec'),
    MinMaxScaler(inputCol='key_vec', outputCol='key_scaled')
])

duration_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['duration'], outputCol='duration_vec'),
    MinMaxScaler(inputCol='duration_vec', outputCol='duration_scaled')
])
loudness_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['loudness'], outputCol='loudness_vec'),
    MinMaxScaler(inputCol='loudness_vec', outputCol='loudness_scaled')
])
tempo_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['tempo'], outputCol='tempo_vec'),
    MinMaxScaler(inputCol='tempo_vec', outputCol='tempo_scaled')
])
mode_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['mode'], outputCol='mode_vec'),
    MinMaxScaler(inputCol='mode_vec', outputCol='mode_scaled')
])
time_signature_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['time_signature'], outputCol='time_signature_vec'),
    MinMaxScaler(inputCol='time_signature_vec', outputCol='time_signature_scaled')
])
year_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['year'], outputCol='year_vec'),
    MinMaxScaler(inputCol='year_vec', outputCol='year_scaled')
])


######################################################################################

segments_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_start_mean'], outputCol='segments_start_mean_vec'),
    MinMaxScaler(inputCol='segments_start_mean_vec', outputCol='segments_start_mean_scaled')
])
segments_loudness_max_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_max_mean'], outputCol='segments_loudness_max_mean_vec'),
    MinMaxScaler(inputCol='segments_loudness_max_mean_vec', outputCol='segments_loudness_max_mean_scaled')
])
segments_loudness_max_time_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_max_time_mean'], outputCol='segments_loudness_max_time_mean_vec'),
    MinMaxScaler(inputCol='segments_loudness_max_time_mean_vec', outputCol='segments_loudness_max_time_mean_scaled')
])
segments_loudness_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_start_mean'], outputCol='segments_loudness_start_mean_vec'),
    MinMaxScaler(inputCol='segments_loudness_start_mean_vec', outputCol='segments_loudness_start_mean_scaled')
])
sections_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['sections_start_mean'], outputCol='sections_start_mean_vec'),
    MinMaxScaler(inputCol='sections_start_mean_vec', outputCol='sections_start_mean_scaled')
])
beats_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['beats_start_mean'], outputCol='beats_start_mean_vec'),
    MinMaxScaler(inputCol='beats_start_mean_vec', outputCol='beats_start_mean_scaled')
])
bars_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['bars_start_mean'], outputCol='bars_start_mean_vec'),
    MinMaxScaler(inputCol='bars_start_mean_vec', outputCol='bars_start_mean_scaled')
])
tatums_start_mean_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['tatums_start_mean'], outputCol='tatums_start_mean_vec'),
    MinMaxScaler(inputCol='tatums_start_mean_vec', outputCol='tatums_start_mean_scaled')
])
segments_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_start_std'], outputCol='segments_start_std_vec'),
    MinMaxScaler(inputCol='segments_start_std_vec', outputCol='segments_start_std_scaled')
])
segments_loudness_max_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_max_std'], outputCol='segments_loudness_max_std_vec'),
    MinMaxScaler(inputCol='segments_loudness_max_std_vec', outputCol='segments_loudness_max_std_scaled')
])
segments_loudness_max_time_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_max_time_std'], outputCol='segments_loudness_max_time_std_vec'),
    MinMaxScaler(inputCol='segments_loudness_max_time_std_vec', outputCol='segments_loudness_max_time_std_scaled')
])
segments_loudness_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['segments_loudness_start_std'], outputCol='segments_loudness_start_std_vec'),
    MinMaxScaler(inputCol='segments_loudness_start_std_vec', outputCol='segments_loudness_start_std_scaled')
])
sections_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['sections_start_std'], outputCol='sections_start_std_vec'),
    MinMaxScaler(inputCol='sections_start_std_vec', outputCol='sections_start_std_scaled')
])
beats_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['beats_start_std'], outputCol='beats_start_std_vec'),
    MinMaxScaler(inputCol='beats_start_std_vec', outputCol='beats_start_std_scaled')
])
bars_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['bars_start_std'], outputCol='bars_start_std_vec'),
    MinMaxScaler(inputCol='bars_start_std_vec', outputCol='bars_start_std_scaled')
])
tatums_start_std_tf = Pipeline(stages=[ 
    VectorAssembler(inputCols=['tatums_start_std'], outputCol='tatums_start_std_vec'),
    MinMaxScaler(inputCol='tatums_start_std_vec', outputCol='tatums_start_std_scaled')
])

######################################################################################


# 2D float arrays

segments_timbre_tf = Pipeline(stages=[
    VectorAssembler(inputCols=['avg(segments_timbre[0])'], outputCol='avg(segments_timbre[0])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[0])_vec', outputCol='avg(segments_timbre[0])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[1])'], outputCol='avg(segments_timbre[1])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[1])_vec', outputCol='avg(segments_timbre[1])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[2])'], outputCol='avg(segments_timbre[2])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[2])_vec', outputCol='avg(segments_timbre[2])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[3])'], outputCol='avg(segments_timbre[3])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[3])_vec', outputCol='avg(segments_timbre[3])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[4])'], outputCol='avg(segments_timbre[4])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[4])_vec', outputCol='avg(segments_timbre[4])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[5])'], outputCol='avg(segments_timbre[5])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[5])_vec', outputCol='avg(segments_timbre[5])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[6])'], outputCol='avg(segments_timbre[6])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[6])_vec', outputCol='avg(segments_timbre[6])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[7])'], outputCol='avg(segments_timbre[7])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[7])_vec', outputCol='avg(segments_timbre[7])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[8])'], outputCol='avg(segments_timbre[8])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[8])_vec', outputCol='avg(segments_timbre[8])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[9])'], outputCol='avg(segments_timbre[9])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[9])_vec', outputCol='avg(segments_timbre[9])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[10])'], outputCol='avg(segments_timbre[10])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[10])_vec', outputCol='avg(segments_timbre[10])_scaled'),
    VectorAssembler(inputCols=['avg(segments_timbre[11])'], outputCol='avg(segments_timbre[11])_vec'),
    MinMaxScaler(inputCol='avg(segments_timbre[11])_vec', outputCol='avg(segments_timbre[11])_scaled')
])

segments_pitches_tf = Pipeline(stages=[
    VectorAssembler(inputCols=['avg(segments_pitches[0])'], outputCol='avg(segments_pitches[0])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[0])_vec', outputCol='avg(segments_pitches[0])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[1])'], outputCol='avg(segments_pitches[1])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[1])_vec', outputCol='avg(segments_pitches[1])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[2])'], outputCol='avg(segments_pitches[2])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[2])_vec', outputCol='avg(segments_pitches[2])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[3])'], outputCol='avg(segments_pitches[3])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[3])_vec', outputCol='avg(segments_pitches[3])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[4])'], outputCol='avg(segments_pitches[4])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[4])_vec', outputCol='avg(segments_pitches[4])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[5])'], outputCol='avg(segments_pitches[5])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[5])_vec', outputCol='avg(segments_pitches[5])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[6])'], outputCol='avg(segments_pitches[6])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[6])_vec', outputCol='avg(segments_pitches[6])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[7])'], outputCol='avg(segments_pitches[7])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[7])_vec', outputCol='avg(segments_pitches[7])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[8])'], outputCol='avg(segments_pitches[8])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[8])_vec', outputCol='avg(segments_pitches[8])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[9])'], outputCol='avg(segments_pitches[9])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[9])_vec', outputCol='avg(segments_pitches[9])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[10])'], outputCol='avg(segments_pitches[10])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[10])_vec', outputCol='avg(segments_pitches[10])_scaled'),
    VectorAssembler(inputCols=['avg(segments_pitches[11])'], outputCol='avg(segments_pitches[11])_vec'),
    MinMaxScaler(inputCol='avg(segments_pitches[11])_vec', outputCol='avg(segments_pitches[11])_scaled')
])

all_tf = Pipeline(stages=[
    # Transformers
    # artist_id_tf,
    # artist_name_tf,
    # title_tf,
    # similar_artists_tf,
    artist_familiarity_tf,
    artist_hotttnesss_tf,
    # danceability_tf,
    # energy_tf,
    # end_of_fade_in_tf,
    # start_of_fade_out_tf,
    key_tf,
    # key_confidence_tf,
    duration_tf,
    loudness_tf,
    tempo_tf,
    mode_tf,
    time_signature_tf,
    year_tf,
    ##
    segments_start_mean_tf,
    segments_loudness_max_mean_tf,
    segments_loudness_max_time_mean_tf,
    segments_loudness_start_mean_tf,
    sections_start_mean_tf,
    beats_start_mean_tf,
    bars_start_mean_tf,
    tatums_start_mean_tf,
    segments_start_std_tf,
    segments_loudness_max_std_tf,
    segments_loudness_max_time_std_tf,
    segments_loudness_start_std_tf,
    sections_start_std_tf,
    beats_start_std_tf,
    bars_start_std_tf,
    tatums_start_std_tf,
    segments_timbre_tf,
    segments_pitches_tf
])


stringTypes_ignore = ['artist_id_words', 'artist_id_vec', 'filename',
    'artist_name_words', 'artist_name_vec',
    'title_words', 'title_vec']
stringArrTypes_ignore = ['similar_artists_vec', 'artist_terms',]
floatTypes_ignore = ['artist_familiarity_vec', 'artist_hotttnesss_vec', 'danceability_vec', 'energy_vec',
    'end_of_fade_in_vec', 'start_of_fade_out_vec', 'key_vec', 'key_confidence_vec', 'duration_vec',
    'loudness_vec', 'tempo_vec', 'mode_vec', 'time_signature_vec', 'year_vec',
    ]
origin_array_ignore = ['segments_start_mean_vec', 'segments_loudness_max_mean_vec','segments_loudness_max_time_mean_vec',
    'segments_loudness_start_mean_vec','sections_start_mean_vec','beats_start_mean_vec','bars_start_mean_vec','tatums_start_mean_vec',
    'segments_start_std_vec','segments_loudness_max_std_vec','segments_loudness_max_time_std_vec','segments_loudness_start_std_vec',
    'sections_start_std_vec','beats_start_std_vec','bars_start_std_vec','tatums_start_std_vec']
origin_2d_array_ignore = [
    'avg(segments_timbre[0])_vec', #'avg(segments_timbre[0])',
    'avg(segments_timbre[1])_vec', #'avg(segments_timbre[1])',
    'avg(segments_timbre[2])_vec', #'avg(segments_timbre[2])',
    'avg(segments_timbre[3])_vec', #'avg(segments_timbre[3])',
    'avg(segments_timbre[4])_vec', #'avg(segments_timbre[4])',
    'avg(segments_timbre[5])_vec', #'avg(segments_timbre[5])',
    'avg(segments_timbre[6])_vec', #'avg(segments_timbre[6])',
    'avg(segments_timbre[7])_vec', #'avg(segments_timbre[7])',
    'avg(segments_timbre[8])_vec', #'avg(segments_timbre[8])',
    'avg(segments_timbre[9])_vec', #'avg(segments_timbre[9])',
    'avg(segments_timbre[10])_vec', #'avg(segments_timbre[10])',
    'avg(segments_timbre[11])_vec', #'avg(segments_timbre[11])',
    'avg(segments_pitches[0])_vec', #'avg(segments_pitches[0])',
    'avg(segments_pitches[1])_vec', #'avg(segments_pitches[1])',
    'avg(segments_pitches[2])_vec', #'avg(segments_pitches[2])',
    'avg(segments_pitches[3])_vec', #'avg(segments_pitches[3])',
    'avg(segments_pitches[4])_vec', #'avg(segments_pitches[4])',
    'avg(segments_pitches[5])_vec', #'avg(segments_pitches[5])',
    'avg(segments_pitches[6])_vec', #'avg(segments_pitches[6])',
    'avg(segments_pitches[7])_vec', #'avg(segments_pitches[7])',
    'avg(segments_pitches[8])_vec', #'avg(segments_pitches[8])',
    'avg(segments_pitches[9])_vec', #'avg(segments_pitches[9])',
    'avg(segments_pitches[10])_vec',# 'avg(segments_pitches[10])',
    'avg(segments_pitches[11])_vec',# 'avg(segments_pitches[11])'
]
#ignore_columns = stringTypes_ignore + stringArrTypes_ignore + floatTypes_ignore + feature_cols + origin_array_ignore + origin_2d_array_ignore # columns to ignore (str)
ignore_columns = ['filename','artist_terms', 'end_of_fade_in', 'start_of_fade_out', 'key_confidence',
                    'mode_confidence', 'time_signature_confidence']
######################################################################################


def main(inputs):

    input_train = inputs + "/trainSet"
    input_test = inputs + "/testSet"

    train_df = spark.read.option("header", "true").csv(input_train, inferSchema=True).cache()
    train_df.drop("filename")
    #train_df.show(1)

    """
    Build pipeline
    """

    scaled_features = [name + '_scaled' for name in train_df.schema.names if name not in ignore_columns]

    final_assembler = VectorAssembler(
    # inputCols=[x for x in df.columns if x not in ignore], 
    inputCols=scaled_features, 
    outputCol='features')

    # Pipeline
    pipeline = Pipeline(stages=[
        all_tf,
        final_assembler,
        KMeans(featuresCol='features', k=4)    # Optmized k
    ])

    model = pipeline.fit(train_df)


    # train_df.unpersist()

    test_df = spark.read.option("header", "true").csv(input_test, inferSchema=True)
    test_df.drop("filename")
    # Summarize the model over the training set and print out some metrics
    

    # Make predictions
    predictions = model.transform(test_df)
    # Evaluate clustering by computing Silhouette score
    evaluator = ClusteringEvaluator()

    silhouette = evaluator.evaluate(predictions)
    print("Silhouette with squared euclidean distance with (kMean k=4) = " + str(silhouette))


    """
    Plot the 2-D cluster using PCA and Kmean
    """

    print("Generating clustering 2-D plot with kmean k=4 and PCA2.")
    # Pipeline
    PCA_assemble_pipeline = Pipeline(stages=[
        all_tf,
        final_assembler
    ])

    PCA_assembled = PCA_assemble_pipeline.fit(train_df) # Choose the dataframe to plot

    Assemble_df = PCA_assembled.transform(train_df).select('features') # Choose the dataframe to plot

    # Assemble_df.first()

    # Clustering
    KMeans_=KMeans(featuresCol='features', k=4)  # Choose the number of cluster here
    KMeans_Model=KMeans_.fit(Assemble_df)
    KMeans_Assignments=KMeans_Model.transform(Assemble_df)

    # Converting to 2-D
    pca = PCA(k=2, inputCol='features', outputCol="PCA_features")
    model = pca.fit(Assemble_df)
    pca_transformed = model.transform(Assemble_df)

    x_pca = np.array(pca_transformed.rdd.map(lambda row: row.PCA_features).collect())

    cluster_assignment = np.array(KMeans_Assignments.rdd.map(lambda row: row.prediction).collect()).reshape(-1,1)

    pca_data = np.hstack((x_pca,cluster_assignment))
    pca_df = pd.DataFrame(data=pca_data, columns=("1st_principal", "2nd_principal","cluster_assignment"))
    sns.FacetGrid(pca_df,hue="cluster_assignment", height=6).map(plt.scatter, '1st_principal', '2nd_principal').add_legend()
    plt.savefig('Cluster.png')

    """
    Plot the 3-D cluster using PCA and Kmean
    """
    print("Generating clustering 3-D plot with kmean k=4 and and PCA3.")
    # Converting to 3-D
    pca = PCA(k=3, inputCol='features', outputCol="pca_features")
    model = pca.fit(Assemble_df)
    pca_transformed = model.transform(Assemble_df)

    x_pca = np.array(pca_transformed.rdd.map(lambda row: row.pca_features).collect())

    cluster_assignment = np.array(KMeans_Assignments.rdd.map(lambda row: row.prediction).collect()).reshape(-1,1)

    pca_data = np.hstack((x_pca,cluster_assignment))
    pca_df = pd.DataFrame(data=pca_data, columns=("1st_principal", "2nd_principal", "3rd_principal","cluster_assignment"))

    # For 3D plotting
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)
    ax = fig.add_subplot(111, projection='3d')
    x = np.array(pca_df['1st_principal'])
    y = np.array(pca_df['2nd_principal'])
    z = np.array(pca_df['3rd_principal'])
    ax.scatter(x,y,z, marker="s", c=pca_df["cluster_assignment"], s=10, cmap="RdBu")
    plt.savefig('Cluster_3D.png')

    print("Saving as a rotating gif.")
    # From https://stackoverflow.com/questions/51457738/animating-a-3d-scatterplot-with-matplotlib-to-gif-ends-up-empty

    # Save the rotating 3D plot as a gif
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation
    def rotate(angle):
        ax.view_init(azim=angle)

    print("Making animation")
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    rot_animation.save('3D-Cluster-Rotation.gif', dpi=80, writer='imagemagick')

    """
    CrossTab the cluster with the artist term, and get the closed musics result
    """
    terms = np.array(train_df.rdd.map(lambda row: row.artist_terms).collect())
    df = pd.DataFrame({
        'cluster': pca_df["cluster_assignment"],
        'term': terms,
    })
    counts = pd.crosstab(df['term'], df['cluster'])
    print("Raw cluster crosstab: ", counts)
    counts.to_csv('term_cluster.csv')

    close_music_terms = np.empty(shape=(6, 4), dtype="U20")
    for i in range(0, 4): # Depending on the number of cluster
        sorted_with_cluster = counts.sort_values(i,ascending=False)
        for j in range(0, 6): # Get the first 6 closed music terms in one cluster
            # print(sorted_with_cluster.index[j])
            close_music_terms[j][i] = sorted_with_cluster.index[j]
    close_music_terms_df = pd.DataFrame(close_music_terms)
    print("Closest 6 musics in clusters:", close_music_terms_df)
    close_music_terms_df.to_csv('closest_musics.csv')
    print("All finished.")


if __name__ == '__main__':
    inputs = sys.argv[1]
    

    # sc = spark.sparkContext

    main(inputs)
