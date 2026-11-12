#!/usr/bin/env python3
"""Builds the Your Local Pool Guys website into ./site

Edit the BUSINESS, CITIES and SERVICES data below, then run:
    python3 build.py
Every page, the sitemap and the structured data are regenerated from this file.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# ---------------------------------------------------------------------------
# Business details  (CHECK THESE before going live)
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Your Local Pool Guys",
    "url": "https://yourlocalpoolguys.com",          # final domain
    "phone_display": "(818) 857-1463",
    "phone_e164": "+18188571463",
    "email": "yourpoolguy@yourlocalpoolguys.com",
    "owner": "Sebastian Polgar",
    "region": "the San Fernando Valley, Westside LA & Conejo Valley",
    "instagram": "https://www.instagram.com/yourlocalpoolguys",  # handle from business card
    "hours": "Open 7 days, 8am–7pm",
}

CITIES = [
    "Encino", "Sherman Oaks", "Studio City", "Tarzana", "Woodland Hills",
    "Calabasas", "West Hills", "Canoga Park", "Reseda", "Northridge",
    "Porter Ranch", "Granada Hills", "Chatsworth", "Van Nuys",
    "North Hollywood", "Valley Village", "Toluca Lake", "Burbank",
    # Westside LA
    "Brentwood", "Bel Air", "Pacific Palisades", "Beverly Hills",
    # Conejo Valley
    "Agoura Hills", "Westlake Village", "Thousand Oaks",
]

TODAY = date.today().isoformat()
YEAR = date.today().year

# ---------------------------------------------------------------------------
# Icons (simple inline SVG, stroke = currentColor)
# ---------------------------------------------------------------------------
ICON_PATHS = {
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18M9 15l2 2 4-4"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L3 17.7V21h3.3l6.3-6.3a4 4 0 0 0 5.1-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "drop": '<path d="M12 3c3 4 6.5 7.2 6.5 11.2a6.5 6.5 0 0 1-13 0C5.5 10.2 9 7 12 3z"/><path d="M9 14.5a3 3 0 0 0 3 3"/>',
    "pump": '<circle cx="9" cy="14" r="5"/><path d="M14 12h7v4h-7M9 9V4h5M9 14h.01"/>',
    "filter": '<path d="M7 4h10v16H7z"/><path d="M12 2v2M7 8h10M7 12h10M7 16h10"/>',
    "flame": '<path d="M12 3c1 3 5.5 5.2 5.5 10.5a5.5 5.5 0 0 1-11 0c0-3 2-4.5 2.3-6.8C10 8 11 9.3 11 11c1.2-2.2 1.3-4.8 1-8z"/>',
    "waves": '<path d="M3 7c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 12c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 17c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
    "tiles": '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/><path d="M15.5 9.5l-2 2.5 1.8 1.6-1.3 2.4" stroke-width="1.6"/>',
    "bucket": '<path d="M5 9h14l-1.6 11H6.6z"/><path d="M8 9a4 4 0 0 1 8 0M9 13h6"/>',
    "trowel": '<path d="M3 21l6.5-6.5"/><path d="M9.5 14.5L13 4l7 7-10.5 3.5z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "message": '<path d="M21 12a8.5 8.5 0 0 1-12.3 7.6L3 21l1.5-5.4A8.5 8.5 0 1 1 21 12z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "spa": '<path d="M4 13h16v4a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3z"/><path d="M8 9c0-1.5 1-1.5 1-3M12 9c0-1.5 1-1.5 1-3M16 9c0-1.5 1-1.5 1-3"/>',
    "arrows": '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>',
    "quote": '<path d="M4 4h16v12H8l-4 4z"/><path d="M8 9h8M8 12h5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "star": '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
}


def icon(name, cls=""):
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (c, ICON_PATHS[name]))


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------
def P(*paras):
    return "".join("<p>%s</p>" % p for p in paras)


def CHECKS(*items):
    return '<ul class="checks">%s</ul>' % "".join("<li>%s</li>" % i for i in items)


def STEPS(*items):
    return '<ol class="process">%s</ol>' % "".join("<li>%s</li>" % i for i in items)


def CALLOUT(text):
    return '<div class="callout"><p>%s</p></div>' % text


# ---------------------------------------------------------------------------
# Services  (order here = order on the site)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "weekly-pool-spa-service",
        "name": "Weekly Pool & Spa Service",
        "nav": "Weekly Service",
        "icon": "calendar",
        "group": "core",
        "card": "Same day every week: chemicals balanced, pool brushed, skimmed and vacuumed, equipment checked.",
        "title": "Weekly Pool & Spa Service in the San Fernando Valley",
        "desc": "Weekly pool and spa cleaning in the San Fernando Valley and LA. Water testing and balancing, brushing, vacuuming, filter and equipment checks. Free quote: (818) 857-1463.",
        "h1": "Weekly pool & spa service",
        "lead": "A clean, balanced pool every week without you lifting a skimmer. We show up on the same day, take care of the water and the equipment, and tell you if anything needs attention.",
        "body": [
            ("What every weekly visit includes", CHECKS(
                "Test the water and balance chlorine, pH and alkalinity",
                "Skim the surface and empty skimmer and pump baskets",
                "Brush the walls, steps and waterline",
                "Vacuum the floor as needed",
                "Check the pump, filter, heater and timer for leaks, noise or pressure changes",
                "Service the attached spa or stand-alone hot tub at the same visit",
                "Let you know about anything that needs a repair before it becomes expensive",
            )),
            ("Our show-up guarantee", P(
                "Most people switch pool companies for one reason: the pool guy stopped showing up. So we put it in writing. <strong>We'll never miss your scheduled weekly service, or your whole month is free.</strong>",
                "Same day every week, rain or shine. If something ever forces a change, we'll tell you ahead of time and make it up.",
            )),
            ("Why weekly service pays for itself", P(
                "Valley heat, Santa Ana winds and summer storms swing pool chemistry fast. A pool that is checked every week stays ahead of algae and scale, which means fewer green-pool emergencies, longer-lasting plaster and equipment that doesn't have to work as hard.",
                "Catching a small leak at the pump seal or a filter that is running high pressure early is almost always cheaper than replacing the part later.",
            )),
            ("Pools and spas", P(
                "Hot tubs and attached spas run hotter and see heavier use per gallon than a pool, so their water needs closer attention. We include spa care in your route, whether it shares the pool's equipment or has its own.",
            )),
            ("How getting started works", STEPS(
                "<strong>Request a quote.</strong> Call, text or send the form with your address and pool size.",
                "<strong>First visit.</strong> We look at the pool, spa and equipment and go over what it needs.",
                "<strong>Your weekly day.</strong> You're added to a regular route on a set day each week.",
            )),
        ],
        "faqs": [
            ("How much does weekly pool service cost?", "Pricing depends on the size of the pool, whether there's a spa, and how much debris the yard drops in. Call, text or send the form for a free quote for your address."),
            ("What is the show-up guarantee?", "We'll never miss your scheduled weekly service. If we do, you don't pay for that month."),
            ("Do I need to be home for weekly service?", "No. As long as we can reach the gate and the equipment, we can service the pool while you're out."),
            ("Are chemicals included?", "Ask us when you request a quote and we'll spell out exactly what's included for your pool."),
            ("Do you service spas and hot tubs on their own?", "Yes. We service attached spas along with the pool, and stand-alone hot tubs as well."),
        ],
        "related": ["green-to-clean", "filter-replacement", "pool-spa-repair"],
    },
    {
        "slug": "pool-spa-repair",
        "name": "Pool & Spa Repair",
        "nav": "Repairs",
        "icon": "wrench",
        "group": "core",
        "card": "Pumps, filters, heaters, leaks and everything that hums, drips or quits. Diagnosed and fixed.",
        "title": "Pool & Spa Repair in the San Fernando Valley & LA",
        "desc": "Pool and spa equipment repair in the San Fernando Valley and Los Angeles: pumps, motors, filters, heaters, valves and plumbing leaks. Call or text (818) 857-1463.",
        "h1": "Pool & spa repair",
        "lead": "When the pump won't prime, the spa won't heat or the equipment pad is leaking, we find the cause and fix it. You get a clear explanation and a quote before any work starts.",
        "body": [
            ("Repairs we handle", CHECKS(
                '<a href="/services/pump-replacement/">Pool pumps and motors</a>: noisy, leaking, overheating or not priming',
                '<a href="/services/filter-replacement/">Filters</a>: cartridge, D.E. and sand, including tanks, grids and cartridges',
                '<a href="/services/heater-repair/">Pool and spa heaters</a> that won\'t fire or won\'t hold temperature',
                "Valves, unions and leaks at the equipment pad",
                "Timers, controls and equipment that won't come on",
                "Spa jets, blowers and spa-side equipment",
            )),
            ("Signs something needs a repair", CHECKS(
                "Grinding, screeching or humming from the pump",
                "Water around the equipment pad or a wet spot that won't dry",
                "Filter pressure noticeably higher or lower than normal",
                "Weak returns, air in the pump basket or bubbles out of the jets",
                "Spa takes much longer to heat, or doesn't heat at all",
                "Water level dropping faster than evaporation would explain",
            )),
            ("How a repair visit works", STEPS(
                "<strong>Tell us what's happening.</strong> A photo or short video of the equipment helps, and you can text it straight to us.",
                "<strong>Diagnosis.</strong> We inspect the system and find the actual cause, not just the symptom.",
                "<strong>Clear quote.</strong> You see the options and price before we start.",
                "<strong>Fix and test.</strong> We complete the repair and run the system to confirm it's working.",
            )),
        ],
        "faqs": [
            ("Should I repair or replace my pool pump?", "It depends on the age of the pump and what failed. A seal or capacitor is usually worth repairing; an old, loud single-speed pump is often worth replacing with a variable-speed model that uses far less electricity. We'll lay out both options."),
            ("Do you repair equipment if you don't service my pool weekly?", "Yes. Repairs are available whether or not you're on a weekly route."),
            ("Can you look at my spa too?", "Yes. We repair spa heaters, jets, blowers and the plumbing and controls that serve the spa."),
        ],
        "related": ["pump-replacement", "filter-replacement", "heater-repair"],
    },
    {
        "slug": "green-to-clean",
        "name": "Green to Clean Pool Recovery",
        "nav": "Green to Clean",
        "icon": "drop",
        "group": "core",
        "card": "Swamp to swimmable. We clear algae, rebalance the water and get the filter caught up.",
        "title": "Green Pool Cleanup (Green to Clean) | San Fernando Valley",
        "desc": "Green pool? Our green-to-clean service clears algae, cleans the filter and rebalances the water so your pool is clear and swimmable again. San Fernando Valley & LA.",
        "h1": "Green to clean pool recovery",
        "lead": "A green pool isn't a lost cause. We kill the algae, clean out the debris and filter, rebalance the water and bring it back to clear, then keep it that way with weekly service if you'd like.",
        "slider": True,
        "body": [
            ("When you need a green-to-clean", CHECKS(
                "The water is green, cloudy or you can't see the floor",
                "The pool sat while a house was empty, for sale or being remodeled",
                "The pump or filter was down for a while",
                "A storm or heat wave pushed chemistry out of balance",
                "You just bought a home with a neglected pool",
            )),
            ("How we bring it back", STEPS(
                "<strong>Remove debris.</strong> Leaves and sludge come out first so chemicals go to work on algae, not dirt.",
                "<strong>Shock and treat.</strong> We dose the water to kill algae and break down organic material.",
                "<strong>Brush everything.</strong> Walls, floor, steps and corners, to knock algae loose.",
                "<strong>Filter and clean the filter.</strong> The filter works hard during a recovery, so it gets cleaned as dead algae is pulled out.",
                "<strong>Vacuum and rebalance.</strong> Once the water clears, we vacuum what has settled and balance the chemistry.",
                "<strong>Follow-up visits.</strong> We return until the water is clear and stable.",
            )),
            ("How long does it take?", P(
                "Most pools clear within a few visits, but timing depends on how far gone the water is, the size of the pool and how well the filter and pump are working. If equipment is part of the problem, we'll tell you up front.",
            ) + CALLOUT("Selling a home? A clear pool photographs better and avoids a red flag at inspection. Ask about getting the pool ready before listing photos.")),
        ],
        "faqs": [
            ("Do you need to drain a green pool?", "Usually not. Most green pools can be cleared with treatment, brushing and filtration. Draining is only needed in specific cases, like very high dissolved solids or when an acid wash is planned."),
            ("Why did my pool turn green so fast?", "Algae grows quickly when chlorine drops, especially in summer heat. A failed pump, a skipped week or a heavy storm is often all it takes."),
            ("Is a green pool dangerous?", "It's not safe to swim in, and stagnant water can attract mosquitoes. It's worth fixing quickly."),
        ],
        "related": ["weekly-pool-spa-service", "acid-wash", "filter-replacement"],
    },
    {
        "slug": "pump-replacement",
        "name": "Pool Pump Replacement",
        "nav": "Pump Replacement",
        "icon": "pump",
        "group": "repair",
        "card": "Loud, leaking or dead pump? We replace it, often with an energy-saving variable-speed model.",
        "title": "Pool Pump Replacement & Repair | San Fernando Valley",
        "desc": "Pool pump replacement and repair in the San Fernando Valley and LA. Variable-speed pump upgrades, motor and seal repair. Call or text (818) 857-1463 for a free quote.",
        "h1": "Pool pump replacement",
        "lead": "The pump keeps your water moving through the filter, and when it fails, the pool goes downhill fast. We repair what can be repaired and replace what can't, sized correctly for your pool.",
        "body": [
            ("Signs your pump is failing", CHECKS(
                "Loud grinding or screeching (usually worn motor bearings)",
                "Humming but not starting",
                "Water leaking from the pump or under the motor",
                "Trouble priming or air in the pump basket",
                "Tripping the breaker",
                "Weak circulation even with clean baskets and filter",
            )),
            ("Variable-speed pumps", P(
                "Older single-speed pumps run at full power all the time. A variable-speed pump can run slower for longer, which moves the same water while using much less electricity. In California, replacement pool pumps generally need to meet current energy efficiency rules, so most replacements today are variable-speed.",
                "We'll recommend a pump that fits your pool size, plumbing and equipment, not just the biggest one available.",
            )),
            ("What's included", STEPS(
                "<strong>Diagnosis.</strong> Confirm whether the pump, the motor or something else is the real problem.",
                "<strong>Options and quote.</strong> Repair versus replacement, with prices for each where both make sense.",
                "<strong>Installation.</strong> Remove the old pump, plumb and wire the new one, check unions and seals.",
                "<strong>Startup.</strong> Prime, set speeds and schedule, and confirm good flow through the filter.",
            )),
        ],
        "faqs": [
            ("How long do pool pumps last?", "Many pumps last around 8 to 12 years, depending on use, maintenance and conditions at the equipment pad. Motors and seals often fail before the pump housing."),
            ("Is a variable-speed pump worth it?", "For most pools, yes. They're quieter and typically use much less electricity than older single-speed pumps."),
            ("Can you just replace the motor?", "Sometimes. If the housing and impeller are in good shape, a motor replacement can make sense. We'll tell you which option is better value."),
        ],
        "related": ["filter-replacement", "heater-repair", "pool-spa-repair"],
    },
    {
        "slug": "filter-replacement",
        "name": "Pool Filter Replacement & Cleaning",
        "nav": "Filter Replacement",
        "icon": "filter",
        "group": "repair",
        "card": "Cartridge, D.E. and sand filters: cleaned, rebuilt or replaced so the water stays clear.",
        "title": "Pool Filter Replacement & Cleaning | San Fernando Valley",
        "desc": "Pool filter replacement, cartridge replacement and filter cleaning for cartridge, D.E. and sand filters in the San Fernando Valley and Los Angeles. Free quote.",
        "h1": "Pool filter replacement & cleaning",
        "lead": "A clogged or broken filter means cloudy water, a struggling pump and more chemicals. We clean, rebuild and replace cartridge, D.E. and sand filters.",
        "body": [
            ("Signs your filter needs attention", CHECKS(
                "Pressure gauge reading well above its clean starting pressure",
                "Cloudy water that won't clear even with balanced chemistry",
                "D.E. or sand blowing back into the pool",
                "Torn, flattened or crumbling cartridges",
                "Cracked tank, leaking band clamp or a broken gauge",
            )),
            ("What we do", CHECKS(
                "<strong>Filter cleaning:</strong> cartridges hosed and degreased, D.E. grids broken down and cleaned, sand filters backwashed",
                "<strong>Cartridge and grid replacement</strong> when the media is worn out",
                "<strong>Full filter replacement</strong> when the tank is cracked or the filter is undersized",
                "<strong>O-rings, gauges and air relief valves</strong> replaced as needed",
            )),
            ("How often should a filter be cleaned?", P(
                "Most residential filters need a full cleaning a few times a year, and more often after a green-to-clean or heavy storms. If you're on weekly service, we watch the pressure for you and tell you when it's time.",
            )),
        ],
        "faqs": [
            ("How often should pool filter cartridges be replaced?", "It depends on use and how often they're cleaned, but cartridges commonly last a few years. When they're torn, flattened or no longer clean up, it's time."),
            ("Which filter type is best?", "Cartridge filters are common and easy to maintain, D.E. filters filter the finest particles, and sand filters are simple and durable. We'll talk through what fits your pool."),
            ("Why is my filter pressure high?", "Usually the filter is dirty. If pressure is still high right after cleaning, there may be a restriction in the plumbing or a problem with the media."),
        ],
        "related": ["pump-replacement", "green-to-clean", "weekly-pool-spa-service"],
    },
    {
        "slug": "heater-repair",
        "name": "Pool & Spa Heater Repair",
        "nav": "Heater Repair",
        "icon": "flame",
        "group": "repair",
        "card": "Heater won't fire or won't hold temperature? We troubleshoot gas heaters and heat pumps.",
        "title": "Pool & Spa Heater Repair | San Fernando Valley & LA",
        "desc": "Pool and spa heater repair in the San Fernando Valley and LA. Troubleshooting for gas heaters and heat pumps that won't ignite or won't heat. Call (818) 857-1463.",
        "h1": "Pool & spa heater repair",
        "lead": "A cold spa on a cold night is no fun. We troubleshoot pool and spa heaters, fix what's fixable and tell you straight when a replacement makes more sense.",
        "body": [
            ("Common heater problems", CHECKS(
                "Heater won't turn on or shows an error code",
                "Ignites, then shuts off",
                "Takes far longer to heat than it used to",
                "Leaking water at the heater",
                "Soot, rust or a burnt smell",
            )),
            ("What we check", P(
                "Many heater problems start somewhere else: low water flow from a dirty filter or a failing pump, a pressure switch that isn't closing, or a settings issue on the controls. We check the whole system so the fix lasts.",
            )),
        ],
        "faqs": [
            ("Why won't my pool heater turn on?", "Common causes include low flow from a dirty filter, a faulty pressure switch, ignition problems or controls set incorrectly. A diagnosis pinpoints which."),
            ("Do you work on heat pumps?", "We troubleshoot both gas heaters and heat pumps. Some repairs may need manufacturer parts or service, and we'll let you know if that's the case."),
        ],
        "related": ["pump-replacement", "filter-replacement", "pool-spa-repair"],
    },
    {
        "slug": "tile-cleaning",
        "name": "Pool Tile Cleaning",
        "nav": "Tile Cleaning",
        "icon": "waves",
        "group": "renovation",
        "card": "White calcium lines and scale removed from the waterline so your tile looks new again.",
        "title": "Pool Tile Cleaning & Calcium Removal | Valley & LA",
        "desc": "Pool tile cleaning and calcium removal in the San Fernando Valley. We remove white scale and waterline stains from pool and spa tile. Free quote: (818) 857-1463.",
        "h1": "Pool tile cleaning & calcium removal",
        "lead": "Hard Valley water leaves white calcium lines along the waterline that brushing won't touch. We remove scale and staining so the tile looks the way it did when it was installed.",
        "body": [
            ("What causes the white line?", P(
                "As pool water evaporates, the minerals in it stay behind and bond to the tile. Over time that builds into a crusty white or gray band of calcium scale. High pH and high calcium hardness speed it up.",
            )),
            ("Our tile cleaning process", STEPS(
                "<strong>Inspect the tile</strong> and grout to choose the right method for the type of buildup.",
                "<strong>Remove scale</strong> using methods suited to your tile, to avoid scratching glass or glazed finishes.",
                "<strong>Clean the grout lines</strong> and rinse the area.",
                "<strong>Rebalance the water</strong> so scale comes back as slowly as possible.",
            )),
            ("Keeping it clean", P(
                "Balanced water is the best prevention. On weekly service, we brush the waterline and keep pH and calcium in check, so heavy buildup takes much longer to form.",
            )),
        ],
        "faqs": [
            ("Can calcium buildup damage my tile?", "Left long enough, heavy scale can be harder to remove and may pit or dull some finishes. Removing it earlier is easier on the tile."),
            ("Will tile cleaning damage glass tile?", "We choose methods based on the tile type. Glass and glazed tile need a gentler approach than stone or unglazed tile."),
            ("Do I need to drain the pool for tile cleaning?", "Usually the water is lowered slightly below the tile line rather than fully drained."),
        ],
        "related": ["tile-repair", "acid-wash", "weekly-pool-spa-service"],
    },
    {
        "slug": "tile-repair",
        "name": "Pool Tile Repair",
        "nav": "Tile Repair",
        "icon": "tiles",
        "group": "renovation",
        "card": "Loose, cracked or missing waterline tile reset and replaced before water gets behind it.",
        "title": "Pool Tile Repair & Replacement | San Fernando Valley",
        "desc": "Pool tile repair in the San Fernando Valley and LA. Loose, cracked and missing waterline tiles reset or replaced, plus grout repair. Call or text (818) 857-1463.",
        "h1": "Pool tile repair",
        "lead": "A few loose or cracked tiles can let water behind the tile line, which loosens more tile over time. We reset and replace tile and repair grout to keep your waterline solid.",
        "body": [
            ("Signs you need tile repair", CHECKS(
                "Tiles that are loose, hollow-sounding or have fallen into the pool",
                "Cracked or chipped tiles at the waterline or on steps",
                "Missing or crumbling grout",
                "Gaps between the tile and the coping",
            )),
            ("What we do", STEPS(
                "<strong>Inspect the tile line</strong> to find every loose tile, not just the obvious ones.",
                "<strong>Lower the water</strong> below the repair area.",
                "<strong>Remove and reset</strong> loose tile, or replace damaged tile with the closest available match.",
                "<strong>Grout and cure</strong> before the water is brought back up.",
            )),
            CALLOUT("Have spare tiles from when the pool was built? Set them aside for us. Matching older tile is the hardest part of a repair."),
        ],
        "faqs": [
            ("Can you match my existing tile?", "We'll try to match it as closely as possible. If your original tile is discontinued, spare tiles from the original install or a complementary accent are the best options."),
            ("Is it worth fixing just a few tiles?", "Yes. Fixing a few loose tiles now helps keep water from getting behind the rest of the tile line."),
        ],
        "related": ["tile-cleaning", "replastering", "acid-wash"],
    },
    {
        "slug": "acid-wash",
        "name": "Pool Acid Wash",
        "nav": "Acid Wash",
        "icon": "bucket",
        "group": "renovation",
        "card": "Drain-and-clean treatment that removes stains and a thin layer of plaster to brighten the finish.",
        "title": "Pool Acid Wash & Drain and Clean | San Fernando Valley",
        "desc": "Pool acid wash and drain-and-clean service in the San Fernando Valley and Los Angeles. Brightens stained, dull plaster. Get a free quote: (818) 857-1463.",
        "h1": "Pool acid wash",
        "lead": "When stains and discoloration have set into the plaster, an acid wash can bring back a brighter finish. The pool is drained and a thin layer of the surface is cleaned away to reveal the fresher plaster underneath.",
        "body": [
            ("When an acid wash makes sense", CHECKS(
                "Algae or mineral stains that don't come out with brushing or treatment",
                "Dull, gray or blotchy plaster",
                "After a severe green pool or long period of neglect",
                "High dissolved solids that call for draining and refilling anyway",
            )),
            ("How an acid wash works", STEPS(
                "<strong>Drain the pool</strong> safely and in line with local rules for draining.",
                "<strong>Clean out debris</strong> from the floor and drains.",
                "<strong>Acid wash</strong> the surface in sections and rinse thoroughly.",
                "<strong>Neutralize and clean up</strong> the wash water.",
                "<strong>Refill and start up</strong> with balanced water chemistry.",
            )),
            ("Is an acid wash right for your pool?", P(
                "Every acid wash removes a thin layer of plaster, so it isn't something to repeat often. If the plaster is thin, rough or delaminating, <a href=\"/services/replastering/\">replastering</a> may be the better investment. We'll look at the surface and tell you honestly which makes sense.",
            )),
        ],
        "faqs": [
            ("How often can a pool be acid washed?", "Sparingly. Because each wash removes some plaster, it's best saved for when stains can't be removed any other way."),
            ("Will an acid wash remove all stains?", "It removes many surface stains, but some deep metal or organic stains may remain. We'll set expectations before we start."),
            ("How long is the pool out of service?", "Draining, washing and refilling are usually done over a few days, depending on the pool size and fill rate."),
        ],
        "related": ["replastering", "green-to-clean", "tile-cleaning"],
    },
    {
        "slug": "replastering",
        "name": "Pool Replastering & Resurfacing",
        "nav": "Replastering",
        "icon": "trowel",
        "group": "renovation",
        "card": "Rough, etched or stained plaster replaced with a smooth new finish that looks and feels like new.",
        "title": "Pool Replastering & Resurfacing | San Fernando Valley",
        "desc": "Pool replastering and resurfacing in the San Fernando Valley and Los Angeles. Replace rough, etched or stained plaster with a fresh new finish. Free quote.",
        "h1": "Pool replastering & resurfacing",
        "lead": "Plaster doesn't last forever. When the surface is rough on your feet, etched, chalky or permanently stained, replastering gives the pool a smooth new finish and a fresh look.",
        "body": [
            ("Signs it's time to replaster", CHECKS(
                "Rough plaster that scratches feet or snags swimsuits",
                "Etching, pitting or chalky residue",
                "Stains that won't come out with an acid wash",
                "Hollow spots, delamination or exposed gunite",
                "Cracks in the surface",
            )),
            ("What the project involves", STEPS(
                "<strong>Drain and prep.</strong> The pool is drained and the old surface is prepared so the new plaster bonds well.",
                "<strong>Tile and fittings.</strong> A good time to address tile repair and replace fittings if needed.",
                "<strong>Apply the new finish.</strong> Fresh plaster or an upgraded finish is applied and smoothed.",
                "<strong>Fill and start up.</strong> The pool is refilled and the new surface is carefully brought up with a proper start-up chemistry plan.",
            )),
            ("Finish options", P(
                "Classic white plaster gives the familiar bright blue water. Colored plasters and aggregate finishes (quartz or pebble) can last longer and change the water color. We'll walk you through the options and what fits your budget.",
            ) + CALLOUT("Start-up care matters. New plaster needs closely managed water chemistry for its first weeks, and that's exactly what weekly service is for.")),
        ],
        "faqs": [
            ("How long does pool plaster last?", "Standard white plaster often lasts around 10 to 15 years with good water chemistry. Aggregate finishes can last longer."),
            ("How long does replastering take?", "Most projects take about one to two weeks from draining to refill, depending on the pool and the finish."),
            ("Should I fix tile at the same time?", "If tile is loose or damaged, replastering is the ideal time, since the pool is already drained."),
        ],
        "related": ["acid-wash", "tile-repair", "weekly-pool-spa-service"],
    },
]

SVC = {s["slug"]: s for s in SERVICES}
GROUPS = [
    ("core", "Weekly service & repairs"),
    ("repair", "Equipment"),
    ("renovation", "Tile, plaster & surfaces"),
]

HOME_FAQS = [
    ("What areas do you serve?", "We serve the San Fernando Valley, Westside LA and the Conejo Valley, including %s. Not sure if you're in range? Call or text and ask." % ", ".join(CITIES[:8])),
    ("Do you service spas and hot tubs?", "Yes. Spas are part of weekly service, and we repair spa heaters, jets and equipment too."),
    ("Do you only do weekly service, or one-time jobs too?", "Both. We do one-time jobs like green-to-clean recoveries, acid washes, tile work and equipment replacement, whether or not you're on a weekly route."),
    ("How do I get a quote?", "Call or text %s, or send the quote form with your address and what you need. Photos of the pool or equipment help us quote faster." % BUSINESS["phone_display"]),
]

HOME_FAQS.insert(1, ("What is your show-up guarantee?",
    "We'll never miss your scheduled weekly service. If we do, you don't pay for that month."))

# ---------------------------------------------------------------------------
# Gallery & reviews: REAL content only. Sections stay hidden while these are empty.
#
# GALLERY: put photos in site/assets/img/gallery/ then add entries like:
#   {"src": "/assets/img/gallery/encino-green-to-clean.jpg",
#    "alt": "Green pool in Encino after cleanup, clear blue water",
#    "caption": "Green to clean, Encino"},
#
# TESTIMONIALS: copy real reviews (with the customer's OK), e.g. from Google:
#   {"quote": "Never missed a week since we switched.", "name": "Maria G.",
#    "city": "Encino", "stars": 5, "source": "Google"},
# ---------------------------------------------------------------------------
GALLERY = [
    {"src": "/assets/img/gallery/cleanup-before-after.jpg", "w": 1200, "h": 904,
     "alt": "Before and after: a cloudy pool full of debris cleaned up to clear blue water",
     "caption": "Cleanup: before and after"},
    {"src": "/assets/img/gallery/pool-spa-weekly-1.jpg", "w": 900, "h": 1200,
     "alt": "Clear blue pool with blue waterline tile, brick coping and attached spa",
     "caption": "Pool & spa on weekly service"},
    {"src": "/assets/img/gallery/pool-spa-weekly-2.jpg", "w": 900, "h": 1200,
     "alt": "Sparkling pool with attached spa and tiled steps on a sunny day",
     "caption": "Clean water, every week"},
]
TESTIMONIALS = []

# Real "before" photos from green-to-clean jobs (shown on the green-to-clean page).
GTC_BEFORE = [
    {"src": "/assets/img/gallery/green-before-2.jpg", "w": 1200, "h": 900,
     "alt": "Rectangular pool with cloudy green water and floating debris, before cleanup",
     "caption": "Bright green, can't see the floor"},
    {"src": "/assets/img/gallery/green-before-3.jpg", "w": 900, "h": 1200,
     "alt": "Murky brown-green pool with algae stains along the walls, before cleanup",
     "caption": "Murky water, stained walls"},
]

# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
BIZ_ID = BUSINESS["url"] + "/#business"


def business_ld():
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": BIZ_ID,
        "name": BUSINESS["name"],
        "url": BUSINESS["url"] + "/",
        "telephone": BUSINESS["phone_e164"],
        "email": BUSINESS["email"],
        "logo": BUSINESS["url"] + "/assets/img/mark-512.png",
        "image": BUSINESS["url"] + "/assets/img/og-image.jpg",
        "founder": {"@type": "Person", "name": BUSINESS["owner"]},
        "areaServed": [{"@type": "City", "name": c + ", CA"} for c in CITIES],
        "sameAs": [BUSINESS["instagram"]],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "08:00", "closes": "19:00"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Pool and spa services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                   "url": BUSINESS["url"] + "/services/%s/" % s["slug"]}}
                for s in SERVICES
            ],
        },
    }


def faq_ld(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def crumbs_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                             "item": BUSINESS["url"] + u} for i, (n, u) in enumerate(items)],
    }


def ld_script(nodes):
    data = {"@context": "https://schema.org", "@graph": nodes}
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


# ---------------------------------------------------------------------------
# Shared page parts
# ---------------------------------------------------------------------------
NAV = [
    ("/services/weekly-pool-spa-service/", "Weekly Service"),
    ("/services/pool-spa-repair/", "Repairs"),
    ("/services/green-to-clean/", "Green to Clean"),
    ("/services/", "All Services"),
    ("/service-area/", "Service Area"),
    ("/contact/", "Contact"),
]

TEL = "tel:" + BUSINESS["phone_e164"]
SMS = "sms:" + BUSINESS["phone_e164"]


def head(title, desc, path, ld=None, noindex=False):
    url = BUSINESS["url"] + path
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}/assets/img/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A2147">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">
{ld}
</head>
""".format(title=esc(title), desc=esc(desc), robots=robots, url=url, name=esc(BUSINESS["name"]),
           base=BUSINESS["url"], ld=ld_script(ld) if ld else "")


def header(active):
    links = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if u == active else "", esc(n))
        for u, n in NAV)
    return """<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{name} home">
      <img src="/assets/img/logo.png" srcset="/assets/img/logo.png 1x, /assets/img/logo@2x.png 2x" width="520" height="288" alt="{name}">
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{menu}<span class="visually-hidden">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
    </nav>
    <a class="btn btn-sun header-phone" href="{tel}">{phone_icon}{phone}</a>
  </div>
</header>
""".format(name=esc(BUSINESS["name"]), menu=icon("menu"), links=links, tel=TEL,
           phone_icon=icon("phone"), phone=BUSINESS["phone_display"])


def footer():
    core = "".join('<li><a href="/services/%s/">%s</a></li>' % (s["slug"], esc(s["nav"]))
                   for s in SERVICES if s["group"] == "core")
    more = "".join('<li><a href="/services/%s/">%s</a></li>' % (s["slug"], esc(s["nav"]))
                   for s in SERVICES if s["group"] != "core")
    return """<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap cta-inner">
    <div>
      <h2 id="cta-title">Let's talk pools.</h2>
      <p>Call or text {phone} for a free quote. You'll talk to the person who does the work.</p>
    </div>
    <div class="btn-row">
      <a class="btn btn-navy" href="{tel}">{pi}Call {phone}</a>
      <a class="btn btn-ghost" href="{sms}">{mi}Text us</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="footer-logo" href="/"><img src="/assets/img/logo.png" width="520" height="288" alt="{name}" loading="lazy"></a>
        <p><a class="footer-phone" href="{tel}">{phone}</a><br>
        <a href="mailto:{email}">{email}</a><br>
        Serving {region}<br>{hours}</p>
      </div>
      <div><h2>Services</h2><ul>{core}<li><a href="/services/">All services</a></li></ul></div>
      <div><h2>Repairs &amp; renovation</h2><ul>{more}</ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="/service-area/">Service area</a></li>
        <li><a href="/contact/">Contact &amp; free quote</a></li>
        <li><a href="{ig}" rel="noopener">Instagram</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {year} {name}. All rights reserved.</span>
      <span>Pool &amp; spa service in the San Fernando Valley, Westside LA &amp; Conejo Valley</span>
    </div>
  </div>
</footer>
<nav class="action-bar" aria-label="Quick contact">
  <a href="{tel}">{pi}Call</a>
  <a href="{sms}">{mi}Text</a>
  <a class="primary" href="/contact/#quote">{qi}Free quote</a>
</nav>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
""".format(phone=BUSINESS["phone_display"], tel=TEL, sms=SMS, pi=icon("phone"), mi=icon("message"),
           qi=icon("quote"), name=esc(BUSINESS["name"]), email=BUSINESS["email"],
           region=esc(BUSINESS["region"]), hours=esc(BUSINESS["hours"]), core=core, more=more,
           ig=BUSINESS["instagram"], year=YEAR)


def quote_form(heading="Get a free quote", sub="Tell us about your pool. We usually reply the same day.", hid="quote", preselect=None):
    opts = ['<option value="">Choose a service</option>']
    for s in SERVICES:
        sel = " selected" if preselect == s["slug"] else ""
        opts.append('<option value="%s"%s>%s</option>' % (esc(s["name"]), sel, esc(s["name"])))
    opts.append('<option value="Something else">Something else</option>')
    return """<div class="quote-card" id="{hid}">
  <h2>{heading}</h2>
  <p class="card-sub">{sub}</p>
  <form name="quote" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="company">
    <input type="hidden" name="form-name" value="quote">
    <p class="hp"><label>Leave this empty <input name="company" tabindex="-1" autocomplete="off"></label></p>
    <div class="form-grid">
      <div class="field"><label for="{hid}-name">Name</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="{hid}-phone">Phone</label><input id="{hid}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required></div>
      <div class="field full"><label for="{hid}-email">Email <span class="opt">(optional)</span></label><input id="{hid}-email" name="email" type="email" autocomplete="email"></div>
      <div class="field full"><label for="{hid}-address">Street address or city</label><input id="{hid}-address" name="address" autocomplete="street-address" required></div>
      <div class="field full"><label for="{hid}-service">What do you need?</label><select id="{hid}-service" name="service" required>{opts}</select></div>
      <div class="field full"><label for="{hid}-msg">Details <span class="opt">(optional)</span></label><textarea id="{hid}-msg" name="message" rows="3"></textarea></div>
    </div>
    <button class="btn btn-sun" type="submit">Request my free quote</button>
    <p class="form-note">Prefer to talk? Call or text <a href="{tel}">{phone}</a>.</p>
  </form>
</div>""".format(hid=hid, heading=esc(heading), sub=esc(sub), opts="".join(opts), tel=TEL,
                 phone=BUSINESS["phone_display"])


def svc_cards(slugs):
    items = []
    for slug in slugs:
        s = SVC[slug]
        items.append("""<li><article class="svc-card">
  <div class="ico">{ico}</div>
  <h3><a href="/services/{slug}/">{name}</a></h3>
  <p>{card}</p>
</article></li>""".format(ico=icon(s["icon"]), slug=slug, name=esc(s["name"]), card=esc(s["card"])))
    return '<ul class="svc-grid">%s</ul>' % "".join(items)


def pain_block():
    rows = [
        ("Skipped weeks and no-shows", "Same day every week, backed by our show-up guarantee."),
        ("A pool that turns green between visits", "Water tested and balanced every visit so algae never gets a head start."),
        ("Calls and texts that go nowhere", "Call or text the owner directly, not a call center."),
    ]
    items = "".join(
        '<li><span class="pain-was">%s%s</span><span class="pain-now">%s%s</span></li>'
        % (icon("x"), esc(a), icon("check"), esc(b)) for a, b in rows)
    return """<section class="section section-foam" aria-labelledby="pain-title">
  <div class="wrap pain">
    <div>
      <h2 id="pain-title">Tired of unreliable pool guys?</h2>
      <p class="lead">You pay every month and still end up with skipped weeks, a green pool on Saturday morning and messages nobody answers. You shouldn't have to babysit your pool company.</p>
      <ul class="pain-list">{items}</ul>
    </div>
    <aside class="guarantee" aria-labelledby="guarantee-title">
      <div class="guarantee-seal" aria-hidden="true">{shield}<span>Show-up<br>guarantee</span></div>
      <h3 id="guarantee-title">We'll never miss a service, or your whole month is free.</h3>
      <p>Your weekly day is your weekly day. If we miss a scheduled service, you don't pay for that month. Simple as that.</p>
      <a class="btn btn-sun" href="/services/weekly-pool-spa-service/">Start weekly service</a>
    </aside>
  </div>
</section>""".format(items=items, shield=icon("shield"))


def gallery_block():
    if not GALLERY:
        return ""
    figs = "".join(
        '<li{wide}><figure><a href="{src}"><img src="{src}" alt="{alt}" loading="lazy" width="{w}" height="{h}"></a>'
        '<figcaption>{cap}</figcaption></figure></li>'.format(src=esc(g["src"]), alt=esc(g["alt"]), cap=esc(g.get("caption", "")),
                                                              w=g.get("w", 800), h=g.get("h", 600),
                                                              wide=' class="wide"' if g.get("w", 800) > g.get("h", 600) else "")
        for g in GALLERY)
    return """<section class="section" aria-labelledby="gallery-title">
  <div class="wrap">
    <div class="section-head"><h2 id="gallery-title">Recent work</h2><p>Real pools we take care of.</p></div>
    <ul class="gallery">{figs}</ul>
  </div>
</section>""".format(figs=figs)


def photo_grid(items):
    return '<ul class="gallery">%s</ul>' % "".join(
        '<li{wide}><figure><a href="{src}"><img src="{src}" alt="{alt}" loading="lazy" width="{w}" height="{h}"></a>'
        '<figcaption>{cap}</figcaption></figure></li>'.format(
            src=esc(g["src"]), alt=esc(g["alt"]), cap=esc(g.get("caption", "")), w=g["w"], h=g["h"],
            wide=' class="wide"' if g["w"] > g["h"] else "")
        for g in items)


def gtc_before_block():
    if not GTC_BEFORE:
        return ""
    return """<section class="section" aria-labelledby="before-title">
  <div class="wrap">
    <div class="section-head"><h2 id="before-title">Green pools we've taken on</h2>
    <p>Real "before" photos from our green-to-clean jobs. However bad yours looks, we've seen worse.</p></div>
    {grid}
  </div>
</section>""".format(grid=photo_grid(GTC_BEFORE).replace('class="gallery"', 'class="gallery gallery-3"', 1))


def reviews_block():
    if not TESTIMONIALS:
        return ""
    cards = []
    for r in TESTIMONIALS:
        stars = ""
        if r.get("stars"):
            stars = '<p class="stars" aria-label="%d out of 5 stars">%s</p>' % (r["stars"], icon("star") * int(r["stars"]))
        src = (" · via %s" % esc(r["source"])) if r.get("source") else ""
        cards.append('<li><figure class="review">%s<blockquote><p>%s</p></blockquote>'
                     '<figcaption><strong>%s</strong>, %s%s</figcaption></figure></li>'
                     % (stars, esc(r["quote"]), esc(r["name"]), esc(r.get("city", "")), src))
    return """<section class="section section-navy tile-navy" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="section-head"><h2 id="reviews-title">What our customers say</h2></div>
    <ul class="reviews">{cards}</ul>
  </div>
</section>""".format(cards="".join(cards))


def faq_block(faqs, title="Common questions"):
    items = "".join('<details><summary>%s</summary><div class="answer"><p>%s</p></div></details>'
                    % (esc(q), esc(a)) for q, a in faqs)
    return '<h2>%s</h2><div class="faq">%s</div>' % (esc(title), items)


# ---------------------------------------------------------------------------
# Green-to-clean before/after illustration (swap for real photos any time)
# ---------------------------------------------------------------------------
def pool_svg(state):
    green = state == "before"
    uid = state
    deck = "#C9C4B8" if green else "#DCD9D2"
    coping = "#B5AE9C" if green else "#F4F2EC"
    tile_a = "#3B5320" if green else "#16508F"
    tile_b = "#4F6A26" if green else "#2E7CC4"
    w1, w2, w3 = ("#7C9A2D", "#5A7A1F", "#3C5614") if green else ("#7FDDF9", "#2BB6EC", "#1386C9")
    s = ['<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">'
         % ("Before: a neglected pool with green, murky water and floating leaves" if green
            else "After: the same pool with clear, sparkling blue water")]
    s.append("""<defs>
<radialGradient id="w-{u}" cx="40%" cy="35%" r="80%"><stop offset="0" stop-color="{w1}"/><stop offset=".55" stop-color="{w2}"/><stop offset="1" stop-color="{w3}"/></radialGradient>
<pattern id="deck-{u}" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="{deck}"/><path d="M0 0h40M0 0v40" stroke="rgba(0,0,0,.07)" stroke-width="2"/></pattern>
<clipPath id="pool-{u}"><rect x="96" y="86" width="608" height="328" rx="34"/></clipPath>
<filter id="blur-{u}"><feGaussianBlur stdDeviation="14"/></filter>
</defs>""".format(u=uid, w1=w1, w2=w2, w3=w3, deck=deck))
    s.append('<rect width="800" height="500" fill="url(#deck-%s)"/>' % uid)
    s.append('<rect x="70" y="60" width="660" height="380" rx="56" fill="%s"/>' % coping)
    s.append('<rect x="88" y="78" width="624" height="344" rx="40" fill="%s"/>' % tile_a)
    s.append('<rect x="88" y="78" width="624" height="344" rx="40" fill="none" stroke="%s" stroke-width="16" stroke-dasharray="14 4"/>' % tile_b)
    s.append('<g clip-path="url(#pool-%s)">' % uid)
    s.append('<rect x="96" y="86" width="608" height="328" fill="url(#w-%s)"/>' % uid)
    # steps in the corner
    step_fill = "rgba(60,80,20,.55)" if green else "rgba(255,255,255,.35)"
    s.append('<path d="M96 300 A120 120 0 0 1 216 414 L96 414Z" fill="%s"/>' % step_fill)
    s.append('<path d="M96 340 A80 80 0 0 1 176 414" fill="none" stroke="%s" stroke-width="5"/>' % step_fill)
    s.append('<path d="M96 375 A42 42 0 0 1 138 414" fill="none" stroke="%s" stroke-width="5"/>' % step_fill)
    # main drain
    s.append('<rect x="384" y="236" width="32" height="32" rx="6" fill="%s"/>' % ("rgba(30,45,10,.5)" if green else "rgba(255,255,255,.55)"))
    if green:
        for cx, cy, r in [(200, 160, 70), (520, 330, 90), (630, 150, 60), (330, 360, 55), (450, 140, 50)]:
            s.append('<circle cx="%d" cy="%d" r="%d" fill="#2E4410" opacity=".55" filter="url(#blur-%s)"/>' % (cx, cy, r, uid))
        leaves = [(180, 210, 20), (260, 130, -35), (420, 300, 60), (560, 220, 15), (610, 340, -20),
                  (330, 250, 80), (480, 380, -60), (650, 260, 40), (240, 330, -10), (520, 120, 70)]
        for x, y, rot in leaves:
            s.append('<g transform="translate(%d %d) rotate(%d)"><ellipse rx="15" ry="6" fill="#6B4A1E"/>'
                     '<path d="M-14 0H14" stroke="#4A3212" stroke-width="1.5"/></g>' % (x, y, rot))
        s.append('<rect x="96" y="86" width="608" height="328" fill="#3C5614" opacity=".18"/>')
    else:
        caustic = ("M110 130c40-18 70 20 110 2s70-22 110 0 80 16 120-4 80-16 120 2 70 18 100 0",
                   "M110 200c40-18 70 20 110 2s70-22 110 0 80 16 120-4 80-16 120 2 70 18 100 0",
                   "M110 270c40-18 70 20 110 2s70-22 110 0 80 16 120-4 80-16 120 2 70 18 100 0",
                   "M110 340c40-18 70 20 110 2s70-22 110 0 80 16 120-4 80-16 120 2 70 18 100 0",
                   "M110 400c40-18 70 20 110 2s70-22 110 0 80 16 120-4 80-16 120 2 70 18 100 0")
        for d in caustic:
            s.append('<path d="%s" fill="none" stroke="#FFFFFF" stroke-opacity=".38" stroke-width="3" stroke-linecap="round"/>' % d)
        s.append('<ellipse cx="300" cy="170" rx="160" ry="60" fill="#FFFFFF" opacity=".16" filter="url(#blur-%s)"/>' % uid)
    s.append("</g>")
    # skimmer lid on the deck
    s.append('<rect x="560" y="22" width="44" height="28" rx="6" fill="%s"/>' % ("#A79F8B" if green else "#ECEAE4"))
    s.append("</svg>")
    return "".join(s)


# Real before/after photos for the slider (same pool, same angle). Set to None to use the illustration.
SLIDER_PHOTOS = {
    "before": "/assets/img/gallery/before.jpg",
    "after": "/assets/img/gallery/after.jpg",
    "w": 712, "h": 940,
    "before_alt": "Before: cloudy pool with debris on the floor",
    "after_alt": "After: the same pool with clear, clean blue water",
}


def slider(caption=True):
    ph = SLIDER_PHOTOS
    if ph:
        after = '<img src="%s" alt="%s" width="%d" height="%d" loading="lazy" draggable="false">' % (ph["after"], esc(ph["after_alt"]), ph["w"], ph["h"])
        before = '<img src="%s" alt="%s" width="%d" height="%d" loading="lazy" draggable="false">' % (ph["before"], esc(ph["before_alt"]), ph["w"], ph["h"])
        style = ' style="--ar: %d / %d"' % (ph["w"], ph["h"])
        note = "A real Your Local Pool Guys cleanup. Drag the handle, or use the arrow keys, to compare."
        cls = "ba ba-photo"
    else:
        after, before, style, cls = pool_svg("after"), pool_svg("before"), "", "ba"
        note = "Illustration. Drag the handle, or use the arrow keys, to compare."
    cap = '<p class="ba-caption">%s</p>' % note if caption else ""
    return """<figure class="ba-figure">
<div class="{cls}" data-ba{style}>
  <div class="ba-layer ba-after">{after}</div>
  <div class="ba-layer ba-before">{before}</div>
  <span class="ba-tag ba-tag-before">Before</span>
  <span class="ba-tag ba-tag-after">After</span>
  <div class="ba-handle"><span>{arrows}</span></div>
  <input type="range" min="0" max="100" value="50" step="1" aria-label="Before and after comparison of a pool cleanup">
</div>
{cap}
</figure>""".format(cls=cls, style=style, after=after, before=before, arrows=icon("arrows"), cap=cap)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/"):
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def page_home():
    title = "Pool & Spa Service San Fernando Valley | Your Local Pool Guys"
    desc = ("Weekly pool and spa service and pool repair in the San Fernando Valley and Los Angeles. "
            "Pumps, filters, green-to-clean, tile, acid wash and replastering. Call or text (818) 857-1463.")
    ld = [business_ld(),
          {"@type": "WebSite", "@id": BUSINESS["url"] + "/#website", "url": BUSINESS["url"] + "/",
           "name": BUSINESS["name"], "publisher": {"@id": BIZ_ID}},
          faq_ld(HOME_FAQS)]
    weekly = SVC["weekly-pool-spa-service"]
    cities = "".join("<li>%s</li>" % esc(c) for c in CITIES)
    body = """<main id="main">
<section class="hero tile">
  <div class="hero-sun" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div>
      <h1><span class="line-sm">San Fernando Valley</span>Pool &amp; spa service and repair</h1>
      <p class="hero-sub">Weekly cleaning, equipment repair and pool makeovers from your local pool guys. One call, and it's handled.</p>
      <a class="phone-bar" href="{tel}">{phone}</a>
      <span class="phone-note">Call or text. Free quotes.</span>
      <div class="btn-row">
        <a class="btn btn-navy" href="/services/weekly-pool-spa-service/">Weekly service</a>
        <a class="btn btn-ghost" href="/services/pool-spa-repair/">Repairs</a>
      </div>
    </div>
    {form}
  </div>
</section>

<div class="promise">
  <ul class="wrap">
    <li>{i_cal}Weekly pool &amp; spa routes</li>
    <li>{i_wr}Equipment repair &amp; replacement</li>
    <li>{i_shield}Show-up guarantee</li>
    <li>{i_pin}Serving the Valley &amp; LA</li>
  </ul>
</div>

{pain}
<section class="section" aria-labelledby="offers-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="offers-title">Two things we do really well</h2>
      <p>Keep your pool and spa clean every week, and fix it when something breaks.</p>
    </div>
    <div class="offers">
      <article class="offer offer-pool">
        <h3>Weekly pool &amp; spa service</h3>
        <p>Same day every week. You enjoy the pool; we keep it that way.</p>
        <ul>
          <li>{chk}Water tested and chemicals balanced</li>
          <li>{chk}Skimmed, brushed and vacuumed</li>
          <li>{chk}Baskets emptied, filter pressure watched</li>
          <li>{chk}Pump, heater and timer checked each visit</li>
        </ul>
        <a class="btn" href="/services/weekly-pool-spa-service/">About weekly service</a>
      </article>
      <article class="offer offer-repair">
        <h3>Pool &amp; spa repairs</h3>
        <p>Noisy pump, leaking pad, heater won't fire? We diagnose it and quote it straight.</p>
        <ul>
          <li>{chk}Pump and motor replacement</li>
          <li>{chk}Filter cleaning, rebuilds and replacement</li>
          <li>{chk}Heater troubleshooting and repair</li>
          <li>{chk}Leaks, valves and equipment pad plumbing</li>
        </ul>
        <a class="btn btn-navy" href="/services/pool-spa-repair/">About repairs</a>
      </article>
    </div>
  </div>
</section>

<section class="section section-navy tile-navy on-dark" aria-labelledby="gtc-title">
  <div class="wrap gtc">
    <div>
      <h2 id="gtc-title">From <span class="green">swamp</span> to swimmable</h2>
      <p>Pool sat too long? Pump died over the summer? Just bought a house with a pond in the backyard? Our green-to-clean service clears the algae, cleans out the filter and brings the water back, usually without draining.</p>
      <div class="btn-row">
        <a class="btn btn-sun" href="/services/green-to-clean/">See green to clean</a>
        <a class="btn btn-ghost" href="{sms}">Text us a photo</a>
      </div>
    </div>
    {slider}
  </div>
</section>

{gallery}
<section class="section section-foam" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="svc-title">Repairs, tile &amp; resurfacing</h2>
      <p>Everything beyond the weekly clean, from equipment swaps to a brand-new finish.</p>
    </div>
    {cards}
  </div>
</section>

<section class="section" aria-labelledby="how-title">
  <div class="wrap">
    <div class="section-head"><h2 id="how-title">Getting started takes one message</h2></div>
    <ol class="steps">
      <li><h3>Call, text or send the form</h3><p>Tell us your address and what's going on. A photo of the pool or equipment helps.</p></li>
      <li><h3>We take a look</h3><p>We check the pool, spa and equipment and give you a clear quote.</p></li>
      <li><h3>Your pool is handled</h3><p>Weekly service starts on your set day, or the repair gets scheduled.</p></li>
    </ol>
  </div>
</section>

{reviews}
<section class="section section-foam" aria-labelledby="area-title">
  <div class="wrap area">
    <div>
      <h2 id="area-title">Your local pool guys, from the Valley to the coast</h2>
      <p class="lead">We serve homes across the San Fernando Valley, the Westside and the Conejo Valley, including:</p>
      <ul class="city-list">{cities}</ul>
      <p>Don't see your city? <a href="{tel}">Call or text</a> and ask.</p>
    </div>
    <div class="map"><iframe title="Map of our service area: San Fernando Valley, Westside LA and Conejo Valley" src="https://maps.google.com/maps?q=Sherman%20Oaks%2C%20CA&amp;z=9&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>

<section class="section" aria-label="Frequently asked questions">
  <div class="wrap">{faq}</div>
</section>
</main>
""".format(tel=TEL, sms=SMS, phone=BUSINESS["phone_display"], form=quote_form(hid="quote-home"),
           i_cal=icon("calendar"), i_wr=icon("wrench"), i_user=icon("user"), i_pin=icon("pin"),
           chk=icon("check"), slider=slider(caption=False),
           cards=svc_cards([s["slug"] for s in SERVICES if s["group"] != "core"]),
           cities=cities, faq=faq_block(HOME_FAQS), i_shield=icon("shield"),
           pain=pain_block(), gallery=gallery_block(), reviews=reviews_block())
    write("/", head(title, desc, "/", ld) + header("/") + body + footer())


def page_service(s):
    path = "/services/%s/" % s["slug"]
    crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
    ld = [business_ld(),
          {"@type": "Service", "name": s["name"], "serviceType": s["name"], "url": BUSINESS["url"] + path,
           "description": s["desc"], "provider": {"@id": BIZ_ID},
           "areaServed": [{"@type": "City", "name": c + ", CA"} for c in CITIES]},
          crumbs_ld(crumbs), faq_ld(s["faqs"])]
    parts = []
    if s.get("slider"):
        parts.append('<div style="margin-bottom:2.2em">%s</div>' % slider())
    for item in s["body"]:
        if isinstance(item, tuple):
            parts.append("<h2>%s</h2>%s" % (esc(item[0]), item[1]))
        else:
            parts.append(item)
    parts.append(faq_block(s["faqs"]))
    others = [x for x in SERVICES if x["slug"] != s["slug"]]
    side_links = "".join('<li><a href="/services/%s/">%s</a></li>' % (x["slug"], esc(x["name"])) for x in others)
    crumb_html = "".join(
        ('<li><a href="%s">%s</a></li>' % (u, esc(n))) if i < len(crumbs) - 1 else
        '<li aria-current="page">%s</li>' % esc(n) for i, (n, u) in enumerate(crumbs))
    body = """<main id="main">
<section class="page-hero tile">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>{crumbs}</ol></nav>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="btn-row">
      <a class="btn btn-sun" href="#quote">Get a free quote</a>
      <a class="btn btn-navy" href="{tel}">{pi}{phone}</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap article-grid">
    <article class="prose">{content}</article>
    <aside class="sidebar" aria-label="Contact and more services">
      <div class="contact-card">
        <h2>Talk to us</h2>
        <p>Call or text for a free quote. Photos help.</p>
        <a class="btn btn-sun" href="{tel}">{pi}{phone}</a>
        <a class="btn btn-ghost" href="{sms}">{mi}Send a text</a>
      </div>
      <div class="side-links"><h2>More services</h2><ul>{side}</ul></div>
    </aside>
  </div>
</section>
{before_strip}
<section class="section section-foam" aria-labelledby="rel-title">
  <div class="wrap">
    <div class="section-head"><h2 id="rel-title">Related services</h2></div>
    {related}
  </div>
</section>
<section class="section">
  <div class="wrap" style="max-width:760px">{form}</div>
</section>
</main>
""".format(crumbs=crumb_html, h1=esc(s["h1"]), lead=esc(s["lead"]), tel=TEL, sms=SMS,
           phone=BUSINESS["phone_display"], pi=icon("phone"), mi=icon("message"),
           content="".join(parts), side=side_links, related=svc_cards(s["related"]),
           before_strip=gtc_before_block() if s["slug"] == "green-to-clean" else "",
           form=quote_form(heading="Get a free %s quote" % s["nav"].lower() if s["group"] != "core" else "Get a free quote",
                           preselect=s["slug"]))
    write(path, head(s["title"], s["desc"], path, ld) + header(path) + body + footer())


def page_services():
    path = "/services/"
    title = "Pool & Spa Services | Your Local Pool Guys"
    desc = ("All pool and spa services from Your Local Pool Guys: weekly service, repairs, pump and filter "
            "replacement, green-to-clean, tile cleaning and repair, acid wash and replastering.")
    crumbs = [("Home", "/"), ("Services", path)]
    groups = ""
    for key, label in GROUPS:
        slugs = [s["slug"] for s in SERVICES if s["group"] == key]
        groups += '<div style="margin-bottom:48px"><h2>%s</h2>%s</div>' % (esc(label), svc_cards(slugs))
    body = """<main id="main">
<section class="page-hero tile"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Services</li></ol></nav>
  <h1>Pool &amp; spa services</h1>
  <p class="lead">Weekly service to keep it clean, repairs to keep it running, and renovation work to make it look new again.</p>
</div></section>
<section class="section"><div class="wrap">{groups}</div></section>
</main>
""".format(groups=groups)
    write(path, head(title, desc, path, [business_ld(), crumbs_ld(crumbs)]) + header(path) + body + footer())


def page_area():
    path = "/service-area/"
    title = "Service Area: SFV, Westside & Conejo Valley | Your Local Pool Guys"
    desc = ("Your Local Pool Guys serves %s and surrounding Los Angeles neighborhoods with weekly pool service and repairs."
            % ", ".join(CITIES[:6]))
    crumbs = [("Home", "/"), ("Service Area", path)]
    cities = "".join("<li>%s</li>" % esc(c) for c in CITIES)
    links = "".join('<li><a href="/services/%s/">%s</a></li>' % (s["slug"], esc(s["name"])) for s in SERVICES)
    body = """<main id="main">
<section class="page-hero tile"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Service Area</li></ol></nav>
  <h1>Pool service across the Valley, Westside &amp; Conejo Valley</h1>
  <p class="lead">Local routes mean we're nearby when something breaks, and your weekly day stays consistent.</p>
</div></section>
<section class="section"><div class="wrap area">
  <div>
    <h2>Cities and neighborhoods we serve</h2>
    <ul class="city-list">{cities}</ul>
    <p>Close by but not listed? <a href="{tel}">Call or text {phone}</a> and we'll tell you if you're on a route.</p>
    <h2 style="margin-top:1.4em">Services available in every area</h2>
    <ul class="checks-plain">{links}</ul>
  </div>
  <div class="map"><iframe title="Map of our service area: San Fernando Valley, Westside LA and Conejo Valley" src="https://maps.google.com/maps?q=Sherman%20Oaks%2C%20CA&amp;z=9&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
</main>
""".format(cities=cities, tel=TEL, phone=BUSINESS["phone_display"], links=links)
    write(path, head(title, desc, path, [business_ld(), crumbs_ld(crumbs)]) + header(path) + body + footer())


def page_contact():
    path = "/contact/"
    title = "Contact & Free Quote | Your Local Pool Guys"
    desc = "Call or text (818) 857-1463 or send the form for a free pool and spa service or repair quote in the San Fernando Valley and LA."
    crumbs = [("Home", "/"), ("Contact", path)]
    body = """<main id="main">
<section class="page-hero tile"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Contact</li></ol></nav>
  <h1>Get a free quote</h1>
  <p class="lead">Call, text or send the form. You'll hear back from the person who does the work.</p>
</div></section>
<section class="section"><div class="wrap contact-grid">
  <div>
    <ul class="contact-list">
      <li><strong>Call or text</strong><a href="{tel}">{phone}</a></li>
      <li><strong>Email</strong><a href="mailto:{email}">{email}</a></li>
      <li><strong>Hours</strong><span>{hours}</span></li>
      <li><strong>Service area</strong><span>{region}</span></li>
    </ul>
    <div class="btn-row">
      <a class="btn btn-navy" href="{tel}">{pi}Call now</a>
      <a class="btn btn-ghost" href="{sms}">{mi}Send a text</a>
    </div>
  </div>
  {form}
</div></section>
</main>
""".format(tel=TEL, sms=SMS, phone=BUSINESS["phone_display"], email=BUSINESS["email"],
           hours=esc(BUSINESS["hours"]), region=esc(BUSINESS["region"]), pi=icon("phone"),
           mi=icon("message"), form=quote_form(hid="quote"))
    write(path, head(title, desc, path, [business_ld(), crumbs_ld(crumbs)]) + header(path) + body + footer())


def page_simple(path, title, h1, text, noindex=True, filename=None):
    body = """<main id="main" class="wrap center-page"><div>
<h1>{h1}</h1><p class="lead">{text}</p>
<div class="btn-row"><a class="btn btn-sun" href="/">Back to home</a><a class="btn btn-navy" href="{tel}">{pi}{phone}</a></div>
</div></main>
""".format(h1=esc(h1), text=esc(text), tel=TEL, pi=icon("phone"), phone=BUSINESS["phone_display"])
    content = head(title, text, path, None, noindex=noindex) + header(None) + body + footer()
    if filename:
        with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
            f.write(content)
    else:
        write(path, content)


def sitemap_and_robots():
    paths = ["/", "/services/", "/service-area/", "/contact/"] + ["/services/%s/" % s["slug"] for s in SERVICES]
    urls = "".join("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (BUSINESS["url"], p, TODAY) for p in paths)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: %s/sitemap.xml\n" % BUSINESS["url"])
    return paths


def main():
    page_home()
    page_services()
    for s in SERVICES:
        page_service(s)
    page_area()
    page_contact()
    page_simple("/thank-you/", "Thanks | Your Local Pool Guys", "Quote request received",
                "Thanks! We'll get back to you shortly. Need us sooner? Call or text %s." % BUSINESS["phone_display"])
    page_simple("/404.html", "Page not found | Your Local Pool Guys", "Page not found",
                "That page isn't here. Head home or give us a call.", filename="404.html")
    paths = sitemap_and_robots()
    print("Built %d indexable pages into %s" % (len(paths), OUT))


if __name__ == "__main__":
    main()
