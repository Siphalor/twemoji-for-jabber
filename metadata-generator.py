import json
from typing import Dict, List, Optional, Any, Set

emoji_metadata: Dict[str, Dict[str, Any]] = {}
emoji_slugs: Set[str] = set()


def main():
    skin_tones: Dict[str, str] = {}
    with open("unicode-emoji-json/data-emoji-components.json") as emoji_components_file:
        for (name, unicode) in json.load(emoji_components_file).items():
            if name.endswith("_skin_tone"):
                skin_tones[name[:-10]] = unicode

    with open("unicode-emoji-json/data-by-emoji.json", "r") as emoji_json_file:
        emoji_data: dict = json.load(emoji_json_file)
        for (emoji, data) in emoji_data.items():
            process_emoji(emoji, [data['slug']], data['name'].capitalize())

            if data['skin_tone_support']:
                process_emoji_skins(emoji, [data['slug']], data['name'], skin_tones)

    with open("gemoji/db/emoji.json", "r") as emoji_json_file:
        emoji_data: List[Dict[str, Any]] = json.load(emoji_json_file)

        for data in emoji_data:
            process_emoji(data['emoji'], data['aliases'], data['description'])

            if data.get('skin_tones'):
                process_emoji_skins(data['emoji'], data['aliases'], data['description'], skin_tones)

    # Regional indicators
    for letter in map(chr, range(ord('A'), ord('Z') + 1)):
        process_emoji(chr(0x1F1E6 + ord(letter) - ord('A')), [letter, f"regional_indicator_{letter.lower()}"], f"Regional Indicator {letter}")

    with open("metadata.json", "w") as metadata_file:
        json.dump(emoji_metadata, metadata_file)

    with open("CHEATSHEET.md", "w") as cheatsheet_file:
        cheatsheet_file.write("Use an emoji by putting the slug in colons (`:slug:`) or tildes (`~slug~`).\n\n")
        cheatsheet_file.write("| Emoji | Slugs | Name |\n"
                              "| ----- | ----- | ---- |\n")
        for (_, emoji) in emoji_metadata.items():
            cheatsheet_file.write(f"| {emoji['emoji']} | {', '.join(map(lambda slug: f'`{slug}`', emoji['slugs']))} | {emoji['name']} |\n")


def process_emoji_skins(emoji: str, slugs: List[str], name: Optional[str], skin_tones: Dict[str, str]):
    joiner_index = emoji.find(chr(0x200d))

    for (skin_id, skin_code) in skin_tones.items():
        if joiner_index == -1:
            skin_emoji_str = emoji + skin_code
        else:
            skin_emoji_str = emoji[:joiner_index] + skin_code + emoji[joiner_index:]

        process_emoji(skin_emoji_str, list(map(lambda slug: f"{skin_id}_{slug}", slugs)),
                      None if name is None else f"{skin_id.replace('_', ' ')} {name}".capitalize())


def process_emoji(emoji: str, slugs: List[str], name: Optional[str]):
    clean_emoji = emoji.replace(chr(0xfe0f), '')
    if clean_emoji in emoji_metadata:
        metadata = emoji_metadata[clean_emoji]
        if metadata['name'] is None:
            metadata['name'] = name

        slugs_ref: List[str] = metadata['slugs']
        for slug in slugs:
            if slug not in emoji_slugs:
                slugs_ref.append(slug)
                emoji_slugs.add(slug)

    else:
        emoji_metadata[clean_emoji] = {
            'emoji': emoji,
            'name': name,
            'slugs': slugs
        }
        emoji_slugs.union(slugs)


if __name__ == '__main__':
    main()
