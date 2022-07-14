# Twemoji for Jabber

Use your favorite emoji set in Cisco Jabber for Windows!

This repository contains a generator to create a Jabber emoji set from [twemoji](https://github.com/twitter/twemoji) and [unicode-emoji-json](https://github.com/muan/unicode-emoji-json).

## Installation

Builds can be found in the releases tab, [click here](https://github.com/Siphalor/twemoji-for-jabber/releases/latest) to go to the latest release.

You can install the emoji set locally on Windows by extracting the release to `%USERPROFILE%\AppData\Roaming\Cisco\Unified Communications\Jabber\CSF\CustomEmoticons` and then restarting Jabber.

See [the official Jabber article](https://help.webex.com/en-us/article/WBX72042/How-Do-I-Add-Custom-Emoticons-with-Cisco-Jabber-for-Windows?) for a detailed explanation of custom emojis in Jabber.

## Usage

You may use any of the supported emojis by using writing its slug wrapped in colons (`:slug:`) or tildes (`~slug~`).

For a complete list of all supported emojis and their slugs, see [the cheatsheet](./CHEATSHEET.md).

Alternatively, you may directly enter an emoji with <kbd><kbd>Win</kbd>+<kbd>.</kbd></kbd>. See [limitations](#limitations) for more info about the issues with that.

## Limitations

Jabber's emoji implementation has a few limitations:

- When entering an emoji directly, this emoji will render in its large form, even if used inline.  
  There seems to be no way around this.
- The default emoji sequences take precedence and will stop some sequences from working.  
  For example, every slug beginning with `:s` will be destroyed by Jabber's default emoji.  
  To work around this you can use the tilde syntax for these sequences.

The current implementation of this project doesn't support emojis with more than one skin tone.
It would be entirely possible to support these, I just gave up on these, because I didn't deem it being worth my time.

## License

The code in this repository is licensed as [MIT](./LICENSE).

The `metadata.json` file is based on `gemoji` and `unicode-emoji-json` and is therefore licensed under the combined MIT licenses of both projects.
