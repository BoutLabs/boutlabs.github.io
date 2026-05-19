---
layout: project
title: HereNotes
permalink: /projects/herenotes/
order: 3
kind: iOS app
pitch: Location-aware personal notes. The second brain that knows where you were when you wrote things down.
stack: SwiftUI, iOS native, Core Location, iCloud
role: Built end-to-end at Bout Labs
status: In active development
links: []
---

Most note-taking apps treat location as metadata you might surface later, if you remember it exists. HereNotes flips it: the location is part of the note's identity. The note about the coffee shop wifi password lives at the coffee shop. The grocery-list addendum lives at the store. The walk-and-think idea lives along the route where it came up.

## Why we built it

Personal-product team move. The Bout Labs team kept ending up with notes apps full of context-free fragments &mdash; "the thing I noticed", "what they said", "the part to remember" &mdash; written somewhere meaningful and then divorced from the place that made them make sense. HereNotes is the version that doesn't lose the where.

The result feels less like a notebook and more like a quiet annotation layer on the day. Walk past the spot, the note surfaces. Revisit a city, the notes from last time come back with the streets.

## What's in it

- A capture flow that geocodes a note to its location the moment it's written
- An on-device map view that shows the notes laid out as you've laid them down
- Re-surfacing on revisit &mdash; the note about a place pops back when you're back
- Native SwiftUI; iCloud sync between devices; no third-party servers
- Privacy-first: notes stay on your devices and in your iCloud, nowhere else

## What we learned shipping it

(To be written as the app matures. Worth covering here later: the on-device geocoding tradeoffs, the iCloud sync model for location-tagged data, the App Review category fit, and the spatial-UI patterns that made the map view feel like a notebook rather than a tracker.)
