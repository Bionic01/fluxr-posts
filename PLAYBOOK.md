# Fluxr daily social playbook

This is the source of truth for the daily Fluxr routine. Owner: Rodney (rmjesiman@gmail.com). Timezone: Africa/Johannesburg. Last updated 1 Oct 2026.

## Golden rules (never break)

1. **Approval first.** Never publish or schedule a post, create, activate, pause or change an ad, or spend money until the user replies in chat with a clear yes for that day's set ("post", or "A"/"B" on faces day). Ad suggestions are done only when the user says yes to that numbered suggestion.
2. **Contact.** Use only WhatsApp **+27 60 636 0061**, info@fluxr.co.za and www.fluxr.co.za. Never use +27872658671.
3. **Vouchers.** Only these four: 1Voucher, OTT Voucher, Blu Voucher and FNB Voucher, from R5 at stores. Always show the real logos.
4. **Dial code.**
   - Main code, used on most posts: buy a voucher, dial `*130*31026*VoucherPIN#` (written on pictures as `*130*31026*voucher#`), then follow the menu and enter their number (country code, first 0 dropped).
   - Long code, about 1 post in 4: `*130*31026*VoucherPIN*RecipientNumber#`, with a correct example.
   - Never use the bare `*130*31026#` as the main code.
5. **No made-up facts.** Never invent prices, bundles, promotions or statistics. Use only offers the user gave or that appear in a recent Fluxr post (for example 450MB NetOne data to Zimbabwe for R50, 27 Sep 2026). Never invent Meta targeting IDs.
6. **Best route first.** Prefer the official, legitimate and cheapest option. Don't use AdWhispr (removed).
7. **Rotate countries** and never repeat a country two days running: Zimbabwe, Malawi, Mozambique, Botswana, Lesotho, DRC, Ethiopia, Somalia, Nigeria, Pakistan. Zimbabwe is the biggest market.
8. **Check everything before sending.** Open every picture and sample frames of every video, and proofread every word, code, number and logo.

Country codes and example numbers:

| Country | Code | Example |
|---|---|---|
| Zimbabwe | 263 | 263771234567 |
| Malawi | 265 | 265991234567 |
| Mozambique | 258 | 258841234567 |
| Botswana | 267 | 26771234567 |
| Lesotho | 266 | 26658123456 |
| DRC | 243 | 243812345678 |
| Ethiopia | 251 | 251911234567 |
| Somalia | 252 | 252612345678 |
| Nigeria | 234 | 2348031234567 |
| Pakistan | 92 | 923001234567 |

Also worth posting about now and then:
- The Fluxr app on Google Play.
- Fluxr Agents: 10% commission on customers' international airtime and data for up to five years. People apply by sending "AGENT REQUEST" on WhatsApp to +27 60 636 0061.

## The daily routine (briefing at 07:45 in the main chat)

1. **Ad report** (Meta Ads connector, ad account 657424934810767, ZAR).
   - Cover every ACTIVE ad set whose end time is in the future or empty: spend, reach, frequency, results and cost per result, for yesterday and lifetime.
   - Keep a running comparison of picture styles (code poster vs ElevenLabs vs Canva) by cost per WhatsApp chat.
   - Give numbered suggestions. Change nothing.
2. **Idea.**
   - Check Metricool analytics (FBPO02, FBPO03 and FBPO12, last 14 days) and the scheduled posts, then pick a fresh idea and country.
   - What works: naming a product and price, and opening with a question. Plain greetings perform worst.
3. **Make the set for every platform** (see below): the poster, the short video and per-platform copy.
4. **Review message.** Send the poster and video, the copy for each platform, the times and the ad plan. Ask the user to reply "post", or "A"/"B" on Fridays. Then stop and wait.
5. **After "post".**
   - Schedule everything in Metricool.
   - Create and activate the 7-day WhatsApp ad.
   - Confirm with getScheduledPosts and ads_get_ad_entities, then report back in a few lines.
6. **Keep the chain going.** Before finishing the briefing turn, schedule tomorrow's 07:45 briefing with send_later.

## Platforms (Metricool brand 7157206, all connected)

| Platform | Format | Default time |
|---|---|---|
| Facebook + Instagram | Poster (1080×1350) and the main caption. Instagram `isAiGenerated` is false for code posters and true for ElevenLabs or Canva pictures. | Best hour, usually 10:00 |
| X (@FluxrSA) | Poster plus text of 270 characters or less, with 1–2 hashtags | 10:00 |
| Threads | Poster plus text of 450 characters or less | 10:00 |
| LinkedIn (company page) | A professional angle: financial inclusion, why USSD, agents, partners or milestones. Not a hard sell. 600–1,200 characters, 3–5 hashtags, poster or video | About 11:00 |
| TikTok | The short video, a short caption and 3–5 hashtags | About 18:00 |
| YouTube | The short video as a Short (`youtubeData.type` "short"). Title of 90 characters or less, ending in #Shorts. Description with the steps and contacts. `madeForKids` false | About 16:00 |
| Instagram + Facebook Reels | The short video (optional, ask the user) | Evening |
| Google Business Profile | `gmbData.type` "publication": a text update of 1,500 characters or less, linking to www.fluxr.co.za. **Never put phone numbers in GBP posts (Google rejects them).** Add the poster as a "photo" post about once a week | 09:00 |

Use getBestTimeToPostByNetwork for each network to adjust the times.

**Two posts a day (the user's instruction on 1 Oct 2026).**
- The poster goes out in the morning: Facebook + Instagram, X, Threads and GBP.
- The short video goes out in the evening, about 18:00, as one Metricool post to TikTok, Instagram Reel, Facebook Reel, X and Threads. The video also goes to YouTube as a Short at about 16:00.
- Google Business Profile gets 2 a day (the user's request on 1 Oct 2026): the text update with the poster in the morning, and the video at about 18:00 as a separate `gmbData.type` "photo" post (no text; videos must be 30 seconds or less).
- LinkedIn gets ONE post a day (several posts a day hurt reach there). Use the video with the professional text.
- Use the video's static.metricool.com URL (from the first video post Metricool accepts) for the other video posts, because the ElevenLabs link expires.

## Pictures

- **Mon–Thu, Sat, Sun: code poster.** Run `kit/render.py` (see its docstring and `kit/configs_example.json`). Proofread the PNG, then commit it to `posts/`.
- **Friday is faces day.** Make two versions of the same idea with realistic people:
  - A: ElevenLabs, flow FdwBEZOYHTRRMts7H49b, gpt-image-2 at 1080×1350, with the official logo reference nodes.
  - B: Canva, on the user's current plan. Skip any paid feature and say so.

## Short video (YouTube Shorts, TikTok, Reels)

1. **Write the voiceover script** from the timeline in `kit/video.py`:
   - The hook.
   - "Buy a 1Voucher, OTT, Blu or FNB Voucher."
   - The dial code, spoken as "star, one three zero, star, three one zero two six, star, your voucher PIN, then hash."
   - "Follow the menu…"
   - "Fluxr. No app, no data, any phone."
2. **Generate the voice in ElevenLabs.**
   - Make one flow per day, named "Fluxr shorts - <date> <country>".
   - Use a TTS node with eleven_multilingual_v2 and generations 1.
   - The default voice is "Monique African Queen" (nKSoaggACPsVWCfZyDEv), a warm southern-African female voice. "Grace" (TaC4GDlXCYYbuVG7GsRr) is an alternative.
   - Read the voice's `duration_secs`.
3. **Render the video** in code at the voice length rounded up: set `"duration"` in the config, then run `python3 kit/video.py config.json posts/<date>-<country>-music.mp4 --music`. This adds a quiet music bed and key clicks. Check 5 sample frames with ffmpeg.
4. **Push to GitHub** and attach the video to the flow by its **commit-SHA raw URL**, for example `https://raw.githubusercontent.com/Bionic01/fluxr-posts/<sha>/posts/<file>`. The `main` URL can be cached for about 5 minutes.
5. **Compose.**
   - Add a `composition` node (eleven_composition) with `connect_from` set to [video node, TTS node], then run it.
   - The result's `master_url` is the final video. It expires after about 2 hours, so get a fresh one with creative_get_flow_run_status before scheduling.
6. **Fallback.** If ElevenLabs is unavailable, use the `--music` video on its own (no voice).

## Hosting (computer can be off)

- The workspace cannot upload to most sites, but git push to GitHub works.
- Pictures and videos go to `posts/` in the public repo Bionic01/fluxr-posts, which has the Claude GitHub app installed.
- Use the commit-SHA raw URL as the Metricool media URL. Metricool re-hosts it to static.metricool.com, and that static URL is what Meta ad creatives use.

## Meta ads (one per day, 7 days, minimum budget)

- **Campaign:** ads_create_campaign with objective OUTCOME_ENGAGEMENT, AUCTION, campaign_daily_budget 1634 (R16.34), LOWEST_COST_WITHOUT_CAP and special_ad_categories []. Name it "Fluxr | <country> | <idea> (<Code/ElevenLabs/Canva>) | WhatsApp | 7 Days".
- **Ad set:**
  - IMPRESSIONS billing, optimization_goal CONVERSATIONS and destination_type WHATSAPP.
  - promoted_object {"page_id":"554087821128756"}.
  - Starts at the post time and ends exactly 7 days later.
  - Targeting: ZA (home and recent), ages 18–65, advantage_audience 0.
  - Zimbabwe uses behavior 6019673233983 ("Lived in Zimbabwe (Formerly Expats - Zimbabwe)").
  - Mozambique uses interests 6003698043583 (Mozambique) and 6003320984914 (Remittance).
  - Other countries: use only IDs already found in this account's ad sets. Otherwise target ZA broadly and say so.
- **Creative:**
  - page_id 554087821128756.
  - image_url is the static.metricool.com URL.
  - link_url https://api.whatsapp.com/send and CTA WHATSAPP_MESSAGE.
  - Headline like "Top up family in <country>".
  - Body is the caption without hashtags, ending "Questions? Tap the WhatsApp button and chat to us."
- **Ad:** create it, then activate the campaign, ad set and ad, and confirm.
- **Budget note:** a 7-day ad for every daily post means about 7 overlap, roughly R114/day. Review on 7 Oct.

## Standing items and history

- 30 Sep 2026: "You spoke, we listened!" (120243428430930085) was paused on the user's instruction.
- 7 Oct 2026, 07:30: pause the Malawi (120254232283700085) and Mozambique (120254232336310085) 60-day engagement ad sets. This is already scheduled. Then propose the plan forward.
- Ads running from 30 Sep: Zimbabwe WhatsApp with the ElevenLabs picture (campaign 120254392425900085) and with the Canva picture (120254392547500085), both to 7 Oct. From 1 Oct: Mozambique code poster (120254403091160085), to 8 Oct.
- Metricool upgraded to the Starter plan (about $25/month) on 1 Oct 2026.
