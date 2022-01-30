## NLP - Movie review sentiment analysis

The colab notebook contains the code for building a LSTM Recurrent Neural Network that gives 87-88% accuracy on the IMDB Movie Review Sentiment Analysis Dataset. The repo also contains the code to deploy the model online.

## App demo

Follow the instructions below to run the app locally with Docker.

Once you have Docker installed, clone this repo 

```bash
git clone https://github.com/sbhimire/nlp-sentiment-analysis.git
```

Navigate to the webapp directory of the repo.

```bash
cd semi-super/webapp
```

Now build the container image using the `docker build` command. It will take few minutes.

```bash
docker build -t sentiment .
```

Start your container using the docker run command and specify the name of the image we just created:

```bash
docker run -dp 8080:8080 sentiment
```

After a few seconds, open your web browser to http://localhost:8080. You should see the app.
