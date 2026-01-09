from fastapi import APIRouter
import re

from backend.services.market_price_service import get_market_prices
from backend.services.market_advisory_engine import analyze_markets

router = APIRouter(prefix="/api/chat", tags=["Chat Assistant"])

SESSIONS = {}

# -------- CONSTANTS --------
GREETINGS = ["hi", "hello", "hey", "hai"]
END_COMMANDS = ["stop", "end", "exit", "bye", "thanks", "thank you"]
RESET_COMMANDS = ["reset", "restart", "start over"]
NEXT_COMMANDS = ["next", "next crop", "analyze next", "for"]

SUPPORTED_CROPS = ["rice", "tomato", "onion", "paddy"]


def extract_number(text: str):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def reset_for_next_crop(session):
    session.pop("crop", None)
    session.pop("quantity_kg", None)
    session.pop("days_delay", None)
    session.pop("district", None)
    session.pop("mode", None)


@router.get("/")
def chat(session_id: str, message: str):
    session = SESSIONS.setdefault(session_id, {})
    text = message.lower().strip()

    # =========================================================
    # GLOBAL FREE-CHAT CONTROL (AFTER ANALYSIS)
    # =========================================================
    if session.get("mode") == "ANALYSIS_DONE":

        if any(cmd in text for cmd in END_COMMANDS):
            session.clear()
            return {
                "reply": "🙏 Thank you. Wish you a profitable sale. Come back anytime!"
            }

        if any(cmd in text for cmd in RESET_COMMANDS):
            session.clear()
            return {
                "reply": "🔄 Starting fresh.\nWhich crop did you harvest?"
            }

        if any(cmd in text for cmd in NEXT_COMMANDS):
            if session.get("pending_crops"):
                next_crop = session["pending_crops"].pop(0)
                reset_for_next_crop(session)
                session["crop"] = next_crop
                return {
                    "reply": (
                        f"Alright 👍 Let’s analyze {next_crop}.\n"
                        "How much quantity did you harvest (in kg)?"
                    )
                }
            else:
                reset_for_next_crop(session)
                return {
                    "reply": "Which crop would you like to analyze next?"
                }

        return {
            "reply": (
                "You can type:\n"
                "• next → analyze another crop\n"
                "• reset → start over\n"
                "• end → finish chat"
            )
        }

    # =========================================================
    # STEP 0: GREETING
    # =========================================================
    if text in GREETINGS and not session:
        return {
            "reply": (
                "Hello 👋 I will help you decide the best market to sell your crop.\n\n"
                "Which crop did you harvest?"
            )
        }

    # =========================================================
    # STEP 1: CROP (MULTI-CROP AWARE)
    # =========================================================
    if "crop" not in session:
        detected = [c for c in SUPPORTED_CROPS if c in text]

        if not detected:
            return {
                "reply": (
                    "Please tell me which crop you harvested.\n"
                    "Example: rice, tomato, onion"
                )
            }

        session["crop"] = detected[0]
        if len(detected) > 1:
            session["pending_crops"] = detected[1:]

        return {
            "reply": (
                f"Got it 👍 You harvested {session['crop']}.\n\n"
                "How much quantity did you harvest (in kg)?"
            )
        }

    # =========================================================
    # STEP 2: QUANTITY
    # =========================================================
    if "quantity_kg" not in session:
        qty = extract_number(text)
        if qty and qty > 0:
            session["quantity_kg"] = qty
            return {
                "reply": (
                    f"Noted 👍 Quantity is {qty} kg.\n\n"
                    "After how many days are you planning to sell?"
                )
            }
        return {
            "reply": "Please enter quantity in kg (example: 500 kg)."
        }

    # =========================================================
    # STEP 3: DAYS DELAY
    # =========================================================
    if "days_delay" not in session:
        days = extract_number(text)
        if days is not None and days >= 0:
            session["days_delay"] = days
            return {
                "reply": (
                    f"Okay 👍 Selling after {days} days.\n\n"
                    "Which district are you selling from?"
                )
            }
        return {
            "reply": "Please enter number of days (example: 3 days)."
        }

    # =========================================================
    # STEP 4: DISTRICT + FULL ADVISORY
    # =========================================================
    if "district" not in session:
        district = text.title()
        markets = get_market_prices(session["crop"], district)

        if not markets:
            return {
                "reply": (
                    f"I don't have market price data for {session['crop']} in {district}.\n"
                    "Please try a nearby district."
                )
            }

        session["district"] = district

        analysis = analyze_markets(
            crop=session["crop"],
            quantity_kg=session["quantity_kg"],
            days_delay=session["days_delay"],
            farmer_district=district,
            market_prices=markets
        )

        best = analysis[0]

        reply = (
            f"📍 Analysis for {session['crop']} from {district}\n\n"
            f"Nearby market comparison:\n"
        )

        for m in analysis:
            reply += (
                f"- {m['market']} ({m['distance_km']} km): "
                f"Net ₹{m['net_revenue']}\n"
            )

        reply += (
            f"\nStorage impact:\n"
            f"- Expected quantity loss: ~{best['loss_kg']} kg\n\n"
            f"Recommendation:\n"
            f"Selling at {best['market']} gives the highest net return "
            f"after transport and storage loss.\n\n"
            f"Risk note:\n"
            f"Prices may fluctuate due to arrivals and demand.\n\n"
            f"What would you like to do next?\n"
            f"• next → analyze another crop\n"
            f"• reset → start over\n"
            f"• end → finish chat"
        )

        session["mode"] = "ANALYSIS_DONE"
        return {"reply": reply}

    # =========================================================
    # FALLBACK
    # =========================================================
    return {
        "reply": "I am here to help. What would you like to do next?"
    }
