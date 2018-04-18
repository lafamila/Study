from Data_Wrangling import Wrangler
from tom_lib.structure.corpus import Corpus
from tom_lib.nlp.topic_model import LatentDirichletAllocation
from tom_lib.visualization.visualization import Visualization

stop_words=["facebook", "youtub", "htc", "free"]

wrangler = Wrangler(file_path="Steam.csv", output="Steam_Cleand_test.csv",
                    text_column_name="comment", id_column_name="profile",
                    sep=",", encoding="utf-8", stop_words=stop_words)
output = wrangler.wrangling()


corpus = Corpus(source_file_path=output,
                language='english',
                vectorization='tfidf',
                n_gram=1,
                max_relative_frequency=0.8,
                min_absolute_frequency=3)
print('corpus size:', corpus.size)
print('vocabulary size:', len(corpus.vocabulary))


topic_model = LatentDirichletAllocation(corpus)
topic_model.infer_topics(num_topics=15, algorithm='variational')

print('\nTopics:')
topic_model.print_topics(num_words=10)
print('\nTopic distribution for document 0:',
      topic_model.topic_distribution_for_document(0))
print('\nMost likely topic for document 0:',
      topic_model.most_likely_topic_for_document(0))
print('\nFrequency of topics:',
      topic_model.topics_frequency())
for i in range(1, 11, 1):
    print('\nTop 10 most relevant words for topic {}:'.format(i),
      topic_model.top_words(i, 10))
