# Know Their Names: youth group name quiz

A small web app that helps youth leaders learn every student's name. Add a photo of
each student, then practice with flashcards and quizzes until you know them all.
It's one file with no build step, no dependencies, and no server.

**Open it:** double-click `index.html`, or serve the repo (`python3 -m http.server`)
and visit `http://localhost:8000/name-quiz/`. On a phone, host it anywhere static
(GitHub Pages works) and use "Add to Home Screen."

## How leaders use it

1. **Roster → Add many photos.** Pick a batch of photos. If the files are named after
   the students (`Maya Johnson.jpg`, `maya_johnson.png`), the names fill in on their own.
   Otherwise you type each name. You can also give the whole batch a grade, school,
   gender, or group. **Add one** uses the phone camera directly.
2. **Practice.** Choose a round size, then one of four modes (no game over here):
   - **Flashcards:** see the face, say the name, flip to check, then mark whether you knew it.
   - **Pick the name:** a photo with four names to choose from.
   - **Type the name:** a photo and a text box. The first name, full name, or "goes by"
     name all count, and small typos are accepted.
   - **Find the face:** a name with four photos to choose from.
3. **Build a deck.** On the Practice tab, narrow the deck by group, grade, school, and/or
   gender (for example, "8th grade · Girls · Lincoln Middle"). A filter shows up once at
   least one student has that detail filled in. Every quiz, and the streak challenge,
   uses only the students in the current deck.
4. **Streak challenge.** A game: get names right in a row, and one miss ends it. Choose to
   win at 10 in a row, 25 in a row, or all of the deck (every student once, in random
   order), or play endless. You can answer by picking the name, typing it, or finding the
   face. Correct answers move on automatically. Your best streak is saved for each deck,
   goal, and answer style, and the game-over screen shows the student who stopped you.
5. **Share → Save roster file.** Sends every name and photo to other leaders as one file.
   They open the app and choose **Load a roster file.**

Missed names come back sooner. Each student sits in a Leitner box from 1 to 5: a correct
answer moves them up one box, and a miss sends them back to box 1. Each round starts with
the lowest boxes and the students you've seen least recently. Box 3 and up counts as
"know it" on the progress ring.

## Privacy

These are photos of minors, so the app is built to keep them close:

- Photos are downscaled (560 px, JPEG) and stored **only in the browser's IndexedDB** on
  that device. Nothing is uploaded, and the app makes no network requests at all.
- The only way photos leave the device is a roster file that a leader chooses to save and
  send. The Share screen reminds leaders to send it only to approved leaders and to delete
  it from chats afterward.
- **Share → Delete all students** wipes the device.

Churches usually have a policy on student photos. Follow it, and get parents'
permission where the policy asks for it.

## Trying it out

On a fresh device, **Try it with 12 sample students** loads illustrated (not real) faces
so you can see how the quizzes work. **Roster → Remove the sample students** clears them.
Sample students are never included in a saved roster file.
