import json
import os.path
import shutil
import sys
from typing import IO, Dict, Any, List

output_dir = "generated"


def main():
    os.makedirs(output_dir, exist_ok=True)

    with open("metadata.json") as metadata_file:
        emoji_metadata: Dict[str, Dict[str, Any]] = json.load(metadata_file)

        with open(os.path.join(output_dir, "emoticonDefs.xml"), "w") as definition_file:
            definition_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            definition_file.write('<emoticons>\n')

            for (clean_emoji, emoji_data) in emoji_metadata.items():
                process_emoji(definition_file, emoji_data['emoji'], emoji_data['slugs'], emoji_data['name'])

            definition_file.write('</emoticons>\n')

        shutil.copy("twemoji/LICENSE-GRAPHICS", os.path.join(output_dir, "LICENSE-GRAPHICS"))
        shutil.copy("unicode-emoji-json/LICENSE", os.path.join(output_dir, "LICENSE-METADATA-UNICODE-EMOJI-JSON"))
        shutil.copy("gemoji/LICENSE", os.path.join(output_dir, "LICENSE-METADATA-GEMOJI"))


def process_emoji(definition_file: IO, emoji: str, slugs: List[str], name: str):
    main_slug = slugs[0]

    twemoji_path = get_twemoji_path(get_twemoji_id(emoji))
    if not os.path.exists(twemoji_path):
        # Try to remove the variation selector
        # that indicates that a unicode point should be displayed instead of a normal font character.
        # Twemoji sometimes uses it, but sometimes doesn't.
        emoji_stripped = emoji.replace(chr(0xfe0f), '')
        twemoji_path = get_twemoji_path(get_twemoji_id(emoji_stripped))
        if not os.path.exists(twemoji_path):
            # In even rarer cases twemoji contains the variation selector when the base emoji doesn't
            twemoji_path = get_twemoji_path(get_twemoji_id(emoji_stripped + chr(0xfe0f)))
            if not os.path.exists(twemoji_path):
                print(f"Failed to resolve emoji image for {emoji} ({name}): {twemoji_path}", file=sys.stderr)
                return

    shutil.copy(twemoji_path, os.path.join(output_dir, main_slug + ".png"))

    # Emoji titles may contain ampersands
    name = name.replace('&', '&amp;')
    clean_emoji = emoji.rstrip(chr(0xfe0f))
    definition_file.write(f"<emoticon defaultKey=\":{main_slug}:\" image=\"{main_slug}.png\" text=\"{name}\" "
                          f"order=\"20000\" hidden=\"true\"><alt>{clean_emoji}</alt>")
    # The order has to be set but doesn't matter since the emojis are already hidden
    for slug in slugs:
        definition_file.write(f"<alt>:{slug}:</alt><alt>~{slug}~</alt>")
    definition_file.write("</emoticon>\n")


def get_twemoji_id(emoji_str: str) -> str:
    return "-".join(map(lambda byte: f"{ord(byte):x}", emoji_str))


def get_twemoji_path(twemoji_id: str) -> str:
    return f"twemoji/assets/72x72/{twemoji_id}.png"


if __name__ == '__main__': main()
