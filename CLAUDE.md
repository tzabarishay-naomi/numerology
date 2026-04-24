# נומרולוגיה קבלית — כללים וחישובים

## כללים כלליים
- מערכת נומרולוגיה **קבלית בלבד** (לא פיתגוריאנית)
- שפה: עברית בלבד
- ממשק: RTL
- שמות: גימטריה עברית

---

## ערכי גימטריה עברית
אותיות סופיות = אותה ספרה כמו הרגילות (ך=כ=20, ם=מ=40, ן=נ=50, ף=פ=80, ץ=צ=90)

---

## מספרי מאסטר
11, 22, 33 — **לעולם לא מצמצמים** — **רק בחישובי שביל גורל ותאריך לידה**
שנה אישית וחודש אישי: **תמיד 1–9** (reducePY — מצמצם גם מאסטר)

---

## חישובים בסיסיים

### reduceNumber(n)
צמצום ספרות עד ספרה אחת, תוך שמירה על מאסטר (11/22/33).

### reduceYear(year)
סכום ספרות השנה → reduceNumber

### calcLifePath(day, month, year)
```
d = reduceNumber(day)
m = reduceNumber(month)
y = reduceYear(year)
lp = reduceNumber(d + m + y)
```

---

## שנה אישית

### calcPYForBirthdayYear(birthDay, birthMonth, calYear)
מחשב את מספר השנה האישית שמתחילה ביום ההולדת של calYear:
```
d = reduceNumber(birthDay)
m = reduceNumber(birthMonth)
y = birthMonth <= 6 ? reduceYear(calYear) : reduceYear(calYear + 1)
PY = reduceNumber(d + m + y)
```
**כלל חודש הלידה:** ינואר-יוני → משתמשים בשנה עצמה; יולי-דצמבר → משתמשים בשנה+1

### getCurrentPY(birthDay, birthMonth, checkDate)
```
lastBirthdayYear = (checkDate >= birthdayThisYear) ? cy : cy - 1
return calcPYForBirthdayYear(birthDay, birthMonth, lastBirthdayYear)
```

### חודש אישי
```
PM = reduceNumber(personalYear + currentCalendarMonth)
```

---

## פסגות (Peaks)
```
peak1 = reduceNumber(d + m)
peak2 = reduceNumber(d + y)
peak3 = reduceNumber(d + lp)   ← יום + שביל גורל
peak4 = reduceNumber(m + y)
```

## אתגרים (Challenges)
```
c1 = |d - m|
c2 = |d - y|
c3 = |c1 - c2|
c4 = |m - y|
ch1..ch4 = reduceNumber של כל אחד
```

## גילאי פסגות
נוסחה: `27 − שביל גורל = גיל תחילת פסגה 1`
מאסטר: 11→2, 22→4, 33→6 לצורך חישוב הגיל.
כל פסגה = 9 שנים:
```
peak1: [s, s+8]
peak2: [s+9, s+17]
peak3: [s+18, s+26]
peak4: [s+27, s+35]
```

---

## מספרים קיימים וחסרים
- לוקחים את ספרות המספרים של יום+חודש+שנה (כמחרוזת)
- קיים = ספרות 1-9 שמופיעות (ללא כפילויות)
- חסר = ספרות 1-9 שלא מופיעות

---

## הרמוניה שם-תאריך
3 מספרים: יום (מצומצם), שביל גורל, שם פרטי (גימטריה מצומצמת)

קבוצות הרמוניה:
```
[1,2,3], [4,5,6], [7,8,9]
[1,4,7], [2,5,8], [3,6,9]
[1,5,9], [3,5,7]
```
נורמליזציה: 11→2, 22→4, 33→6

תנאי הרמוניה:
- 2 מהמספרים חולקים קבוצה
- השלישי יכול לעמוד לבד
- הפרש מהשניים המשותפים ≤ 2

---

## ציר זמן (Timeline)
- buildPYTimeline: עבור כל שנה בטווח, מחשב calcPYForBirthdayYear(day, month, yr)
- age = yr - birthYear
- isCurrent: today >= birthday(yr) && today < birthday(yr+1)
- תאים לפני לידה: pyNum = null (תצוגה כסריגה)

---

## קובץ הפרויקט
- `templates/index.html` — **קובץ יחיד, עצמאי לחלוטין** (CSS + JS מוטמעים פנימה)
- נתונים: `localStorage` עם מפתח `'kab_profiles'` (אין שרת, אין Flask)

## הרצת הפרויקט
פתיחת `templates/index.html` ישירות בדפדפן — **ללא שרת**.

---

## reducePY(n)
צמצום תמיד ל-1–9, **ללא** שמירת מאסטר. משמש לשנה אישית וחודש אישי.

---

## ספירלה תלת-ממדית (Canvas 3D)
- Canvas 2D עם השלכת פרספקטיבה ידנית (ללא ספריות חיצוניות)
- היליקס: `x = r·cos(angle)`, `y = -t·Y_RISE`, `z = r·sin(angle)`
- מיון Painter's algorithm לפי עומק
- שליטה: גרירה = סיבוב מצלמה, Ctrl+גרירה = הזזה, גלגלת = זום
- פונקציות מפתח: `draw3DSpiral()`, `_rotate3D()`, `_project3D()`, `setSpiralView(preset)`
- פריסות: `'top'` | `'perspective'` | `'side'`
