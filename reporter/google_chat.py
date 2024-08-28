import os, json, requests
from token import PERCENT

PASSED_COLOR = "#00ff00"
WARNING_COLOR = "#ffa500"
FAILED_COLOR = "#ff0000"
PERCENTAGE_ICON_LINK = {
    "#00ff00": "https://www.iconsdb.com/icons/preview/green/percentage-2-xxl.png",
    "#ffa500": "https://www.iconsdb.com/icons/preview/orange/percentage-2-xxl.png",
    "#ff0000": "https://www.iconsdb.com/icons/preview/red/percentage-2-xxl.png"
}

MESSAGE_HEADERS = {'Content-Type': 'application/json; charset=UTF-8'}

def main(webhook: str, stats_path: str, title: str, link: str, on_fails: str) -> None:
    if on_fails.lower() == 'true' and os.getenv('HAS_FAILS', 'false') == 'false':
        return

    with open(stats_path, 'r') as f:
        statistics = json.load(f)

    with open(os.path.join(os.path.dirname(__file__), 'report_card.json'), 'r') as f:
        report_card = json.load(f)

    if statistics["pass_percentage"] > 90:
        color = PASSED_COLOR
    elif 75 <= statistics["pass_percentage"] <= 90:
        color = WARNING_COLOR
    else:
        color = FAILED_COLOR

    # Update the report card title
    report_card["cardsV2"][0]["card"]["sections"][0]["header"] = title

    # Update the report card
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][0]["decoratedText"]["text"] = f'<font color="#80e27e">{statistics["passed"]}</font>'
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][1]["decoratedText"]["text"] = f'<font color="#ff0000">{statistics["failed"]}</font>'
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][2]["decoratedText"]["text"] = f'<font color="#9e9e9e">{statistics["skipped"]}</font>'
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][3]["decoratedText"]["text"] = str(statistics["total"])
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][0]["widgets"][4]["decoratedText"]["text"] = f'<font color="{color}">Passed %</font>'
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][0]["widgets"][4]["decoratedText"]["icon"]["iconUrl"] = PERCENTAGE_ICON_LINK.get(color)
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][4]["decoratedText"]["text"] = f'<font color="{color}">{statistics["pass_percentage"]}</font>'
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"][5]["decoratedText"]["text"] = statistics["duration"]

    if not statistics["skipped"]:
        report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][0]["widgets"].pop(2)
        report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][0]["columns"]["columnItems"][1]["widgets"].pop(2)

    # Add report link to footer
    report_card["cardsV2"][0]["card"]["sections"][0]["widgets"][1]["buttonList"]["buttons"][0]["onClick"]["openLink"]["url"] = link

    # Send the report card to Google Chat
    response = requests.post(webhook, headers=MESSAGE_HEADERS, json=report_card)

    if response.status_code != 200:
        raise Exception(f"Failed to send the report card to Google Chat: {response.text}")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('webhook', help='The Google Chat webhook', type=str)
    parser.add_argument('-s', '--stats', help='The statistics JSON file',
                        required=True, type=str)
    parser.add_argument('-l', '--link', help='The report link',
                        required=True, type=str)
    parser.add_argument('-t', '--title', help='The report title',
                        required=False, default="Robot Framework Report", type=str)
    parser.add_argument('-of', '--on_fails', help='Send the report only if there are failed tests',
                        required=False, default='false', type=str)
    args = parser.parse_args()

    main(args.webhook, args.stats, args.title, args.link, args.on_fails)
