# True/False Swipe Cards - Visual Guide & Usage

## What You'll See

### 1. Mode Selection Screen
When you complete the explanation, you'll see THREE options:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Standard Quiz]  [Adaptive Practice]  [Swipe Cards]  │
│                                                     │
│  Click any button to switch between modes          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2. Swipe Cards View

```
┌─────────────────────────────────────────────────────┐
│  True/False Cards                        1/10       │
│  ████░░░░░░░░░░░░░░░░  (Progress Bar)              │
└─────────────────────────────────────────────────────┘

        ╔═══════════════════════════════════════╗
        ║                                       ║
        ║  FALSE                TRUE            ║
        ║  (opacity increases as you drag)     ║
        ║                                       ║
        ║  "Photosynthesis occurs in animals"  ║
        ║                                       ║
        ║  ← Swipe right for TRUE →            ║
        ║                                       ║
        ║  ← or use buttons below →            ║
        ║                                       ║
        ╚═══════════════════════════════════════╝

        [X FALSE]              [Check TRUE]
        
        Correct Answers: 1/10
```

### 3. After Answering

```
        ╔═══════════════════════════════════════╗
        ║                                       ║
        ║  "Photosynthesis occurs in animals"  ║
        ║                                       ║
        ║  ┌─────────────────────────────────┐ ║
        ║  │ X Incorrect                     │ ║
        ║  │ Photosynthesis primarily occurs │ ║
        ║  │ in plants and algae, not        │ ║
        ║  │ animals.                        │ ║
        ║  └─────────────────────────────────┘ ║
        ║                                       ║
        ║     Loading next question...         ║
        ║                                       ║
        ╚═══════════════════════════════════════╝

        (Auto-advances after 2.5 seconds)
```

### 4. Final Results Screen

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              Quiz Complete!                      │
│                                                     │
│                      8/10                           │
│                     80% Correct                     │
│                                                     │
│              [Try Again]                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## How to Use

### Swipe Gesture (Mobile/Trackpad)
```
Step 1: Place finger/cursor on card
Step 2: Drag RIGHT → Answer is TRUE
        Drag LEFT  → Answer is FALSE
Step 3: Release when you see "TRUE" or "FALSE" label
Step 4: Watch the explanation appear
Step 5: Auto-advance to next card (2.5 sec)
```

### Mouse Controls
```
Step 1: Click [Check TRUE] button to mark as true
        OR click [X FALSE] button to mark as false
Step 2: Card shows explanation
Step 3: Auto-advances (or click [Try Again] if finished)
```

### ⌨️ Keyboard (Future)
Currently not implemented, but could add:
- Q or Right Arrow → TRUE
- E or Left Arrow → FALSE
- Space → Next card

## Animation Breakdown

### 1. Card Entrance
```
Time: 0ms        → 500ms
Opacity: 0%      → 100%
Position: -20px  → 0px
Scale: 95%       → 100%
```

### 2. Drag in Progress
```
As you drag RIGHT:
- Card rotates 5°
- Shadow gets brighter
- "TRUE" label fades in
- Card tilts forward

As you drag LEFT:
- Card rotates -5°
- Card tilts backward
- "FALSE" label fades in
```

### 3. Card Exit (Left Swipe)
```
Swiped LEFT (FALSE answer)
Duration: 300ms
- translateX(-500px)
- rotateY(20°)
- rotateZ(-10°)
- scale 0.8x
- opacity 0%
```

### 4. Card Exit (Right Swipe)
```
Swiped RIGHT (TRUE answer)
Duration: 300ms
- translateX(+500px)
- rotateY(-20°)
- rotateZ(+10°)
- scale 0.8x
- opacity 0%
```

### 5. Explanation Glow
After answering:
```
Correct: Green glow expands/contracts
Incorrect: Red glow expands/contracts
Duration: 1 second
```

## Tips for Best Experience

### For Mobile Users
- Use full-screen mode for better immersion
- Swipe from center of card for best gesture recognition
- Try both swipe and button methods to find your preference

### For Desktop Users
- Use mouse dragging for the most satisfying feel
- Buttons work perfectly too
- Try trackpad swiping if you have a Mac

### For Teachers/Educators
- Great for quick comprehension checks
- Provides immediate feedback
- Students love the gamified approach
- Can track scores across classes

## Performance Notes

- **Statements load**: ~1-2 seconds (API call)
- **Per question**: ~2.5 seconds (auto-advance timer)
- **Completion time**: ~5 minutes for all 10 statements
- **Smooth animations**: 60 FPS on modern devices

## Accessibility

**Mouse Support**: Fully functional buttons
**Touch Support**: Swipe gestures work on tablets/phones
**Keyboard**: Can tab through and click buttons
**Screen Readers**: Semantic HTML (can be improved)
**Color Blind**: Uses text labels + colors (X/Check, TRUE/FALSE)

## Troubleshooting

### Cards won't load?
- Check backend is running: `curl http://localhost:8000/api/v1/tutor/health`
- Check OpenRouter API key in `.env`
- Try refreshing the page

### Swipe not working?
- Make sure you're dragging, not clicking
- Drag at least 50px to register
- Try using the buttons instead

### Statements not relevant?
- The statements are generated from your explanation
- Better explanations = better statements
- Try a different topic

### Animation stuttering?
- Close other tabs/apps
- Check browser console for errors
- Try a different browser

## Sample Topics to Try

Perfect for testing the feature:
- "Photosynthesis" - Biology
- "French Revolution" - History
- "Python lists" - Programming
- "Einstein theory of relativity" - Physics
- "Shakespeare's Hamlet" - Literature
- "Climate change" - Environment
- "Cryptocurrency" - Finance

Try them all to see how the statements vary by topic!

## Stats & Scoring

The component tracks:
- **Current index**: Which card you're on (0-9)
- **User answers**: Map of card index → true/false
- **Correct count**: Total correct answers
- **Score percentage**: (correct/total) × 100

Score appears as:
```
8/10 → 80%
9/10 → 90%
10/10 → 100%
```

## Next Steps

Once you test this feature:
1. Try all three quiz modes with the same topic
2. Compare how you learn with different methods
3. See which mode works best for you
4. Share your feedback!

---

**Ready to swipe? Head to http://localhost:3000 and test it out!**
