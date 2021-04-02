from ovos_workshop.skills.video_collection import VideoCollectionSkill
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_workshop.frameworks.cps import CPSMatchType, CPSPlayback, \
    CPSMatchConfidence


class CinemocracySkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("Cinemocracy")
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.VIDEO]
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        # load video catalog
        path = join(dirname(__file__), "res", "cinemocracy.jsondb")
        logo = join(dirname(__file__), "res", "cinemocracy.png")
        self.media_collection = Collection("cinemocracy", logo=logo, db_path=path)
        self.default_image = join(dirname(__file__), "ui", "cinemocracy.png")
        self.skill_logo = join(dirname(__file__), "ui", "cinemocracy.png")
        self.skill_icon = join(dirname(__file__), "ui", "cinemocracy.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.jpeg")
        self.media_type = CPSMatchType.VIDEO
        self.playback_type = CPSPlayback.GUI

    # voice interaction
    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # better common play
    def normalize_title(self, title):
        title = title.lower().strip()
        title = self.remove_voc(title, "cinemocracy")
        title = self.remove_voc(title, "movie")
        title = self.remove_voc(title, "play")
        title = self.remove_voc(title, "video")
        title = title.replace("|", "").replace('"', "") \
            .replace(':', "").replace('”', "").replace('“', "") \
            .strip()
        return " ".join([w for w in title.split(" ") if w])  # remove extra spaces

    def match_media_type(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "video") or media_type == CPSMatchType.VIDEO:
            score += 10

        if self.voc_match(phrase, "old"):
            score += 10

        if self.voc_match(phrase, "real"):
            score += 15

        if self.voc_match(phrase, "war"):
            score += 20

        if self.voc_match(phrase, "propaganda"):
            score += 20

        if self.voc_match(phrase, "cinemocracy"):
            score += 50

        return score


def create_skill():
    return CinemocracySkill()

