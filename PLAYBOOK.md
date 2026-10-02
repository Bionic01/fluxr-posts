# Fluxr daily social playbook

This is the source of truth for the daily Fluxr routine. Owner: Rodney (rmjesiman@gmail.com). Timezone: Africa/Johannesburg. Last updated 1 Oct 2026 (night).

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
9. **No AI labels on any post (user, 2 Oct 2026).** Instagram `isAiGenerated` false, YouTube `isAiGeneratedContent` false, TikTok `isAigc` false, and leave the Meta ad creative `self_ai_disclosure` unset. Platforms may still add a label on their own; that's outside our control.

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
- Fluxr Agents (the free Fluxr Agents app on Google Play: https://play.google.com/store/apps/details?id=za.co.fluxr.agents). Agents get an agent code, customers dial *130*31026*AGENTCODE# to link, and agents earn up to 10% when their customers send airtime and data home and 2% on local airtime and data, paid from the customer's 2nd purchase. The top 3 agents win R500, R300 and R100 each month. (Facts as used in the Agents campaign chat, 1 Oct 2026.)

## The daily routine (briefing at 07:45 in the main chat)

1. **Ad report** (Meta Ads connector, ad account 657424934810767, ZAR).
   - Cover every ACTIVE ad set whose end time is in the future or empty: spend, reach, frequency, results and cost per result, for yesterday and lifetime.
   - Keep a running comparison of picture styles (code poster vs ElevenLabs vs Canva) by cost per WhatsApp chat.
   - Give numbered suggestions. Change nothing.
   - **Mondays: voice scoreboard.** Score last week's voices as described in VOICES.md, send the table with one line on who's leading, and recommend whether to change the main voice. Change it only after the user says yes. Plan this week's 7 voices (4 main, 3 test) and write them in the VOICES.md log.
2. **Idea.**
   - Check Metricool analytics (FBPO02, FBPO03 and FBPO12, last 14 days) and the scheduled posts, then pick a fresh idea and country.
   - What works: naming a product and price, and opening with a question. Plain greetings perform worst.
   - **Say it plainly (user, 1 Oct 2026).** Headlines, video hooks and opening lines state what Fluxr does in plain words, for example "Send data to Malawi", "Send airtime to Zimbabwe in seconds" or "Need to send data to Malawi?". No vague or clever phrases like "Weekend data for home?" that make people guess.
3. **Make the set for every platform** (see below): the poster, the short video and per-platform copy.
4. **Review message.** Send the poster and video, the copy for each platform, the times and the ad plan. Ask the user to reply "post", or "A"/"B" on faces days (Mon, Wed, Fri). Then stop and wait.
5. **After "post".**
   - Schedule everything in Metricool.
   - Create and activate the 7-day WhatsApp ad.
   - Confirm with getScheduledPosts and ads_get_ad_entities, then report back in a few lines.
6. **Keep the chain going.** Before finishing the briefing turn, schedule tomorrow's 07:45 briefing with send_later.

## Platforms (Metricool brand 7157206, all connected)

| Platform | Format | Default time |
|---|---|---|
| Facebook + Instagram | Poster (1080×1350) and the main caption. Instagram `isAiGenerated` is always false (no AI labels, see golden rule 9). | Best hour, usually 10:00 |
| X (@FluxrSA) | Poster plus text of 270 characters or less, with 1–2 hashtags | 10:00 |
| Threads | Poster plus text of 450 characters or less | 10:00 |
| LinkedIn (company page) | A professional angle: financial inclusion, why USSD, agents, partners or milestones. Not a hard sell. 600–1,200 characters, 3–5 hashtags, poster or video | About 11:00 |
| TikTok | The short video, a short caption and 3–5 hashtags | About 18:00 |
| YouTube | The short video as a Short (`youtubeData.type` "short"). Title of 90 characters or less, ending in #Shorts. Description with the steps and contacts. `madeForKids` false | About 16:00 |
| Instagram + Facebook Reels | The short video (optional, ask the user) | Evening |
| Google Business Profile | `gmbData.type` "publication": a text update of 1,500 characters or less, linking to www.fluxr.co.za. **Never put phone numbers in GBP posts (Google rejects them).** Add the poster as a "photo" post about once a week | 09:00 |

Use getBestTimeToPostByNetwork for each network to adjust the times.

**Other chats schedule Fluxr posts too (user, 1 Oct 2026: keep the chats working together).** Before planning a day, run getScheduledPosts for that day and include everything already booked in the day's table, whoever made it. Keep this routine's posts at least 1 hour away from those on the same network, and don't duplicate their topic.
- Fluxr Agents campaign (made in the "Flaxa Agent promo videos" chat): Video 1 on Fri 2 Oct 17:00 and Video 2 on Mon 5 Oct 17:00 (Facebook and Instagram Reels, TikTok, YouTube), and 5 picture posts at 12:00 on 3, 4, 6, 7 and 8 Oct (Facebook + Instagram). That chat also has scheduled tasks that prepare paused Agents ads after each video goes out; they wait for the user's go and a daily budget. Include them in the ad report once live.

**Two posts a day (the user's instruction on 1 Oct 2026).**
- The poster goes out in the morning: Facebook + Instagram, X, Threads and GBP.
- The short video goes out in the evening, about 18:00, as one Metricool post to TikTok, Instagram Reel, Facebook Reel, X and Threads. The video also goes to YouTube as a Short at about 16:00.
- Google Business Profile gets 2 a day (the user's request on 1 Oct 2026): the text update with the poster in the morning, and the video at about 18:00 as a separate `gmbData.type` "photo" post (no text; videos must be 30 seconds or less).
- LinkedIn gets ONE post a day (several posts a day hurt reach there). Use the video with the professional text.
- Use the video's static.metricool.com URL (from the first video post Metricool accepts) for the other video posts, because the ElevenLabs link expires.

## Pictures

**Design rules (user, 1 Oct 2026, after a scan of ~130 past Fluxr Facebook pictures):**
- **One Fluxr logo per flyer**, small, top-left. Never a second logo (no logo in the footer).
- **One flag per flyer** (the destination country). No extra SA→country emoji flags.
- Keep text short and leave breathing space: a plain 2–5 word headline that says the service and the country ("Send data to Malawi"), one short sub-line, the code label, the code bar, the voucher logos and the contact footer. No extra pills or taglines.
- Fluxr's own style: a big lifestyle photo of real-looking people (often holding a phone) on top, a curved dark-green panel with a lime rim below, and the headline in white. Palette: dark green #0E3B24, lime #7ED957/#85ED70.

**Which picture on which day (user, 1 Oct 2026):**
- **Mon, Wed, Fri are faces days.** Make two versions of the same idea and the user replies "A" or "B":
  - A: ElevenLabs, flow FdwBEZOYHTRRMts7H49b, gpt-image-2 at 1080×1350, with the official logo reference nodes.
  - B: Canva (the user prefers this look). Use `copy-design` on the 4:5 template **DAHWxzTM-8E** (1080×1350, one logo, clean green panel; edit link https://www.canva.com/d/3_3UM5o6CfiihCY). Swap the photo with `generate-image` + `update_fill` on the photo rect, and change the headline, sub and code with `find_and_replace_text`. Do NOT use resize-design (free trial uses are nearly gone). Do not use the old 1080×1440 design DAHWvUx5c0o (Instagram rejects 3:4, and its green panel image has old text baked in).
  - The faces in both versions are AI-made (Canva's generator is AI too). Tell the user so if it comes up. No AI labels (golden rule 9).
- **Tue, Thu, Sat, Sun: code poster.** Run `kit/render.py` (see its docstring and `kit/configs_example.json`). It now has one logo and one flag. Proofread the PNG, then commit it to `posts/`.
- Skip any paid Canva feature and say so. The user will not pay for Canva.

## Short video (YouTube Shorts, TikTok, Reels)

1. **Write the voiceover script** from the timeline in `kit/video.py`:
   - The hook.
   - "Buy a 1Voucher, OTT, Blu or FNB Voucher."
   - The dial code, spoken as "star, one three zero, star, three one zero two six, star, your voucher PIN, then hash."
   - "Follow the menu…"
   - "Fluxr. No app, no data, any phone."
2. **Generate the voice in ElevenLabs.**
   - Make one flow per day, named "Fluxr shorts - <date> <country>".
   - Use a TTS node with eleven_v4 and generations 1 (eleven_multilingual_v2 only if v4 isn't available in the node).
   - **Voice: follow VOICES.md** (user, 1 Oct 2026). In every 7 videos, use the main voice 4 times and test other southern-African voices the other 3 times, mixing female and male. The main voices for now are "Thobeka Majola" (hjmGn69egwbuNEZ8kska, South African female) and "Darius Voice" (fyDgymp89lRTiPu6iLkM, South African male), alternating. The test pool and IDs are in VOICES.md. Voices must suit the African market and must never sound like AI.
   - Log every video's voice in the VOICES.md log the day it is made.
   - With eleven_v4, add light direction tags such as [warmly] or [excited], use [long pause] between sentences that need a gap, and write the brand as /ˈflʌksə/ so it is said "flux-er". These settings made the Fluxr Agents promo videos (1 Oct 2026) sound natural.
   - Read the voice's `duration_secs`.
3. **Render the video** in code at the voice length rounded up: set `"duration"` in the config, then run `python3 kit/video.py config.json posts/<date>-<country>-voice.mp4 --music --voice`. `--voice` keeps the music bed about 17 dB under the voiceover and leaves out the key clicks (user, 1 Oct 2026: the tones were overpowering the voice). Check 5 sample frames with ffmpeg.
4. **Push to GitHub** and attach the video to the flow by its **commit-SHA raw URL**, for example `https://raw.githubusercontent.com/Bionic01/fluxr-posts/<sha>/posts/<file>`. The `main` URL can be cached for about 5 minutes.
5. **Compose.**
   - Add a `composition` node (eleven_composition) with `connect_from` set to [video node, TTS node], then run it.
   - The result's `master_url` is the final video. It expires after about 2 hours, so get a fresh one with creative_get_flow_run_status before scheduling.
6. **Fallback.** If ElevenLabs is unavailable, render with `--music` only (normal music level and key clicks) and use that video on its own (no voice).

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
  - IDs found in this account so far: Malawi interest 6003288582476; Botswana interest 6002988706250; Zimbabwe interest 6004176068095; Ethiopia interest 6003006728219 and behavior 6018797165983 (Lived in Ethiopia); Nigeria behavior 6018797004183 (Lived in Nigeria); WorldRemit interest 6014750122166; Remittance 6003320984914.
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
- 2 Oct: deleted the unused "Your voucher, their airtime | Foreigners in SA | 14 days" campaign (120254403202960085; its ad was paused, R0 spent) on the user's instruction. The boosted post "Your voucher. Their airtime." (ad set 120254404386660085) keeps running to 7 Oct.
- From 3 Oct: Botswana WhatsApp ad, code poster (campaign 120254433473170085, ad set 120254433475780085), to 10 Oct.
- From 2 Oct: Malawi WhatsApp ad with the Canva picture (campaign 120254423744900085, ad set 120254423747760085), to 9 Oct. Malawi targeting uses interest 6003288582476 ("Malawi"), found in this account's Malawi 60-day ad set.
- Picture-style scoreboard so far (cost per WhatsApp chat): ElevenLabs R3.42 (4 chats) vs Canva R6.66 (2 chats), Zimbabwe, as of 30 Sep.
