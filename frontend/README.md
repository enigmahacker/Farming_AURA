# Frontend — UI/UX Plan & Developer Notes

This folder contains the UI/UX plan and wireframe notes for the Farming_AURA mobile app. The app should be built with a farmer-friendly design (Flutter or React Native recommended).

Design Philosophy
- Big fonts and large touch targets
- Hindi-first UI, icons for key actions
- Calm earthy palette (greens, browns, blues)

Key Screens (developer notes)

1. Splash Screen — logo, tagline, fade-in
2. Home Dashboard — today's weather summary, "Today's Advice" card, quick actions
3. Weather Forecast — hourly & 7-day, graphs
4. Crop Recommendations — cards with images, rating, tap for guide
5. Watering Schedule — calendar view & smart suggestions
6. Alerts — color-coded list, tap for advice
7. Knowledge Hub — offline articles & PDFs
8. Settings — language, units, offline toggle

Assets
- Place icons and screen mockups in `frontend/assets/` (not included in prototype). Use large 120x120 icons for primary actions.

Accessibility
- High contrast, voice-over support and large type sizes

Developer tasks to integrate with backend
- Use `/api/` endpoints for user/farm creation, recommendations, weather logs and assistant messages
- Add a local cache for last-known forecast for offline fallback
