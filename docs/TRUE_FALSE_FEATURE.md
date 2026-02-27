# True/False Swipe Cards Feature - Complete Documentation

## Overview
We've added a new **True/False Swipe Card** feature to the AiTutor app! This feature generates 10 true/false statements based on the explanation text and allows students to swipe through them with beautiful animations.

## Features

### Visual Design
- **Modern card design** with gradient backgrounds
- **3D perspective rotation** while dragging
- **Smooth animations** for card transitions
- **Visual feedback** with correct/incorrect explanations
- **Progress bar** showing completion
- **Real-time statistics** tracking correct answers

### Interactions
- **Swipe gestures**: 
  - Swipe RIGHT → Mark as TRUE
  - Swipe LEFT → Mark as FALSE
- **Button controls** for mouse users (Check TRUE and X FALSE buttons)
- **Drag resistance** with threshold detection
- **Disabled state** after answering to prevent re-answering

### Study Features
- **Auto-advance** to next question after 2.5 seconds
- **Explanation display** showing why the answer is correct/incorrect
- **Score tracking** throughout the session
- **Results summary** at the end with percentage

## Architecture

### Backend Components

#### 1. **New Schema Types** (`backend/app/models/schemas.py`)
```python
class TrueOrFalseStatement(BaseModel):
    id: int
    statement: str              # The statement to evaluate
    is_true: bool               # Correct answer: True or False
    explanation: str            # Why it's true or false

class TrueOrFalseRequest(BaseModel):
    topic: str
    explanation: str
    language: str = "en"

class TrueOrFalseResponse(BaseModel):
    topic: str
    statements: list[TrueOrFalseStatement]
```

#### 2. **Service Module** (`backend/app/services/true_false_service.py`)
- **`generate_true_false_statements()`** - Main function that:
  - Takes topic and explanation
  - Calls OpenRouter API to generate 10 statements
  - Mixes TRUE and FALSE statements
  - Returns parsed statements with explanations
  - Has fallback if parsing fails

#### 3. **API Route** (`backend/app/api/routes/tutor.py`)
```python
@router.post("/true-false", response_model=TrueOrFalseResponse)
async def true_false_cards(req: TrueOrFalseRequest):
    """Generate True/False statements from explanation for swipeable cards."""
    return await true_false_service.generate_true_false_statements(
        req.topic, req.explanation, req.language
    )
```

### Frontend Components

#### 1. **Swipeable Card Component** (`frontend/app/components/tutor/TrueOrFalseSwipeCards.tsx`)
Features:
- State management for statements, current index, user answers
- Drag detection with mouse and touch support
- Real-time opacity for swipe indicators (FALSE/TRUE)
- 3D rotation transform based on drag distance
- Auto-advance on answer
- Explanation display
- Score tracking
- Results page with reset button

#### 2. **Animation CSS** (`frontend/app/components/tutor/swipe-animations.css`)
Includes animations for:
- Card entrance (fade + scale)
- Swipe left/right (exit animations with rotation)
- Correct/incorrect glows
- Button pulse effects
- Bounce effects for stats
- Particle effects

#### 3. **App Integration** (`frontend/app/components/tutor/TutorApp.tsx`)
- Added "truefalse" mode to quiz mode selector
- New button "↔️ Swipe Cards" in mode toggle
- Renders `<TrueOrFalseSwipeCards>` when mode is "truefalse"

#### 4. **API Client Update** (`frontend/app/lib/api.ts`)
```typescript
trueOrFalse: (body: TrueOrFalseRequest) =>
  apiFetch<TrueOrFalseResponse>("/api/v1/tutor/true-false", {
    method: "POST",
    body: JSON.stringify(body),
  }),
```

#### 5. **Type Definitions** (`frontend/app/types/index.ts`)
- `TrueOrFalseStatement`
- `TrueOrFalseRequest`
- `TrueOrFalseResponse`

## User Flow

1. **User enters topic** (e.g., "Photosynthesis")
2. **Sees explanation + quiz options** with three modes:
   - Standard Quiz (traditional MCQ)
   - Adaptive Practice (difficulty adapts)
   - Swipe Cards (NEW!)
3. **Clicks "Swipe Cards"**
4. **Backend generates 10 statements** from the explanation
5. **Frontend loads card UI** with progress bar
6. **User swipes or clicks**:
   - Swipe RIGHT / Click TRUE → if correct, show green feedback
   - Swipe LEFT / Click FALSE → if incorrect, show red feedback
7. **Card auto-advances** after 2.5 seconds
8. **Score increments** on correct answers
9. **Final screen shows score** (e.g., 8/10 = 80%)
10. **Can reset and try again**

## Technical Details

### Statement Generation Prompt
The backend uses OpenRouter API with this prompt structure:
- Asks for **10 statements** (mix of TRUE and FALSE)
- Requires statements be **based on the explanation**
- Asks for brief **explanations of why** each is true/false
- Specifies exact format for parsing
- Rates statements as **plausible** (not obvious)

### Drag Physics
```typescript
// Calculate rotation from drag distance
const rotationDeg = (dragX / 150) * 5;  // Max 5° rotation

// Opacity increases as you drag towards true/false
const opacityLeft = Math.max(0, -dragX / 75);   // FALSE (left)
const opacityRight = Math.max(0, dragX / 75);   // TRUE (right)

// Threshold: 50px minimum drag to register
if (Math.abs(dragX) > 50) {
  handleAnswer(dragX > 0);  // Right = True, Left = False
}
```

### Performance Optimizations
- Single API call to generate all 10 statements
- Statements parsed with regex pattern matching
- CSS transforms (GPU-accelerated) for smooth animations
- Fallback question pool if API fails
- Auto-cleanup on component unmount

## Error Handling
- **Network errors**: Shows error message, suggests switching modes
- **Parsing errors**: Falls back to basic statement generation
- **Empty response**: Shows graceful error state
- **No statements**: Displays helpful error message

## Future Enhancements (Optional)
1. **Difficulty levels**: Generate harder/easier statements based on topic complexity
2. **Time tracking**: Show how fast users answered
3. **Leaderboard**: Track best scores across sessions
4. **Customization**: Allow teachers to create custom true/false sets
5. **Keyboard shortcuts**: Q for true/false, arrow keys for navigation
6. **Sound effects**: Optional audio feedback on correct/incorrect
7. **Streak tracking**: Show current correct answer streak
8. **Mobile optimization**: Further optimize for mobile swipe gestures

## Files Modified/Created

### Backend
- Created: `backend/app/services/true_false_service.py` (170 lines)
- Modified: `backend/app/models/schemas.py` (added 3 schema classes)
- Modified: `backend/app/api/routes/tutor.py` (added `/true-false` endpoint)

### Frontend
- Created: `frontend/app/components/tutor/TrueOrFalseSwipeCards.tsx` (280 lines)
- Created: `frontend/app/components/tutor/swipe-animations.css` (140 lines)
- Modified: `frontend/app/components/tutor/TutorApp.tsx` (added mode selector)
- Modified: `frontend/app/lib/api.ts` (added trueOrFalse API method)
- Modified: `frontend/app/types/index.ts` (added 3 type interfaces)

## Testing the Feature

### 1. Start the app
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Navigate to http://localhost:3000 (or 3001)

### 3. Test flow
1. Enter topic: "Photosynthesis"
2. Click "Swipe Cards" button
3. Swipe right for TRUE, left for FALSE
4. Or click the buttons instead
5. Watch the explanation appear after each answer
6. Complete all 10 statements
7. See your final score

### 4. Try different topics
- "World War 2"
- "Python Programming"
- "Quantum Physics"
- "Leonardo da Vinci"

## Summary

This feature adds an **interactive, gamified study method** to the AiTutor platform. The swipe card mechanism is:
- **Engaging**: Fun gesture-based interaction
- **Effective**: Tests true understanding of concepts
- **Fast**: Single API call, ~2-3 second per question
- **Beautiful**: Modern animations and visual feedback
- **Accessible**: Works with mouse, touch, and buttons
- **Reliable**: Graceful fallbacks when APIs fail

Perfect for students who prefer rapid-fire assessment with immediate feedback!
