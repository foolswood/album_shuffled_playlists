#!/usr/bin/env python

from os import listdir
from os.path import isdir, join, dirname
from random import shuffle
from argparse import ArgumentParser

audio_file_extensions = {'flac', 'wav', 'mp3', 'wma'}


def digits_sort_key(filename):
    digits = ''
    for char in filename:
        if char.isdigit():
            digits += char
    if digits:
        return int(digits)
    return 0


def get_tracks(music_dir, artist, album):
    filenames = listdir(join(music_dir, artist, album))
    tracks = []
    for track in sorted(filenames, key=digits_sort_key):
        if track.rsplit('.', 1)[1] in audio_file_extensions:
            tracks.append(f'{artist}\\{album}\\{track}\r\n')
    return ''.join(tracks)


def get_albums(music_dir):
    albums = []
    for artist in listdir(music_dir):
        artist_dir = join(music_dir, artist)
        if not isdir(artist_dir):
            continue
        for album in listdir(artist_dir):
            albums.append(get_tracks(music_dir, artist, album))
    return albums


parser = ArgumentParser(
    description='Generate playlists in album shuffled order')
parser.add_argument(
    '-d', '--music-dir', dest='music_dir', default=dirname(__file__))
parser.add_argument(
    '-n', '--n-playlists', dest='n_playlists', default=8,
    help='Specify the number of shuffled playlists to generate.')
parser.add_argument(
    '-p', '--playlist-base', dest='playlist_base', default='0 album_shuffle',
    help='Beginning of filename for playlist files.')
args = parser.parse_args()

albums = get_albums(args.music_dir)
for n in range(args.n_playlists):
    shuffle(albums)
    with open(join(args.music_dir, f'{args.playlist_base}{n}.m3u8'), 'w') as f:
        for tracklist in albums:
            f.write(tracklist)
