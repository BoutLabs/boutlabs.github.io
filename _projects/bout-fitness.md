---
layout: project
title: Bout Fitness
permalink: /projects/bout-fitness/
order: 1
kind: iOS app
pitch: Focused work sessions, modeled as boxing Rounds &mdash; work in the ring, recover in your Corner, never leave the desk for long.
stack: SwiftUI, iOS 18+, Combine, Core Data + optional CloudKit sync, StoreKit 2
role: Built end-to-end at Bout Labs
status: In active development
links: []
---

Most productivity timers split the screen into work and break, and treat the break as the absence of the work. Bout Fitness treats it the other way around: the break is the point. The work happens in *Rounds* &mdash; short, focused intervals &mdash; and the *Corner* is where the day's movement quietly accumulates between them.

The concept is straightforward. Sit down to work, the app starts a Round. When the bell rings, you don't leave the desk &mdash; you do whatever the Corner is showing: a 60-second mobility flow, a posture reset, a stand-up stretch, a quick walk. By the end of the workday, the desk worker has done what most fitness apps demand a separate 45-minute block for.

## Why we built it

Personal-product team move. The Bout Labs team works long sessions at the desk, and watched too many ergonomic + fitness apps fail the same way: they ask for a separate block of time that the user doesn't actually have. Rounds + Corner sneaks the movement *into* the work session, where the time was always going to go.

The other half is structure. Pomodoro-style timers are tools without an opinion. Bout Fitness has opinions &mdash; about what a good Round looks like, what to do in your Corner, when to push and when to recover. The app is the coach, not the stopwatch.

## What's in it

- A focused-work timer built around Rounds (work) and Corners (active recovery)
- A growing library of Corner exercises &mdash; mobility, posture, breath
- Subscription unlocks deeper Corner libraries, personalized Round structure, and longer-term tracking
- Native SwiftUI, no web shell &mdash; the app belongs on the platform it runs on
- Optional CloudKit sync &mdash; your Rounds follow you between devices

## What we learned shipping it

(To be written as the app matures. Notes that belong here include: the Corner-content authoring pipeline, the calibration approach for Round-length defaults, the subscription pricing experiments, and the App Review patterns specific to fitness apps.)
