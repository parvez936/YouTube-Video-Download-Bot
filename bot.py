# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/YouTube-Video-Download-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot



import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
import instaloader
import youtube_dl
from facebook_scraper import get_posts
import tweepy
from TikTokApi import TikTokApi

# Telegram bot token
TOKEN = '7373482498:AAHXxBWCi-icjzmNJXcGzBzlEy8haN9zHYA'

# Twitter API credentials
TWITTER_CONSUMER_KEY = 'YOUR_TWITTER_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET = 'YOUR_TWITTER_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_SECRET = 'YOUR_TWITTER_ACCESS_SECRET'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a link to download the video.')

def download_youtube_video(url: str) -> str:
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    filename = stream.download()
    return filename

def download_instagram_video(url: str) -> str:
    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context, url.split('/')[-2])
    filename = post.download()
    return filename

def download_twitter_video(url: str) -> str:
    auth = tweepy.OAuth1UserHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    tweet_id = url.split('/')[-1]
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    video_url = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
    response = requests.get(video_url)
    filename = 'twitter_video.mp4'
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

def download_facebook_video(url: str) -> str:
    for post in get_posts(post_urls=[url], options={"comments": False}):
        video_url = post['video']
        response = requests.get(video_url)
        filename = 'facebook_video.mp4'
        with open(filename, 'wb') as f:
            f.write(response.content)
    return filename

def download_tiktok_video(url: str) -> str:
    api = TikTokApi()
    video_data = api.video(url=url)
    video_bytes = video_data.bytes()
    filename = 'tiktok_video.mp4'
    with open(filename, 'wb') as f:
        f.write(video_bytes)
    return filename

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text('Downloading YouTube video...')
        try:
            filename = download_youtube_video(url)
            update.message.reply_text('Uploading video...')
            update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    elif "instagram.com" in url:
        update.message.reply_text('Downloading Instagram video...')
        try:
            filename = download_instagram_video(url)
            update.message.reply_text('Uploading video...')
            update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    elif "twitter.com" in url:
        update.message.reply_text('Downloading Twitter video...')
        try:
            filename = download_twitter_video(url)
            update.message.reply_text('Uploading video...')
            update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    elif "facebook.com" in url:
        update.message.reply_text('Downloading Facebook video...')
        try:
            filename = download_facebook_video(url)
            update.message.reply_text('Uploading video...')
            update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    elif "tiktok.com" in url:
        update.message.reply_text('Downloading TikTok video...')
        try:
            filename = download_tiktok_video(url)
            update.message.reply_text('Uploading video...')
            update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    else:
        update.message.reply_text('Unsupported URL')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
