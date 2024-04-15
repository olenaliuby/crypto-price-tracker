#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -rf dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/CryptoPriceTracker.app" dist/dmg/
# If the DMG already exists, delete it.
test -f "dist/CryptoPriceTracker.dmg" && rm "dist/CryptoPriceTracker.dmg"
create-dmg \
 --volname "CryptoPriceTracker" \
 --icon "CryptoPriceTracker.app" 200 190 \
 --hide-extension "CryptoPriceTracker.app" \
 --window-pos 200 120 \
 --window-size 800 400 \
 --icon-size 100 \
 --app-drop-link 600 185 \
 "dist/CryptoPriceTracker.dmg" \
 "dist/dmg/"
