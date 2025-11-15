# Frontend Work Division by Pages - 4 Developers

## Overview
This document divides all frontend pages among 4 developers for parallel development.

## Page Breakdown

### Total Pages: 10
1. **Base Template** (`base.html`) - Shared foundation
2. **Home Page** (`index.html`)
3. **Login Page** (`auth/login.html`)
4. **Signup Page** (`auth/signup.html`)
5. **Mission List** (`missions/list.html`)
6. **Mission Detail** (`missions/detail.html`)
7. **Create Mission** (`missions/create.html`)
8. **Profile Page** (`profile/index.html`)
9. **Leaderboard Page** (`leaderboard/index.html`)
10. **Admin Dashboard** (`admin/dashboard.html`)

---

## Developer 1: Base & Authentication Pages

### Pages Assigned:
- [ ] **Base Template** (`templates/base.html`)
  - Navigation bar
  - Footer
  - Flash messages container
  - Base layout structure
  - Block definitions (title, content, extra_css, extra_js)

- [ ] **Home Page** (`templates/index.html`)
  - Hero section
  - Welcome message
  - User stats cards (points, level, major)
  - CTA buttons
  - Recent missions section

- [ ] **Login Page** (`templates/auth/login.html`)
  - Login form
  - Email and password fields
  - Submit button
  - Link to signup page

- [ ] **Signup Page** (`templates/auth/signup.html`)
  - Signup form
  - Name, email, password fields
  - Major/group selection
  - Submit button
  - Link to login page

### CSS Files:
- [ ] `frontend/css/main.css` - Base styles, navigation, footer, buttons, hero section
- [ ] `frontend/css/auth.css` - Authentication page styles

### JavaScript Files:
- [ ] `frontend/js/main.js` - Base utilities, flash message handling, form validation
- [ ] `frontend/js/auth.js` - Login/signup form validation and handling

### Deliverables:
- ✅ Complete navigation system
- ✅ Responsive layout structure
- ✅ Login and signup forms working
- ✅ Homepage with user stats
- ✅ Base styling system for all pages

---

## Developer 2: Mission List & Detail Pages

### Pages Assigned:
- [ ] **Mission List Page** (`templates/missions/list.html`)
  - Mission grid/card layout
  - Category filter buttons
  - Mission cards with:
    - Title
    - Description preview
    - Category badge
    - Status badge
    - Difficulty badge
    - Points display
    - Creator info
    - "View Details" button

- [ ] **Mission Detail Page** (`templates/missions/detail.html`)
  - Full mission title and description
  - Mission metadata (category, difficulty, points, status)
  - Attachment display/download
  - Mission info (creator, dates, assignee)
  - Accept mission button
  - Complete mission button
  - Back to missions button

### CSS Files:
- [ ] `frontend/css/missions.css` - Mission list and detail styling
  - Mission card styles
  - Filter button styles
  - Status badge styles
  - Detail page layout

### JavaScript Files:
- [ ] `frontend/js/missions.js` - Mission list and detail functionality
  - Category filtering
  - Accept/complete confirmation dialogs
  - Dynamic status updates

### Deliverables:
- ✅ Mission feed/list page with filtering
- ✅ Mission detail page with all actions
- ✅ Category filtering working
- ✅ Accept and complete mission functionality
- ✅ Status and difficulty badges styled

---

## Developer 3: Create Mission & Profile Pages

### Pages Assigned:
- [ ] **Create Mission Page** (`templates/missions/create.html`)
  - Mission creation form
  - Title input
  - Description textarea
  - Category dropdown
  - Difficulty dropdown (conditional on category)
  - File upload for attachments
  - Submit button
  - Cancel button

- [ ] **Profile Page** (`templates/profile/index.html`)
  - User header with name
  - Stats display (points, level, major)
  - Completed missions list
  - Created missions list
  - Accepted missions list
  - Mission cards/sections for each category

### CSS Files:
- [ ] `frontend/css/missions.css` - Create mission form styles
- [ ] `frontend/css/main.css` - Profile page styles
  - Profile header
  - Stats cards
  - Mission lists

### JavaScript Files:
- [ ] `frontend/js/missions.js` - Create mission functionality
  - Show/hide difficulty field based on category
  - File upload validation
  - Form validation
- [ ] `frontend/js/main.js` - Profile page utilities (if needed)

### Deliverables:
- ✅ Mission creation form with all fields
- ✅ File upload working
- ✅ Profile page with user stats
- ✅ Three mission lists (completed, created, accepted)
- ✅ Form validation and conditional fields

---

## Developer 4: Leaderboard & Admin Pages

### Pages Assigned:
- [ ] **Leaderboard Page** (`templates/leaderboard/index.html`)
  - Page header with group name
  - User's rank display
  - User's points and level
  - Top 5 users table
  - Rank, name, points, level columns
  - Highlight current user in table

- [ ] **Admin Dashboard** (`templates/admin/dashboard.html`)
  - Admin header
  - Filter form (category, status, creator)
  - All missions table
  - Table columns: Title, Category, Status, Creator, Assignee, Points, Actions
  - Invalidate points button for each completed mission
  - Filter functionality

### CSS Files:
- [ ] `frontend/css/main.css` - Leaderboard and admin styles
  - Leaderboard table
  - Admin dashboard layout
  - Filter form styles
  - Admin table styles

### JavaScript Files:
- [ ] `frontend/js/main.js` - Leaderboard utilities
- [ ] `frontend/js/api.js` - API helpers (if needed for admin)
- [ ] Admin-specific JavaScript (filter handling, confirmations)

### Deliverables:
- ✅ Leaderboard with top 5 users
- ✅ User rank display
- ✅ Admin dashboard with mission table
- ✅ Filter functionality (category, status, creator)
- ✅ Invalidate points functionality

---

## Shared Files & Coordination

### Base Template (`base.html`)
- **Owner:** Developer 1
- **Others:** Coordinate any navigation/structure changes
- **Communication:** Notify team before major layout changes

### Main CSS (`main.css`)
- **Structure:** Use clear section comments
  ```css
  /* ============================================
     Base Styles (Developer 1)
     ============================================ */
  
  /* ============================================
     Profile Styles (Developer 3)
     ============================================ */
  
  /* ============================================
     Leaderboard & Admin Styles (Developer 4)
     ============================================ */
  ```
- **Conflicts:** Use different sections to minimize conflicts

### Main JavaScript (`main.js`)
- **Structure:** Use clear function grouping by developer
- **Communication:** Coordinate shared utilities

---

## File Ownership Summary

| Developer | Pages | CSS Files | JS Files |
|-----------|-------|-----------|----------|
| **Dev 1** | `base.html`, `index.html`, `auth/login.html`, `auth/signup.html` | `main.css` (base), `auth.css` | `main.js` (base), `auth.js` |
| **Dev 2** | `missions/list.html`, `missions/detail.html` | `missions.css` | `missions.js` |
| **Dev 3** | `missions/create.html`, `profile/index.html` | `missions.css`, `main.css` (profile) | `missions.js` |
| **Dev 4** | `leaderboard/index.html`, `admin/dashboard.html` | `main.css` (leaderboard, admin) | `main.js` (admin) |

---

## Git Workflow

### Step 1: Create Feature Branches
```bash
# Everyone pulls latest development
git checkout development
git pull origin development

# Create your feature branch
git checkout -b frontend/dev1-base-auth      # Developer 1
git checkout -b frontend/dev2-mission-list   # Developer 2
git checkout -b frontend/dev3-create-profile # Developer 3
git checkout -b frontend/dev4-board-admin    # Developer 4
```

### Step 2: Work on Your Pages
- Work independently on your assigned pages
- Commit frequently with clear messages
- Push to your feature branch

### Step 3: Merge to Development
```bash
# When ready to merge
git checkout development
git pull origin development
git merge frontend/dev1-base-auth  # Your branch
git push origin development
```

### Step 4: Resolve Conflicts
- `base.html` conflicts: Coordinate with Dev 1
- `main.css` conflicts: Merge sections carefully
- `main.js` conflicts: Coordinate function placement

---

## Testing Checklist (Each Developer)

Before merging, test your pages:
- [ ] Page loads without errors
- [ ] All links work
- [ ] Forms submit correctly
- [ ] Responsive on mobile (< 768px)
- [ ] Responsive on tablet (768px - 1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari (if available)
- [ ] JavaScript console has no errors
- [ ] CSS loads correctly
- [ ] Backend routes work correctly

---

## Timeline Suggestions

### Week 1: Initial Development
- **Dev 1:** Base template + Home page + Auth pages structure
- **Dev 2:** Mission list page layout + Mission detail page layout
- **Dev 3:** Create mission form + Profile page structure
- **Dev 4:** Leaderboard table + Admin dashboard structure

### Week 2: Functionality & Styling
- **Dev 1:** Polish auth pages + Navigation functionality
- **Dev 2:** Category filtering + Accept/complete functionality
- **Dev 3:** File upload + Profile mission lists
- **Dev 4:** Admin filters + Invalidate points functionality

### Week 3: Integration & Polish
- **All:** Test all pages together
- **All:** Fix any integration issues
- **All:** Responsive design refinements
- **All:** Final UX polish

---

## Communication Points

### Daily Standup Questions:
1. What pages did you work on yesterday?
2. Any conflicts or blockers?
3. Need coordination on shared files?
4. Ready to merge today?

### Before Major Changes:
- **Dev 1:** Notify team before changing `base.html` structure
- **All:** Coordinate CSS class naming conventions
- **All:** Agree on color scheme and design tokens
- **All:** Agree on breakpoints (mobile, tablet, desktop)

---

## Quick Reference

| Page | Developer | Status |
|------|-----------|--------|
| `base.html` | Dev 1 | Foundation |
| `index.html` | Dev 1 | Home |
| `auth/login.html` | Dev 1 | Login |
| `auth/signup.html` | Dev 1 | Signup |
| `missions/list.html` | Dev 2 | Mission Feed |
| `missions/detail.html` | Dev 2 | Mission View |
| `missions/create.html` | Dev 3 | Create Mission |
| `profile/index.html` | Dev 3 | User Profile |
| `leaderboard/index.html` | Dev 4 | Leaderboard |
| `admin/dashboard.html` | Dev 4 | Admin Panel |

---

## Notes

- **Base template** is critical - Dev 1 should complete it first
- **CSS conflicts** - Use section comments and coordinate
- **JavaScript conflicts** - Use clear function names and grouping
- **Test together** before final merge to master
- **Keep code consistent** with existing patterns
- **Communicate frequently** to avoid conflicts

