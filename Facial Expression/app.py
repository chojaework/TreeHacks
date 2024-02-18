# Facial expression classifier
import os
from fastai.vision.all import *
import gradio as gr

# Emotion
learn_emotion = load_learner('emotions_vgg19.pkl')
learn_emotion_labels = learn_emotion.dls.vocab

# Sentiment
learn_sentiment = load_learner('sentiment_vgg19.pkl')
learn_sentiment_labels = learn_sentiment.dls.vocab

# Predict
def predict(img):
    img = PILImage.create(img)
    
    pred_emotion, pred_emotion_idx, probs_emotion = learn_emotion.predict(img)
    
    pred_sentiment, pred_sentiment_idx, probs_sentiment = learn_sentiment.predict(img)
    
    #emotions = {f'emotion_{learn_emotion_labels[i]}': float(probs_emotion[i]) for i in range(len(learn_emotion_labels))}
    #sentiments = {f'sentiment_{learn_sentiment_labels[i]}': float(probs_sentiment[i]) for i in range(len(learn_sentiment_labels))}
    
    emotions = {learn_emotion_labels[i]: float(probs_emotion[i]) for i in range(len(learn_emotion_labels))}
    sentiments = {learn_sentiment_labels[i]: float(probs_sentiment[i]) for i in range(len(learn_sentiment_labels))}

    print("Emotions:", emotions)
    print("Sentiments:", sentiments)
                
    return [emotions, sentiments] #{**emotions, **sentiments}

# Gradio
title = "Facial Emotion and Sentiment Detector"

description = gr.Markdown(
                """Ever wondered what a person might be feeling looking at their picture? 
                 Well, now you can! Try this fun app. Just upload a facial image in JPG or
                 PNG format. Voila! you can now see what they might have felt when the picture
                 was taken.
                 
                 **Tip**: Be sure to only include face to get best results. Check some sample images
                 below for inspiration!""").value

article = gr.Markdown(
             """**DISCLAIMER:** This model does not reveal the actual emotional state of a person. Use and 
             interpret results at your own risk! It was built as a demo for AI course. Samples images
             were downloaded from VG & AftenPosten news webpages. Copyrights belong to respective
             brands. All rights reserved.
             
             **PREMISE:** The idea is to determine an overall sentiment of a news site on a daily basis
             based on the pictures. We are restricting pictures to only include close-up facial
             images.
             
             **DATA:** FER2013 dataset consists of 48x48 pixel grayscale images of faces. There are 28,709 
             images in the training set and 3,589 images in the test set. However, for this demo all 
             pictures were combined into a single dataset and 80:20 split was used for training. Images
             are assigned one of the 7 emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, and Neutral.
             In addition to these 7 classes, images were re-classified into 3 sentiment categories based
             on emotions:
             
             Positive (Happy, Surprise)
             
             Negative (Angry, Disgust, Fear, Sad)
             
             Neutral (Neutral)
             
             FER2013 (preliminary version) dataset can be downloaded at:
             https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data
             
             **MODEL:** VGG19 was used as the base model and trained on FER2013 dataset. Model was trained
             using PyTorch and FastAI. Two models were trained, one for detecting emotion and the other
             for detecting sentiment. Although, this could have been done with just one model, here two
             models were trained for the demo.""").value

enable_queue=True

examples = ['happy1.jpg', 'happy2.jpg', 'angry1.png', 'angry2.jpg', 'neutral1.jpg', 'neutral2.jpg']

gr.Interface(fn = predict, 
             inputs = gr.Image(shape=(48,48), image_mode='L'), # width=48, height=48 # shape=(48,48)
             outputs = [gr.Label(label='Emotion'), gr.Label(label='Sentiment')], #gr.Label(),
             title = title,
             examples = examples,
             description = description,
             article=article,
             allow_flagging='never').launch(enable_queue=enable_queue)
        
# Gradio
title = "Facial Emotion and Sentiment Detector"

description = gr.Markdown(
                """Ever wondered what a person might be feeling looking at their picture? 
                 Well, now you can! Try this fun app. Just upload a facial image in JPG or
                 PNG format. Voila! you can now see what they might have felt when the picture
                 was taken.
                 
                 **Tip**: Be sure to only include face to get best results. Check some sample images
                 below for inspiration!""").value

article = gr.Markdown(
             """**DISCLAIMER:** This model does not reveal the actual emotional state of a person. Use and 
             interpret results at your own risk! It was built as a demo for AI course. Samples images
             were downloaded from VG & AftenPosten news webpages. Copyrights belong to respective
             brands. All rights reserved.
             
             **PREMISE:** The idea is to determine an overall sentiment of a news site on a daily basis
             based on the pictures. We are restricting pictures to only include close-up facial
             images.
             
             **DATA:** FER2013 dataset consists of 48x48 pixel grayscale images of faces. There are 28,709 
             images in the training set and 3,589 images in the test set. However, for this demo all 
             pictures were combined into a single dataset and 80:20 split was used for training. Images
             are assigned one of the 7 emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, and Neutral.
             In addition to these 7 classes, images were re-classified into 3 sentiment categories based
             on emotions:
             
             Positive (Happy, Surprise)
             
             Negative (Angry, Disgust, Fear, Sad)
             
             Neutral (Neutral)
             
             FER2013 (preliminary version) dataset can be downloaded at:
             https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data
             
             **MODEL:** VGG19 was used as the base model and trained on FER2013 dataset. Model was trained
             using PyTorch and FastAI. Two models were trained, one for detecting emotion and the other
             for detecting sentiment. Although, this could have been done with just one model, here two
             models were trained for the demo.""").value

enable_queue=True

examples = ['happy1.jpg', 'happy2.jpg', 'angry1.png', 'angry2.jpg', 'neutral1.jpg', 'neutral2.jpg']

gr.Interface(fn = predict, 
             inputs = gr.Image(shape=(48,48), image_mode='L'), # width=48, height=48 # shape=(48,48)
             outputs = [gr.Label(label='Emotion'), gr.Label(label='Sentiment')], #gr.Label(),
             title = title,
             examples = examples,
             description = description,
             article=article,
             allow_flagging='never').launch(enable_queue=enable_queue)
