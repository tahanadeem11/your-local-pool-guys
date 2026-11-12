# Your Local Pool Guys website

The finished site is in `site/`. It's plain HTML and CSS, so it works on any web host.

## Editing
All text, services, cities and contact details live in `build.py`. Edit that file, then rebuild:

```
python3 build.py
```

Don't edit the HTML files in `site/` directly; the next build overwrites them.

## Check before going live
- [x] **Hours**: open 7 days, 8am–7pm.
- [x] **Cities**: SFV, Westside LA and Conejo Valley (edit `CITIES` to change).
- [x] **Heater repair page**: confirmed, kept.
- [ ] **Instagram**: assumes @yourlocalpoolguys is on Instagram.
- [ ] **Domain**: assumes https://yourlocalpoolguys.com.
- [ ] **Copy**: read every service page and fix anything that doesn't match how you work.
- [ ] **License number**: if you have a CSLB license, add it to the footer (it builds trust and is required in some ads).

## Going live (Netlify, free)
1. Drag the `site` folder onto app.netlify.com/drop.
2. Connect your domain in Netlify's domain settings.
3. The quote form works automatically on Netlify. Turn on email notifications under Forms → Notifications so submissions reach your inbox.
4. Submit `https://yourlocalpoolguys.com/sitemap.xml` in Google Search Console.

## Biggest SEO wins after launch
1. **Google Business Profile**: set it up as a service-area business with the same name, phone number and cities. This matters more for local search than anything on the site.
2. **Reviews**: once you have Google reviews, add a reviews section to the homepage.
3. **Real photos**: replace the illustrated green-to-clean slider with your own before/after photos, and add job photos to each service page.

## Adding gallery photos and reviews
Both homepage sections stay hidden until you add real content to `build.py`, then rebuild.

**Gallery:** put photos in `site/assets/img/gallery/` (landscape works best). Then add one entry per photo to `GALLERY`:
```
{"src": "/assets/img/gallery/encino-green-to-clean.jpg", "alt": "Encino pool after green-to-clean, clear blue water", "caption": "Green to clean, Encino"},
```

**Reviews:** add real customer reviews to `TESTIMONIALS`, and ask each customer first if you can use their name:
```
{"quote": "Haven't missed a week since we switched.", "name": "Maria G.", "city": "Encino", "stars": 5, "source": "Google"},
```
Or send me the photos and reviews and I'll add them.

## Show-up guarantee
The site promises: "We'll never miss a service, or your whole month is free." Decide what counts as a miss, for example whether weather or a locked gate counts. If you have exceptions, they should be written on the site.
