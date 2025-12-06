from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from db_utils import get_cursor


class ActionQueryIPCSection(Action):
    def name(self) -> Text:
        return "action_query_ipc_section"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            # Get the IPC section from the tracker
            ipc_section = next(tracker.get_latest_entity_values("ipc_section"), None)

            if not ipc_section:
                dispatcher.utter_message(
                    text=(
                        "I couldn't find the IPC section you're asking about. "
                        "Could you please specify the section number?"
                    )
                )
                return []

            # Clean the section number
            section_number = (
                ipc_section.replace("IPC section", "")
                .replace("IPC", "")
                .replace("section", "")
                .strip()
            )

            with get_cursor(dictionary=True) as (cursor, connection):
                # Query the database
                query = "SELECT * FROM ipc_sections WHERE section_number = %s"
                cursor.execute(query, (section_number,))
                result = cursor.fetchone()

                if result:
                    response = f"IPC Section {result['section_number']}:\n"
                    response += f"Title: {result['title']}\n"
                    response += f"Description: {result['description']}\n"
                    response += f"Punishment: {result['punishment']}"
                else:
                    response = (
                        f"I couldn't find information about IPC Section {section_number}."
                    )

                dispatcher.utter_message(text=response)

        except Exception as e:  # pragma: no cover - defensive
            dispatcher.utter_message(
                text=(
                    "Sorry, I encountered an error while accessing the database: "
                    f"{str(e)}"
                )
            )

        return []


class ActionQueryCrime(Action):
    def name(self) -> Text:
        return "action_query_crime"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            # Get the crime from the tracker
            crime = next(tracker.get_latest_entity_values("crime"), None)

            if not crime:
                dispatcher.utter_message(
                    text=(
                        "I couldn't identify the crime you're asking about. "
                        "Could you please specify the crime?"
                    )
                )
                return []

            with get_cursor(dictionary=True) as (cursor, connection):
                # Query the database for the crime and related IPC sections
                query = """
                    SELECT c.*, i.section_number, i.title, i.punishment
                    FROM crimes c
                    JOIN crime_ipc_mapping m ON c.id = m.crime_id
                    JOIN ipc_sections i ON m.ipc_section_id = i.id
                    WHERE c.name LIKE %s
                """
                cursor.execute(query, (f"%{crime}%",))
                results = cursor.fetchall()

                if results:
                    response = f"Information about {crime}:\n\n"
                    response += f"Description: {results[0]['description']}\n"
                    response += f"Severity: {results[0]['severity']}\n\n"
                    response += "Related IPC Sections:\n"

                    for result in results:
                        response += f"\nSection {result['section_number']}:\n"
                        response += f"Title: {result['title']}\n"
                        response += f"Punishment: {result['punishment']}\n"
                else:
                    response = f"I couldn't find information about {crime}."

                dispatcher.utter_message(text=response)

        except Exception as e:  # pragma: no cover - defensive
            dispatcher.utter_message(
                text=(
                    "Sorry, I encountered an error while accessing the database: "
                    f"{str(e)}"
                )
            )

        return []


class ActionSuggestIPCFromDescription(Action):
    """Suggest likely crimes and IPC sections from a free-text incident description."""

    def name(self) -> Text:
        return "action_suggest_ipc_from_description"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text = (tracker.latest_message.get("text") or "").strip()

        if not text:
            dispatcher.utter_message(
                text=(
                    "Please describe the incident in your own words so I can "
                    "suggest relevant crimes and IPC sections."
                )
            )
            return []

        lowered = text.lower()

        try:
            with get_cursor(dictionary=True) as (cursor, connection):
                # Load all crimes once
                cursor.execute(
                    "SELECT id, name, description, severity FROM crimes ORDER BY name"
                )
                crimes = cursor.fetchall()

                matched_crimes = []

                # 1) Direct name match in the text
                for crime in crimes:
                    crime_name = (crime["name"] or "").lower()
                    if crime_name and crime_name in lowered:
                        matched_crimes.append(crime)

                # 2) If no direct match, try keyword-based matching for common crime types
                if not matched_crimes:
                    crime_keywords = {
                        "theft": [
                            "steal",
                            "stole",
                            "stolen",
                            "stealing",
                            "jewellery",
                            "cash",
                            "wallet",
                            "phone",
                            "mobile phone",
                        ],
                        "robbery": [
                            "rob",
                            "robbed",
                            "robbing",
                            "weapon",
                            "threatened me",
                            "took my mobile",
                            "snatched my phone",
                        ],
                        "domestic violence": [
                            "beating his wife",
                            "beats his wife",
                            "beating her",
                            "regularly beating",
                            "domestic violence",
                        ],
                        "kidnapping": [
                            "kidnap",
                            "kidnapped",
                            "abducted",
                            "took the child",
                            "child from outside the school",
                        ],
                        "cyber fraud": [
                            "fake online profiles",
                            "online profile",
                            "cheat people online",
                            "took money from them online",
                            "online scam",
                        ],
                    }

                    for crime in crimes:
                        name = (crime["name"] or "").lower()
                        keywords = crime_keywords.get(name, [])
                        if any(kw in lowered for kw in keywords):
                            matched_crimes.append(crime)

                if not matched_crimes:
                    dispatcher.utter_message(
                        text=(
                            "Based on your description I couldn't confidently match a "
                            "specific crime from my database. You may ask directly "
                            "about a crime (for example: \"What is robbery?\") or an "
                            "IPC section (for example: \"What is section 379?\")."
                        )
                    )
                    return []

                # For each matched crime, fetch related IPC sections
                response_parts: List[str] = []
                for crime in matched_crimes:
                    crime_id = crime["id"]
                    cursor.execute(
                        """
                        SELECT i.section_number, i.title, i.punishment
                        FROM crime_ipc_mapping m
                        JOIN ipc_sections i ON m.ipc_section_id = i.id
                        WHERE m.crime_id = %s
                        ORDER BY i.section_number
                        """,
                        (crime_id,),
                    )
                    sections = cursor.fetchall()

                    part_lines = [
                        f"Information about {crime['name']}:",
                        "",
                        f"Description: {crime['description']}",
                        f"Severity: {crime['severity']}",
                        "",
                    ]

                    if sections:
                        part_lines.append("Related IPC Sections:")
                        for sec in sections:
                            part_lines.append("")
                            part_lines.append(f"Section {sec['section_number']}:")
                            part_lines.append(f"Title: {sec['title']}")
                            part_lines.append(f"Punishment: {sec['punishment']}")
                    else:
                        part_lines.append(
                            "Related IPC Sections:\nNo specific IPC sections found in the database."
                        )

                    response_parts.append("\n".join(part_lines))

                final_response = "\n\n".join(response_parts)
                dispatcher.utter_message(text=final_response)

        except Exception as e:  # pragma: no cover - defensive
            dispatcher.utter_message(
                text=(
                    "Sorry, I encountered an error while analysing your description: "
                    f"{str(e)}"
                )
            )

        return []