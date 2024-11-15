from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (
    BinaryCritic,
    EvalRubric,
    EvalSuite,
    SimilarityCritic,
    tool_eval,
)
from arcade_twilio.tools.send_sms import send_sms
from arcade_twilio.tools.send_whatsapp import send_whatsapp

catalog = ToolCatalog()
catalog.add_tool(send_sms, "Twilio")
catalog.add_tool(send_whatsapp, "Twilio")

rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
    fail_on_tool_selection=True,
    tool_selection_weight=1.0,
)


@tool_eval()
def twilio_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="Twilio Evaluation Suite",
        system_message="You are a helpful assistant.",
        catalog=catalog,
        rubric=rubric,
    )

    # Test SMS with specific phone number
    suite.add_case(
        name="Send SMS to specific number",
        user_message="Text 1234567890 saying Your appointment is confirmed for tomorrow at 2 PM",
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "1234567890",
                    "message": "Your appointment is confirmed for tomorrow at 2 PM",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Test SMS with my_phone_number
    suite.add_case(
        name="Send SMS to my number",
        user_message="Send me an SMS to remember to buy groceries",
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "my_phone_number",
                    "message": "Remember to buy groceries",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Test WhatsApp with specific number
    suite.add_case(
        name="Send WhatsApp to specific number",
        user_message="Send a WhatsApp message to +1987654321 with the text 'Meeting rescheduled to next week'",
        expected_tool_calls=[
            (
                send_whatsapp,
                {
                    "phone_number": "+1987654321",
                    "message": "Meeting rescheduled to next week",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Test WhatsApp with my_phone_number
    suite.add_case(
        name="Send WhatsApp to my number",
        additional_messages=[
            {
                "role": "user",
                "content": "Create a short list of the top 5 most popular movies",
            },
            {
                "role": "assistant",
                "content": """"
                    Here's a list of top-rated movies of all time, though opinions may vary:                

                    1 The Godfather (1972)                                                                 
                    2 The Shawshank Redemption (1994)                                                      
                    3 Schindler's List (1993)                                                              
                    4 Raging Bull (1980)                                                                   
                    5 Casablanca (1942)                                                                    

                    These titles are often mentioned in various "best of all time" lists.
                """,
            },
        ],
        user_message="Send me a WhatsApp message with the list",
        expected_tool_calls=[
            (
                send_whatsapp,
                {
                    "phone_number": "my_phone_number",
                    "message": """
                        Top 5 Movies of 
                        All Time:\n1. The Godfather (1972)\n2. The Shawshank Redemption (1994)\n3. Schindler's 
                        List (1993)\n4. Raging Bull (1980)\n5. Casablanca 
                        (1942)
                    """,
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Test platform selection with ambiguous request
    suite.add_case(
        name="Default to SMS when platform is not specified",
        user_message="Send a text to +1122334455 saying 'Hello!'",
        expected_tool_calls=[
            (
                send_sms,  # Default to SMS when platform is not specified
                {
                    "phone_number": "+1122334455",
                    "message": "Hello!",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Test multiple messages in sequence
    suite.add_case(
        name="Multiple messages sequence",
        user_message="Send an SMS to 1234567890 saying 'Part 1 of the document' and then send them a WhatsApp message with 'Part 2 of the document'",
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "1234567890",
                    "message": "Part 1 of the document",
                },
            ),
            (
                send_whatsapp,
                {
                    "phone_number": "1234567890",
                    "message": "Part 2 of the document",
                },
            ),
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    # Send previous content to WhatsApp
    suite.add_case(
        name="Send previous content to WhatsApp",
        user_message="Send me a WhatsApp message with the poem",
        additional_messages=[
            {
                "role": "user",
                "content": "Create a poem about the sunset",
            },
            {
                "role": "assistant",
                "content": "In the sky, hues softly blend, Daylight whispers to an end. Golden dreams and twilight's art, Sunset paints with love, depart.",
            },
        ],
        expected_tool_calls=[
            (
                send_whatsapp,
                {
                    "phone_number": "my_phone_number",
                    "message": "In the sky, hues softly blend, Daylight whispers to an end. Golden dreams and twilight's art, Sunset paints with love, depart.",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.7
            ),
        ],
    )

    # Send an SMS with the previous content
    suite.add_case(
        name="Send previous content via SMS",
        user_message="Send an SMS to my number with the poem",
        additional_messages=[
            {
                "role": "user",
                "content": "Write a really short poem about the sunset",
            },
            {
                "role": "assistant",
                "content": "In the sky, hues softly blend, Daylight whispers to an end. Golden dreams and twilight's art, Sunset paints with love, depart.",
            },
        ],
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "my_phone_number",
                    "message": "In the sky, hues softly blend, Daylight whispers to an end. Golden dreams and twilight's art, Sunset paints with love, depart.",
                },
            ),
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.7
            ),
        ],
    )

    # Test continuation with multiple messages
    suite.add_case(
        name="Basic continuation",
        additional_messages=[
            {
                "role": "assistant",
                "content": """
                    Here's the meeting notes:
                        Agenda:                                                                                 
                        1 Project Update:                                                                      
                            • John provided a status update on the X Project.                                   
                            • Key milestones have been achieved, and the project is on track.                   
                        2 Budget Review:                                                                       
                            • Jane discussed the current budget and necessary adjustments.                      
                            • Potential areas for cost-saving were highlighted.                                 
                        3 New Initiatives:                                                                     
                            • Emily introduced new outreach strategies for the upcoming quarter.                
                            • Approval needed for additional resources.
                """,
            },
            {"role": "user", "content": "Send the meeting notes to 1234567890"},
            {
                "role": "assistant",
                "content": "I've sent the meeting notes to 1234567890. Let me know if there's anything else you need help with!    ",
            },
            {
                "role": "user",
                "content": "What's the deadline for the project update?",
            },
            {
                "role": "assistant",
                "content": "The deadline for the project update is Oct 15.",
            },
        ],
        user_message="let them know about the deadline",
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "1234567890",
                    "message": "The deadline for the project update is Oct 15.",
                },
            ),
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.7
            ),
        ],
    )

    suite.add_case(
        name="Platform switch continuation",
        additional_messages=[
            {"role": "user", "content": "Text +1234567890: Team meeting at 3pm"},
            {
                "role": "assistant",
                "content": "I'll send an SMS saying 'Team meeting at 3pm'",
            },
            {"role": "user", "content": "and send that through WhatsApp too"},
        ],
        user_message="and send that through WhatsApp too",
        expected_tool_calls=[
            (
                send_sms,
                {
                    "phone_number": "+1234567890",
                    "message": "Team meeting at 3pm",
                },
            ),
            (
                send_whatsapp,
                {
                    "phone_number": "+1234567890",
                    "message": "Team meeting at 3pm",
                },
            ),
        ],
        critics=[
            BinaryCritic(critic_field="phone_number", weight=0.5),
            SimilarityCritic(
                critic_field="message", weight=0.5, similarity_threshold=0.9
            ),
        ],
    )

    return suite
