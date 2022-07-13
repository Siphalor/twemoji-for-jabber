import json
import os.path
import shutil
import sys
from typing import IO, Dict

output_dir = "generated"


def main():
    os.makedirs(output_dir, exist_ok=True)

    skin_tones: Dict[str, str] = {}
    with open("unicode-emoji-json/data-emoji-components.json") as emoji_components_file:
        for (name, unicode) in json.load(emoji_components_file).items():
            if name.endswith("_skin_tone"):
                skin_tones[name[:-10]] = unicode

    with open(os.path.join(output_dir, "emoticonDefs.xml"), "w") as definition_file:
        definition_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        definition_file.write('<emoticons>\n')
        with open("unicode-emoji-json/data-by-emoji.json", "r") as emoji_json_file:
            emojis: dict = json.load(emoji_json_file)
            for (emoji, data) in emojis.items():

                emoji_slug = data["slug"]
                process_emoji(definition_file, emoji, emoji_slug, data["name"].capitalize())

                if data["skin_tone_support"]:
                    joiner_index = emoji.find(chr(0x200d))
                    handle_skin_tones(definition_file, emoji, emoji_slug, data['name'], skin_tones, joiner_index)

        definition_file.write('</emoticons>\n')

    shutil.copy("twemoji/LICENSE-GRAPHICS", os.path.join(output_dir, "LICENSE-GRAPHICS"))
    shutil.copy("unicode-emoji-json/LICENSE", os.path.join(output_dir, "LICENSE-EMOJIDATA"))


def handle_skin_tones(definition_file: IO, emoji_str: str, emoji_slug: str, emoji_title: str, skin_tones: Dict[str, str], skin_tone_position: int):
    for (skin_name, skin_code) in skin_tones.items():
        skin_emoji_slug = f"{skin_name}_{emoji_slug}"
        skin_emoji_title = f"{skin_name.replace('_', ' ')} {emoji_title}".capitalize()

        if skin_tone_position == -1:
            skin_emoji_str = emoji_str + skin_code
        else:
            skin_emoji_str = emoji_str[:skin_tone_position] + skin_code + emoji_str[skin_tone_position:]

        process_emoji(definition_file, skin_emoji_str, skin_emoji_slug, skin_emoji_title)


def process_emoji(definition_file: IO, emoji_str: str, emoji_slug: str, emoji_title: str):
    twemoji_path = get_twemoji_path(get_twemoji_id(emoji_str))
    if not os.path.exists(twemoji_path):
        # Try to remove the variation selector
        # that indicates that a unicode point should be displayed instead of a normal font character.
        # Twemoji sometimes uses it, but sometimes doesn't.
        emoji_str_stripped = emoji_str.replace(chr(0xfe0f), '')
        twemoji_path = get_twemoji_path(get_twemoji_id(emoji_str_stripped))
        if not os.path.exists(twemoji_path):
            # In even rarer cases twemoji contains the variation selector when the base emoji doesn't
            twemoji_path = get_twemoji_path(get_twemoji_id(emoji_str_stripped + chr(0xfe0f)))
            if not os.path.exists(twemoji_path):
                print(f"Failed to resolve emoji image for {emoji_str} ({emoji_title}): {twemoji_path}", file=sys.stderr)
                return

    shutil.copy(twemoji_path, os.path.join(output_dir, emoji_slug + ".png"))

    # Emoji titles may contain ampersands
    emoji_title = emoji_title.replace('&', '&amp;')
    definition_file.write(f"<emoticon defaultKey=\":{emoji_slug}:\" image=\"{emoji_slug}.png\" text=\"{emoji_title}\" "
                          f"order="20000" hidden=\"true\"><alt>{emoji_str}</alt></emoticon>\n")
    # The order has to be set but doesn't matter since the emojis are already hidden


def get_twemoji_id(emoji_str: str) -> str:
    return "-".join(map(lambda byte: f"{ord(byte):x}", emoji_str))


def get_twemoji_path(twemoji_id: str) -> str:
    return f"twemoji/assets/72x72/{twemoji_id}.png"


if __name__ == '__main__': main()
