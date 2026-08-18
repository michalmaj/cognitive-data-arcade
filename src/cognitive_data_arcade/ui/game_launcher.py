from __future__ import annotations

from pathlib import Path

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager


def game_factory_for(lesson_num: int, pm: ProfileManager, strings: Strings):
    """Return a zero-arg factory that creates the game scene for lesson_num, or None."""
    if lesson_num == 1:

        def _make_inner() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
            from cognitive_data_arcade.games.big_data_map.info import get_game_info

            game_info = get_game_info(strings)

            def _detail_factory(ln: int) -> Scene:
                from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene

                back = _make_inner()
                detail = ConceptDetailScene(ln, strings, back_scene=back)
                return PausableGame(detail, game_info, lambda: _detail_factory(ln), strings, pm)

            inner = BigDataMapGame(strings, pm, concept_detail_factory=_detail_factory)
            return PausableGame(inner, game_info, _make_inner, strings, pm)

        def _make() -> Scene:
            from cognitive_data_arcade.games.big_data_map.info import get_game_info
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            game_info = get_game_info(strings)
            pausable = _make_inner()
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 2:

        def _make() -> Scene:
            import datetime

            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.reaction_time.config import DEFAULT_CONFIG
            from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame
            from cognitive_data_arcade.games.reaction_time.info import get_game_info
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            profile = pm.load()
            pid = profile.device_uuid
            sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = Path("data") / "generated" / "reaction_time" / f"{sid}.csv"
            inner = ReactionTimeGame(DEFAULT_CONFIG, pm, strings, pid, sid, csv_path)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 3:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene

            return EventLogLevelScene(pm, strings)

        return _make

    if lesson_num == 4:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.data_cleaning.info import get_game_info
            from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = DataCleaningScene(strings, pm)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 6:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.eda.info import get_game_info
            from cognitive_data_arcade.games.eda.scene import EDAScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = EDAScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 7:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

            return StroopLevelScene(pm, strings)

        return _make

    if lesson_num == 8:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

            return FlankerLevelScene(pm, strings)

        return _make

    if lesson_num == 9:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

            return GoNoGoLevelScene(pm, strings)

        return _make

    if lesson_num == 10:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

            return NBackLevelScene(pm, strings)

        return _make

    if lesson_num == 11:

        def _make() -> Scene:
            from cognitive_data_arcade.ui.visual_search_level_scene import VisualSearchLevelScene

            return VisualSearchLevelScene(pm, strings)

        return _make

    if lesson_num == 12:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.cognitive_dashboard.info import get_game_info
            from cognitive_data_arcade.games.cognitive_dashboard.mode_scene import (
                CognitiveDashboardModeScene,
            )
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = CognitiveDashboardModeScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 13:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.distribution_playground.info import get_game_info
            from cognitive_data_arcade.games.distribution_playground.scene import (
                DistributionPlaygroundScene,
            )
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = DistributionPlaygroundScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 14:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.correlation_trap.info import get_game_info
            from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = CorrelationTrapScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 15:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.hypothesis_arena.info import get_game_info
            from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = HypothesisArenaScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 16:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.prediction_slider.info import get_game_info
            from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = PredictionSliderScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 17:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.feature_hunter.game import FeatHunterScene
            from cognitive_data_arcade.games.feature_hunter.info import get_game_info
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = FeatHunterScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 18:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.classifier_battle.game import ClassifierBattleScene
            from cognitive_data_arcade.games.classifier_battle.info import get_game_info

            inner = ClassifierBattleScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 19:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.overfitting_monster.game import OverfittingMonsterScene
            from cognitive_data_arcade.games.overfitting_monster.info import get_game_info

            inner = OverfittingMonsterScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 20:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.anomaly_alert.game import AnomalyAlertScene
            from cognitive_data_arcade.games.anomaly_alert.info import get_game_info

            inner = AnomalyAlertScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 21:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.text_tokenizer.info import get_game_info
            from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = TextTokenizerLabScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 22:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.word_weight_factory.info import get_game_info
            from cognitive_data_arcade.games.word_weight_factory.scene import WordWeightFactoryScene
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = WordWeightFactoryScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 23:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.emotion_classifier.game import EmotionClassifierScene
            from cognitive_data_arcade.games.emotion_classifier.info import get_game_info

            inner = EmotionClassifierScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 24:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.semantic_space.game import SemanticSpaceScene
            from cognitive_data_arcade.games.semantic_space.info import get_game_info

            inner = SemanticSpaceScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 25:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.topic_detective.game import TopicDetectiveScene
            from cognitive_data_arcade.games.topic_detective.info import get_game_info

            inner = TopicDetectiveScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 26:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.human_vs_model.game import HumanVsModelScene
            from cognitive_data_arcade.games.human_vs_model.info import get_game_info

            inner = HumanVsModelScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 27:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.social_network.game import SocialNetworkScene
            from cognitive_data_arcade.games.social_network.info import get_game_info
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = SocialNetworkScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 28:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.misinformation.game import MisinformationScene
            from cognitive_data_arcade.games.misinformation.info import get_game_info

            inner = MisinformationScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 29:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.recommendation_bubble.game import (
                RecommendationBubbleScene,
            )
            from cognitive_data_arcade.games.recommendation_bubble.info import get_game_info

            inner = RecommendationBubbleScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 30:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.bias_blind_spot.game import BiasBlindSpotScene
            from cognitive_data_arcade.games.bias_blind_spot.info import get_game_info

            inner = BiasBlindSpotScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    if lesson_num == 31:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.you_were_the_dataset.game import YouWereTheDatasetScene
            from cognitive_data_arcade.games.you_were_the_dataset.info import get_game_info
            from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

            inner = YouWereTheDatasetScene(pm, strings)
            game_info = get_game_info(strings)
            pausable = PausableGame(inner, game_info, lambda: _make(), strings, pm)
            return make_how_to_play(pm, game_info, strings, back_scene=pausable)

        return _make

    if lesson_num == 32:

        def _make() -> Scene:
            from cognitive_data_arcade.engine.pause import PausableGame
            from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene
            from cognitive_data_arcade.games.architects_trial.info import get_game_info

            inner = ArchitectsTrialScene(pm, strings)
            game_info = get_game_info(strings)
            return PausableGame(inner, game_info, lambda: _make(), strings, pm)

        return _make

    return None


def game_factory_for_with_back(
    lesson_num: int,
    pm: ProfileManager,
    strings: Strings,
    back_scene: "Scene",
) -> "Scene | None":
    """Like game_factory_for but uses back_scene as the ESC/back destination.

    For simple level scenes (no HowToPlay wrapper), returns the scene directly.
    For pausable games with HowToPlay, injects back_scene as esc_scene.
    Falls back to game_factory_for() for complex special cases (RT Lab, BigDataMap).
    """
    from cognitive_data_arcade.engine.pause import PausableGame
    from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

    # Simple level scenes (no HowToPlay, ESC handled internally)
    if lesson_num == 3:
        from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene

        return EventLogLevelScene(pm, strings)

    if lesson_num == 7:
        from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

        return StroopLevelScene(pm, strings)

    if lesson_num == 8:
        from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

        return FlankerLevelScene(pm, strings)

    if lesson_num == 9:
        from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

        return GoNoGoLevelScene(pm, strings)

    if lesson_num == 10:
        from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

        return NBackLevelScene(pm, strings)

    if lesson_num == 11:
        from cognitive_data_arcade.ui.visual_search_level_scene import VisualSearchLevelScene

        return VisualSearchLevelScene(pm, strings)

    if lesson_num == 12:
        from cognitive_data_arcade.games.cognitive_dashboard.mode_scene import (
            CognitiveDashboardModeScene,
        )

        return CognitiveDashboardModeScene(pm, strings)

    # Standard pausable games: wrap with make_how_to_play injecting back_scene as esc_scene
    def _make_pausable_with_back(inner: "Scene", game_info: object) -> "Scene":
        def _restart() -> "Scene":
            return PausableGame(inner, game_info, _restart, strings, pm)  # type: ignore[arg-type]

        pausable = _restart()
        return make_how_to_play(pm, game_info, strings, back_scene=pausable, esc_scene=back_scene)  # type: ignore[arg-type]

    if lesson_num == 4:
        from cognitive_data_arcade.games.data_cleaning.info import get_game_info
        from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene

        return _make_pausable_with_back(DataCleaningScene(strings, pm), get_game_info(strings))

    if lesson_num == 6:
        from cognitive_data_arcade.games.eda.info import get_game_info
        from cognitive_data_arcade.games.eda.scene import EDAScene

        return _make_pausable_with_back(EDAScene(pm, strings), get_game_info(strings))

    if lesson_num == 13:
        from cognitive_data_arcade.games.distribution_playground.info import (
            get_game_info,
        )
        from cognitive_data_arcade.games.distribution_playground.scene import (
            DistributionPlaygroundScene,
        )

        return _make_pausable_with_back(
            DistributionPlaygroundScene(pm, strings), get_game_info(strings)
        )

    if lesson_num == 14:
        from cognitive_data_arcade.games.correlation_trap.info import get_game_info
        from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene

        return _make_pausable_with_back(CorrelationTrapScene(pm, strings), get_game_info(strings))

    if lesson_num == 15:
        from cognitive_data_arcade.games.hypothesis_arena.info import get_game_info
        from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene

        return _make_pausable_with_back(HypothesisArenaScene(pm, strings), get_game_info(strings))

    if lesson_num == 16:
        from cognitive_data_arcade.games.prediction_slider.info import get_game_info
        from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

        return _make_pausable_with_back(PredictionSliderScene(pm, strings), get_game_info(strings))

    if lesson_num == 17:
        from cognitive_data_arcade.games.feature_hunter.game import FeatHunterScene
        from cognitive_data_arcade.games.feature_hunter.info import get_game_info

        return _make_pausable_with_back(FeatHunterScene(pm, strings), get_game_info(strings))

    if lesson_num == 18:
        from cognitive_data_arcade.games.classifier_battle.game import ClassifierBattleScene
        from cognitive_data_arcade.games.classifier_battle.info import get_game_info

        return _make_pausable_with_back(ClassifierBattleScene(pm, strings), get_game_info(strings))

    if lesson_num == 19:
        from cognitive_data_arcade.games.overfitting_monster.game import OverfittingMonsterScene
        from cognitive_data_arcade.games.overfitting_monster.info import get_game_info

        return _make_pausable_with_back(
            OverfittingMonsterScene(pm, strings), get_game_info(strings)
        )

    if lesson_num == 20:
        from cognitive_data_arcade.games.anomaly_alert.game import AnomalyAlertScene
        from cognitive_data_arcade.games.anomaly_alert.info import get_game_info

        return _make_pausable_with_back(AnomalyAlertScene(pm, strings), get_game_info(strings))

    if lesson_num == 21:
        from cognitive_data_arcade.games.text_tokenizer.info import get_game_info
        from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene

        return _make_pausable_with_back(TextTokenizerLabScene(pm, strings), get_game_info(strings))

    if lesson_num == 22:
        from cognitive_data_arcade.games.word_weight_factory.info import get_game_info
        from cognitive_data_arcade.games.word_weight_factory.scene import WordWeightFactoryScene

        return _make_pausable_with_back(WordWeightFactoryScene(pm, strings), get_game_info(strings))

    if lesson_num == 23:
        from cognitive_data_arcade.games.emotion_classifier.game import EmotionClassifierScene
        from cognitive_data_arcade.games.emotion_classifier.info import get_game_info

        return _make_pausable_with_back(EmotionClassifierScene(pm, strings), get_game_info(strings))

    if lesson_num == 24:
        from cognitive_data_arcade.games.semantic_space.game import SemanticSpaceScene
        from cognitive_data_arcade.games.semantic_space.info import get_game_info

        return _make_pausable_with_back(SemanticSpaceScene(pm, strings), get_game_info(strings))

    if lesson_num == 25:
        from cognitive_data_arcade.games.topic_detective.game import TopicDetectiveScene
        from cognitive_data_arcade.games.topic_detective.info import get_game_info

        return _make_pausable_with_back(TopicDetectiveScene(pm, strings), get_game_info(strings))

    if lesson_num == 26:
        from cognitive_data_arcade.games.human_vs_model.game import HumanVsModelScene
        from cognitive_data_arcade.games.human_vs_model.info import get_game_info

        return _make_pausable_with_back(HumanVsModelScene(pm, strings), get_game_info(strings))

    if lesson_num == 27:
        from cognitive_data_arcade.games.social_network.game import SocialNetworkScene
        from cognitive_data_arcade.games.social_network.info import get_game_info

        return _make_pausable_with_back(SocialNetworkScene(pm, strings), get_game_info(strings))

    if lesson_num == 28:
        from cognitive_data_arcade.games.misinformation.game import MisinformationScene
        from cognitive_data_arcade.games.misinformation.info import get_game_info

        return _make_pausable_with_back(MisinformationScene(pm, strings), get_game_info(strings))

    if lesson_num == 29:
        from cognitive_data_arcade.games.recommendation_bubble.game import (
            RecommendationBubbleScene,
        )
        from cognitive_data_arcade.games.recommendation_bubble.info import get_game_info

        return _make_pausable_with_back(
            RecommendationBubbleScene(pm, strings), get_game_info(strings)
        )

    if lesson_num == 30:
        from cognitive_data_arcade.games.bias_blind_spot.game import BiasBlindSpotScene
        from cognitive_data_arcade.games.bias_blind_spot.info import get_game_info

        return _make_pausable_with_back(BiasBlindSpotScene(pm, strings), get_game_info(strings))

    if lesson_num == 31:
        from cognitive_data_arcade.games.you_were_the_dataset.game import YouWereTheDatasetScene
        from cognitive_data_arcade.games.you_were_the_dataset.info import get_game_info

        return _make_pausable_with_back(YouWereTheDatasetScene(pm, strings), get_game_info(strings))

    if lesson_num == 32:
        from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene
        from cognitive_data_arcade.games.architects_trial.info import get_game_info

        return _make_pausable_with_back(ArchitectsTrialScene(pm, strings), get_game_info(strings))

    # Special cases (RT Lab, BigDataMap): fall back to game_factory_for
    factory = game_factory_for(lesson_num, pm, strings)
    if factory is None:
        return None
    return factory()
