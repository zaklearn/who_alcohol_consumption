# ✅ Deployment Checklist

## Pre-Deployment

- [ ] Python 3.8+ installed
- [ ] pip updated: `pip install --upgrade pip`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Setup verified: `python verify_setup.py` passes
- [ ] Test run: `streamlit run streamlit_app.py` works locally

## Functionality Tests

- [ ] Dashboard loads without errors
- [ ] Language switcher works (EN ↔ FR)
- [ ] "Load WHO Data" button fetches data (~10s)
- [ ] All 6 tabs render correctly:
  - [ ] Overview tab
  - [ ] Consumption tab
  - [ ] Disorders tab
  - [ ] Correlations tab
  - [ ] Regional tab
  - [ ] Export tab
- [ ] Charts are interactive (hover, zoom, pan)
- [ ] Report generation works
- [ ] Download button provides HTML file

## Data Validation

- [ ] Consumption data shows 2000-2022 range
- [ ] Top 10 countries list reasonable
- [ ] World map displays correctly
- [ ] Europe trends show 10 countries
- [ ] Gender comparison has Male/Female data
- [ ] Correlation R² calculates
- [ ] Regional averages non-zero

## Bilingual Tests

- [ ] English: All UI text displays
- [ ] French: All UI text displays
- [ ] Chart titles translate
- [ ] Export in English works
- [ ] Export in French works
- [ ] Language switch preserves data

## Performance

- [ ] Initial load <2 seconds
- [ ] Data fetch <15 seconds
- [ ] Tab switches instant
- [ ] No memory leaks (check after 10+ interactions)
- [ ] Report generates <10 seconds

## Error Handling

- [ ] WHO API timeout handled gracefully
- [ ] Missing data doesn't crash app
- [ ] Invalid inputs rejected
- [ ] Error messages user-friendly
- [ ] Network errors display help text

## Browser Compatibility

- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile responsive

## Production Deploy

### Streamlit Cloud
- [ ] GitHub repo created
- [ ] Connected to Streamlit Cloud
- [ ] Environment variables (if needed)
- [ ] Custom domain (optional)

### Docker (Optional)
- [ ] Dockerfile created
- [ ] Image builds successfully
- [ ] Container runs correctly
- [ ] Port exposed properly

### Local Server
- [ ] Firewall configured
- [ ] SSL certificate (if HTTPS)
- [ ] Reverse proxy setup (nginx)
- [ ] Process management (systemd/pm2)

## Documentation

- [ ] README.md reviewed
- [ ] QUICKSTART.md tested
- [ ] INDEX.md links work
- [ ] Code comments adequate
- [ ] API docs referenced

## Security (Production)

- [ ] No hardcoded credentials
- [ ] API rate limiting considered
- [ ] HTTPS enabled
- [ ] Input validation present
- [ ] Dependencies up-to-date

## Monitoring (Production)

- [ ] Uptime monitoring
- [ ] Error logging
- [ ] Usage analytics
- [ ] Performance metrics

## Final Checks

- [ ] All files committed
- [ ] Version tagged
- [ ] Backup created
- [ ] Team notified
- [ ] User guide shared

## Post-Deployment

- [ ] Health check passed
- [ ] User acceptance testing
- [ ] Feedback collection
- [ ] Bug tracking setup

---

**Sign-off:**
- Developer: _______________  Date: _______
- Tester: _________________  Date: _______
- Approver: _______________  Date: _______

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete
