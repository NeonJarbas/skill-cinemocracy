import json
from os.path import join, dirname

from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill


class CinemocracySkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        self.supported_media = [MediaType.DOCUMENTARY]
        # load video catalog
        path = join(dirname(__file__), "res", "cinemocracy.jsondb")
        logo = join(dirname(__file__), "res", "cinemocracy.png")
        self.default_image = join(dirname(__file__), "ui", "cinemocracy.png")
        self.skill_logo = join(dirname(__file__), "ui", "cinemocracy.png")
        self.skill_icon = join(dirname(__file__), "ui", "cinemocracy.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.jpeg")
        with open(path) as f:
            self.archive = json.load(f)["cinemocracy"]
        super().__init__(*args, **kwargs)
        self.load_ocp_keywords()

    def load_ocp_keywords(self):
        title = []

        for data in self.archive:
            t = data["title"].split("|")[0].split("(")[0].strip()
            title.append(t)
            if ":" in t:
                t1, t2 = t.split(":", 1)
                title.append(t1.strip())
                title.append(t2.strip())

        self.register_ocp_keyword(MediaType.DOCUMENTARY,
                                  "documentary_name", title)
        self.register_ocp_keyword(MediaType.DOCUMENTARY,
                                  "documentary_genre", ["war", "propaganda"])
        self.register_ocp_keyword(MediaType.DOCUMENTARY,
                                  "documentary_streaming_provider",
                                  ["Cinemocracy",
                                   "War Propaganda"])

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = 15 if media_type == MediaType.DOCUMENTARY else 0
        entities = self.ocp_voc_match(phrase)

        title = entities.get("documentary_name")
        skill = "documentary_streaming_provider" in entities  # skill matched

        base_score += 30 * len(entities)

        if title:
            base_score += 30
            candidates = [video for video in self.archive
                          if title.lower() in video["title"].lower()]
            for video in candidates:
                yield {
                    "title": video["title"],
                    "match_confidence": min(100, base_score),
                    "media_type": MediaType.DOCUMENTARY,
                    "uri": video["streams"][0],
                    "playback": PlaybackType.VIDEO,
                    "skill_icon": self.skill_icon,
                    "skill_id": self.skill_id
                }

        if skill:
            yield self.get_playlist()

    def get_playlist(self, score=50, num_entries=25):
        pl = self.featured_media()[:num_entries]
        return {
            "match_confidence": score,
            "media_type": MediaType.DOCUMENTARY,
            "playlist": pl,
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "title": "Cinemocracy (Documentary Playlist)",
            "author": "US Government"
        }

    @ocp_featured_media()
    def featured_media(self):
        return [{
            "title": video["title"],
            "match_confidence": 70,
            "media_type": MediaType.DOCUMENTARY,
            "uri": video["streams"][0],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "skill_id": self.skill_id
        } for video in self.archive]


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus

    s = CinemocracySkill(bus=FakeBus(), skill_id="t.fake")
    # "play war propaganda"
    for r in s.search_db("play Why We Fight", MediaType.DOCUMENTARY):
        print(r)
        # {'title': 'Why We Fight: The Battle of Britain', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/BattleOfBritain/BattleOfBritain.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: The Battle of China', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/BattleOfChina/BattleOfChina.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: The Battle of Russia Part I', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/BattleOfRussiaI/BattleOfRussiaI.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: The Battle of Russia Part II', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/BattleOfRussiaII/BattleOfRussiaII.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: Divide and Conquer', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/DivideAndConquer/DivideAndConquer.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: Prelude to War', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/PreludeToWar/PreludeToWar.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: The Nazi Strike', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/TheNazisStrike/TheNazisStrike.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
        # {'title': 'Why We Fight: War Comes to America', 'match_confidence': 75, 'media_type': <MediaType.DOCUMENTARY: 15>, 'uri': 'https://archive.org/download/WarComesToAmerica/WarComesToAmerica.mpeg', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake'}
