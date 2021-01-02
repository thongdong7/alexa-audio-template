# -*- coding: utf-8 -*-
import os

from data import build_items

WELCOME_MSG = "Welcome to the Home Audio. You can say, play the audio to begin the podcast."
WELCOME_REPROMPT_MSG = "You can say, play the audio, to begin."
WELCOME_PLAYBACK_MSG = "You were listening to {}. Would you like to resume?"
WELCOME_PLAYBACK_REPROMPT_MSG = "You can say yes to resume or no to play from the top"
DEVICE_NOT_SUPPORTED = "Sorry, this skill is not supported on this device"
LOOP_ON_MSG = "Loop turned on."
LOOP_OFF_MSG = "Loop turned off."
HELP_MSG = WELCOME_MSG
HELP_PLAYBACK_MSG = WELCOME_PLAYBACK_MSG
HELP_DURING_PLAY_MSG = "You are listening to the Home Audio. You can say, Next or Previous to navigate through the playlist. At any time, you can say Pause to pause the audio and Resume to resume."
STOP_MSG = "Goodbye."
EXCEPTION_MSG = "Sorry, this is not a valid command. Please say help, to hear what you can say."
PLAYBACK_PLAY = "This is {}"
PLAYBACK_PLAY_CARD = "Playing {}"
PLAYBACK_NEXT_END = "You have reached the end of the playlist"
PLAYBACK_PREVIOUS_END = "You have reached the start of the playlist"

DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_PERSISTENCE_TABLE_NAME']

AUDIO_DATA = [
                 # {
                 #     "title": "VOV 1",
                 #     # "url": "https://stream.vov.vn/audio/vovvn1_vov1.stream_aac/chunklist_w538713446.m3u8",
                 #     "url": "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3",
                 # },
                 # {
                 #     "title": "VOV 5",
                 #     "url": "https://stream.vov.vn/audio/vovvn1_vov5.stream_aac/chunklist_w802153371.m3u8",
                 # },
                 # {
                 #     "title": "VOV Giao thong",
                 #     "url": "https://stream.vov.vn/audio/vovvn1_vovGT.stream_aac/chunklist_w1569574426.m3u8",
                 # }
             ] + [{
    'title': f'Espisode {i+1}',
    'url': item
} for i, item in enumerate(build_items())]
