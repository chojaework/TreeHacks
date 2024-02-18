import os
import cv2
import matplotlib.pyplot as plt
from fastai.vision.all import *
import gradio as gr
import moviepy.editor as mp
import speech_recognition as sr


# Emotion and Sentiment learners
learn_emotion = load_learner('emotions_vgg19.pkl')
learn_emotion_labels = learn_emotion.dls.vocab
learn_sentiment = load_learner('sentiment_vgg19.pkl')
learn_sentiment_labels = learn_sentiment.dls.vocab

# Predict emotion and sentiment for a given image
def predict(img):
    pred_emotion, _, probs_emotion = learn_emotion.predict(img)
    pred_sentiment, _, probs_sentiment = learn_sentiment.predict(img)
    
    emotions = {learn_emotion_labels[i]: float(probs_emotion[i]) for i in range(len(learn_emotion_labels))}
    sentiments = {learn_sentiment_labels[i]: float(probs_sentiment[i]) for i in range(len(learn_sentiment_labels))}
    
    return emotions, sentiments

# Process video, capture frames every 5 seconds, and analyze
def process_video(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)

    emotions_total = {label: 0.0 for label in learn_emotion_labels}
    sentiments_total = {label: 0.0 for label in learn_sentiment_labels}
    total_frames = 0
    outputs = []

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % (5 * int(fps)) == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = PILImage.create(frame_rgb)

            # Predict emotions and sentiments
            emotions, sentiments = predict(pil_img)

             # Aggregate emotions and sentiments
            for label in emotions_total:
                emotions_total[label] += emotions[label]
            for label in sentiments_total:
                sentiments_total[label] += sentiments[label]
            total_frames += 1

            # Plot and save the results
            fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2)
            ax[0].imshow(frame_rgb)
            ax[0].axis('off')

            # Emotion probabilities
            ax[1].barh(list(emotions.keys()), list(emotions.values()), color='skyblue')
            ax[1].set_xlim(0, 1)
            ax[1].set_title('Emotion Probabilities')

            # Remove the frame around the plot and x-axis ticks
            ax[1].spines['top'].set_visible(False)
            ax[1].spines['right'].set_visible(False)
            ax[1].spines['bottom'].set_visible(False)
            ax[1].spines['left'].set_visible(False)
            ax[1].get_xaxis().set_ticks([])

            # Save the figure to a temporary file and add to outputs
            tmp_file = f'/tmp/frame_{frame_count}.png'
            plt.savefig(tmp_file)
            plt.close(fig)

            outputs.append(tmp_file)

        frame_count += 1

    cap.release()
    emotions_avg = {label: emotions_total[label] / total_frames for label in emotions_total}
    sentiments_avg = {label: sentiments_total[label] / total_frames for label in sentiments_total}
    
    # Recommend based on emotions and sentiments
    recommendation = recommend(emotions_avg, sentiments_avg)  # Implement this function according to your recommendation logic
    # return recommendation
    return recommendation

def recommend(emotions, sentiments):
    # Example recommendation logic: recommend based on the highest emotion probability
    dominant_sentiment = max(sentiments, key=sentiments.get)
    if dominant_sentiment == "positive" or "negative":
        return "The health care professional seems too emotional. Consider taking actions accordingly."
    elif dominant_sentiment == "neutral":
        return "The health care professional did a good job remaining neutral!"


# Gradio interface
title = "Facial Emotion and Sentiment Analyzer for Video Frames"
description = "This tool captures a frame every 5 seconds from the uploaded video, analyzes facial emotions and sentiments, and displays the results along with the frame."

iface = gr.Interface(fn=process_video,
                     inputs=gr.Video(label="Upload Video"),
                     outputs=gr.TextArea(label="Reccomendation"),
                     title=title,
                     description=description,
                     allow_flagging='never')

iface.launch()